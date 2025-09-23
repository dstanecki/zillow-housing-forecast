document.addEventListener("click", (e) => {
  const menu = document.querySelector("#profileMenu");
  if (!menu) return;

  const trigger = menu.querySelector(".profile-trigger");
  const dropdown = menu.querySelector(".profile-dropdown");

  const clickedInside = menu.contains(e.target);
  const isTrigger = trigger.contains(e.target);

  if (isTrigger) {
    const open = menu.classList.toggle("open");
    trigger.setAttribute("aria-expanded", String(open));
    dropdown.style.display = open ? "block" : "none";
  } else {
    // click outside: close
    menu.classList.remove("open");
    trigger.setAttribute("aria-expanded", "false");
    dropdown.style.display = "none";
  }
});
