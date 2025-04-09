document.addEventListener("DOMContentLoaded", () => {
    const dropdown = document.getElementById("global-range");
    const checkboxes = document.querySelectorAll('.filter-controls input[type="checkbox"]');
    const cards = document.querySelectorAll('.card');
  
    dropdown.addEventListener("change", function () {
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