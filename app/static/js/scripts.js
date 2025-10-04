document.addEventListener('DOMContentLoaded', () => {
    const events = document.querySelectorAll('.events li');
    const offsetFactorX = 0.2; // przesunięcie w prawo jako % szerokości elementu
    const offsetFactorY = 20;  // przesunięcie w dół w px

    events.forEach((event, index) => {
        const width = event.offsetWidth;
        const xOffset = index * width * offsetFactorX;
        const yOffset = index * offsetFactorY;

        // zapis przesunięcia jako zmienne CSS dla hover
        event.style.setProperty('--x-offset', `${xOffset}px`);
        event.style.setProperty('--y-offset', `${yOffset}px`);

        // ustawienie początkowego przesunięcia
        event.style.transform = `translate(${xOffset}px, ${yOffset}px)`;
    });

    // dodatkowy padding, żeby ostatni element nie był przycięty
    if (events.length > 0) {
        const extraSpace = events.length * offsetFactorY * 2;
        events[0].parentElement.style.paddingBottom = `${extraSpace}px`;
    }
});
