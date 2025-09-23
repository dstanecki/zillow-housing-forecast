// --- Profile dropdown ---
document.addEventListener("click", (e) => {
  const menu = document.querySelector("#profileMenu");
  if (!menu) return;

  const trigger = menu.querySelector(".profile-trigger");
  const dropdown = menu.querySelector(".profile-dropdown");

  if (trigger && trigger.contains(e.target)) {
    const open = menu.classList.toggle("open");
    trigger.setAttribute("aria-expanded", String(open));
    if (dropdown) dropdown.style.display = open ? "block" : "none";
  } else if (!menu.contains(e.target)) {
    menu.classList.remove("open");
    if (trigger) trigger.setAttribute("aria-expanded", "false");
    if (dropdown) dropdown.style.display = "none";
  }
});

// --- Map: US-only, true value heatmap (neg=blue, pos=red) + state lines + point overlay ---
(function initMap() {
  // Hide any accidental duplicate #map elements not in the full-bleed hero
  const duplicateMaps = Array.from(document.querySelectorAll("#map"))
    .filter(el => !el.closest(".map-hero"));
  duplicateMaps.forEach(el => { el.style.display = "none"; });

  const mapEl = document.getElementById("map");
  const errEl = document.getElementById("mapError");
  if (!mapEl || typeof maplibregl === "undefined") return;

  // Contiguous US bounds
  const US_LOWER_48_BOUNDS = [[-125.0, 24.4], [-66.9, 49.5]];

  let map;
  try {
    map = new maplibregl.Map({
      container: "map",
      style: "https://demotiles.maplibre.org/style.json",
      center: [-96, 38],
      zoom: 3.4,
      maxBounds: US_LOWER_48_BOUNDS
    });
  } catch (e) {
    if (errEl) {
      errEl.hidden = false;
      errEl.textContent = "Map failed to initialize.";
    }
    return;
  }

  map.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), "top-right");

  map.on("load", async () => {
    // ensure rendering even if container size changes
    map.resize();
    window.addEventListener("resize", () => map.resize());
    map.fitBounds(US_LOWER_48_BOUNDS, { padding: 20, duration: 0 });

    // GeoJSON source (no clustering for a proper heatmap)
    map.addSource("zip-points", { type: "geojson", data: "/api/zip-heat" });

    // Heatmap for NEGATIVE values (weight by |value|, cool colors)
    map.addLayer({
      id: "heat-neg",
      type: "heatmap",
      source: "zip-points",
      filter: ["<", ["get", "value"], 0],
      maxzoom: 12,
      paint: {
        "heatmap-weight": [
          "interpolate", ["linear"], ["abs", ["get", "value"]],
          0, 0, 10, 1
        ],
        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 0.8, 12, 2],
        "heatmap-color": [
          "interpolate", ["linear"], ["heatmap-density"],
          0, "rgba(0,0,0,0)",
          0.2, "#c6dbef",
          0.5, "#6baed6",
          0.8, "#3182bd",
          1.0, "#08519c"
        ],
        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 12, 24],
        "heatmap-opacity": 0.9
      }
    });

    // Heatmap for POSITIVE values (weight by value, warm colors)
    map.addLayer({
      id: "heat-pos",
      type: "heatmap",
      source: "zip-points",
      filter: [">", ["get", "value"], 0],
      maxzoom: 12,
      paint: {
        "heatmap-weight": [
          "interpolate", ["linear"], ["get", "value"],
          0, 0, 10, 1
        ],
        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 0.8, 12, 2],
        "heatmap-color": [
          "interpolate", ["linear"], ["heatmap-density"],
          0, "rgba(0,0,0,0)",
          0.2, "#fff7bc",
          0.5, "#fec44f",
          0.8, "#fe9929",
          1.0, "#d95f0e"
        ],
        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 12, 24],
        "heatmap-opacity": 0.9
      }
    });

    // State outlines (add your GeoJSON at /static/data/us_states.json)
    try {
      map.addSource("us-states", {
        type: "geojson",
        data: "/static/data/us_states.json"
      });
      map.addLayer({
        id: "state-lines",
        type: "line",
        source: "us-states",
        paint: {
          "line-color": "#555",
          "line-width": 1,
          "line-opacity": 0.7
        }
      });
    } catch (e) {
      console.warn("State lines source/layer could not be added:", e);
    }

    // Circle overlay at closer zoom for exact values (on top)
    map.addLayer({
      id: "zip-circles",
      type: "circle",
      source: "zip-points",
      minzoom: 7,
      paint: {
        "circle-radius": ["interpolate", ["linear"], ["zoom"], 7, 2.5, 12, 5],
        "circle-color": [
          "interpolate", ["linear"], ["get", "value"],
          -6, "#2c7fb8",
          -3, "#67a9cf",
           0, "#ffffbf",
           3, "#fdae61",
           6, "#d7191c"
        ],
        "circle-opacity": 0.9,
        "circle-stroke-width": 0.3,
        "circle-stroke-color": "#1f2937"
      }
    });

    // Hover tooltip for points
    const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 8 });
    map.on("mousemove", "zip-circles", (e) => {
      const f = e.features && e.features[0];
      if (!f) return;
      const { zip, value } = f.properties;
      const [lng, lat] = f.geometry.coordinates;
      popup.setLngLat([lng, lat])
           .setHTML(`<div style="font-size:12px;"><strong>${zip}</strong><br/>Forecast: ${Number(value).toFixed(1)}%</div>`)
           .addTo(map);
      map.getCanvas().style.cursor = "pointer";
    });
    map.on("mouseleave", "zip-circles", () => {
      popup.remove();
      map.getCanvas().style.cursor = "";
    });
  });

  map.on("error", () => {
    if (errEl) {
      errEl.hidden = false;
      errEl.textContent = "Map tiles or data failed to load.";
    }
  });
})();
