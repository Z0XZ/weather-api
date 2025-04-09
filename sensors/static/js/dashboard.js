document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("global-range");
    const customRange = document.getElementById("egendefinert");
    const checkboxes = document.querySelectorAll('.filter-controls input[type="checkbox"]');
    const cards = document.querySelectorAll('.card');
  
    dropdown.addEventListener("change", function () {
      console.log(customRange)
      // Tøm datofeltene hvis dropdown er valgt
      document.getElementById("start-date").value = "";
      document.getElementById("end-date").value = "";
      if (dropdown.value === "custom") {
        customRange.style.display = "flex";
      } else {
        customRange.style.display = "none";}
      // Finn alle lastChart-funksjoner som er globale
      for (const fnName in window) {
        if (fnName.startsWith("loadChart_") && typeof window[fnName] === "function") {
          window[fnName]();  // kall funksjonen på nytt
        }
      }
    });

    function updateVisibleCards() {
      const activeLocations = Array.from(checkboxes)
        .filter(cb => cb.checked)
        .map(cb => cb.value);
  
      cards.forEach(card => {
        const matches = activeLocations.some(loc => card.classList.contains('location-' + loc));
        card.style.display = matches ? 'block' : 'none';
      });
    }
  
    checkboxes.forEach(cb => cb.addEventListener("change", updateVisibleCards));
  
    updateVisibleCards(); // init
  });

document.getElementById("start-date").addEventListener("change", reloadAllGraphs);
document.getElementById("end-date").addEventListener("change", reloadAllGraphs);

function reloadAllGraphs() {
  // Tøm dropdown hvis egendefinert periode er brukt
  if (document.getElementById("start-date").value || document.getElementById("end-date").value) {
    document.getElementById("global-range").value = "";
  }

  for (const fnName in window) {
    if (fnName.startsWith("loadChart_") && typeof window[fnName] === "function") {
      window[fnName]();
    }
  }
}