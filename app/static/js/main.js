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

// Safe HTML escape for popup text
function esc(s){
  return String(s ?? "").replace(/[&<>"'`=\/]/g, c => ({
    '&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;','/':'&#x2F;','`':'&#x60;','=':'&#x3D;'
  }[c]));
}

// --- Map: US-only, heatmap (neg=blue, pos=orange) + internal state lines + point overlay ---
(function initMap() {
  // Hide any accidental duplicate #map elements not in the full-bleed hero
  const duplicateMaps = Array.from(document.querySelectorAll("#map"))
    .filter(el => !el.closest(".map-hero"));
  duplicateMaps.forEach(el => { el.style.display = "none"; });

  const mapEl = document.getElementById("map");
  const errEl = document.getElementById("mapError");
  if (!mapEl || typeof maplibregl === "undefined") return;

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
    if (errEl) { errEl.hidden = false; errEl.textContent = "Map failed to initialize."; }
    return;
  }

  map.addControl(new maplibregl.NavigationControl({ visualizePitch: false }), "top-right");

  map.on("load", async () => {
    map.resize();
    window.addEventListener("resize", () => map.resize());
    map.fitBounds(US_LOWER_48_BOUNDS, { padding: 20, duration: 0 });

    // --- Fetch data first so failures are visible ---
    let geo = null;
    try {
      const r = await fetch("/api/zip-heat", { cache: "no-store" });
      if (!r.ok) throw new Error(`zip-heat ${r.status}`);
      geo = await r.json();
      if (!geo || !geo.features) throw new Error("Invalid GeoJSON");
      console.log("zip-heat sample:", geo);
    } catch (e) {
      console.error(e);
      if (errEl) { errEl.hidden = false; errEl.textContent = "Data load failed."; }
      return;
    }

    // Source (no clustering for heatmap)
    map.addSource("zip-points", { type: "geojson", data: geo });

    // Heatmap for NEGATIVE values
    map.addLayer({
      id: "heat-neg",
      type: "heatmap",
      source: "zip-points",
      filter: ["<", ["get", "value"], 0],
      maxzoom: 12,
      paint: {
        "heatmap-weight": ["interpolate", ["linear"], ["abs", ["get", "value"]], 0, 0, 10, 1],
        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 0.8, 12, 2],
        "heatmap-color": [
          "interpolate", ["linear"], ["heatmap-density"],
          0, "rgba(0,0,0,0)",
          0.2, "#c6dbef",
          0.5, "#6baed6",
          0.8, "#3182bd",
          1.0, "#08519c"
        ],
        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 12, 22],
        "heatmap-opacity": 0.85
      }
    });

    // Heatmap for POSITIVE values
    map.addLayer({
      id: "heat-pos",
      type: "heatmap",
      source: "zip-points",
      filter: [">", ["get", "value"], 0],
      maxzoom: 12,
      paint: {
        "heatmap-weight": ["interpolate", ["linear"], ["get", "value"], 0, 0, 10, 1],
        "heatmap-intensity": ["interpolate", ["linear"], ["zoom"], 0, 0.8, 12, 2],
        "heatmap-color": [
          "interpolate", ["linear"], ["heatmap-density"],
          0, "rgba(0,0,0,0)",
          0.2, "#fff7bc",
          0.5, "#fec44f",
          0.8, "#fe9929",
          1.0, "#d95f0e"
        ],
        "heatmap-radius": ["interpolate", ["linear"], ["zoom"], 0, 2, 12, 22],
        "heatmap-opacity": 0.85
      }
    });

    // Internal state borders via us-atlas TopoJSON → GeoJSON mesh
    await loadScriptOnce("https://unpkg.com/topojson-client@3");
    try {
      const topoRes = await fetch("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json", { cache: "force-cache" });
      const topo = await topoRes.json();
      const internalMesh = window.topojson.mesh(topo, topo.objects.states, (a, b) => a !== b);
      map.addSource("state-borders", { type: "geojson", data: internalMesh });
      map.addLayer({
        id: "state-borders-line",
        type: "line",
        source: "state-borders",
        paint: {
          "line-color": "#ffffff",
          "line-width": ["interpolate", ["linear"], ["zoom"], 3, 0.6, 6, 1.0, 8, 1.4],
          "line-opacity": 0.9
        }
      });
    } catch (e) {
      console.warn("Failed to load/draw state borders mesh:", e);
    }

    // Point overlay at closer zoom
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

    // Ensure state lines are beneath circles (but above heat)
    if (map.getLayer("state-borders-line")) {
      map.moveLayer("state-borders-line", "zip-circles");
    }

    // Tooltip
    const popup = new maplibregl.Popup({ closeButton: false, closeOnClick: false, offset: 8 });

    map.on("mouseenter", "zip-circles", () => {
      map.getCanvas().style.cursor = "pointer";
    });

    map.on("mousemove", "zip-circles", (e) => {
      const f = e.features && e.features[0];
      if (!f) return;
      const [lng, lat] = f.geometry.coordinates;
      const { zip, value, city, state, metro, county } = f.properties;
      popup
        .setLngLat([lng, lat])
        .setHTML(
          `<div style="font-size:12px;line-height:1.35;">
             <div>ZIP: <strong>${esc(zip)}</strong></div>
             <div>City: <strong>${esc(city)}</strong></div>
             <div>State: <strong>${esc(state)}</strong></div>
             <div>Metro: <strong>${esc(metro)}</strong></div>
             <div>County: <strong>${esc(county)}</strong></div>
             <div>Forecast: <strong>${Number(value).toFixed(1)}%</strong></div>
           </div>`
        )
        .addTo(map);
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

// --- Helpers ---
let __scriptLoaded = {};
function loadScriptOnce(src) {
  if (__scriptLoaded[src]) return __scriptLoaded[src];
  __scriptLoaded[src] = new Promise((resolve, reject) => {
    const s = document.createElement("script");
    s.src = src;
    s.async = true;
    s.onload = resolve;
    s.onerror = reject;
    document.head.appendChild(s);
  });
  return __scriptLoaded[src];
}
