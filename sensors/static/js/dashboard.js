document.addEventListener("DOMContentLoaded", () => {
    const checkboxes = document.querySelectorAll('.location-filter input[type="checkbox"]');
    const cards = document.querySelectorAll('.card');
  
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