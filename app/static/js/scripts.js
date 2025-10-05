// ==================== Authentication Management ====================

/**
 * Check if user is logged in by verifying JWT token exists
 */
function isUserLoggedIn() {
    const token = localStorage.getItem('token');
    return token !== null && token !== '';
}

/**
 * Get current user data from localStorage
 */
function getCurrentUser() {
    const userStr = localStorage.getItem('user');
    return userStr ? JSON.parse(userStr) : null;
}

/**
 * Logout user by removing JWT token and user data
 */
async function logout() {
    try {
        const token = localStorage.getItem('token');

        // Call backend logout endpoint (optional, for logging purposes)
        if (token) {
            await fetch('/users/logout', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${token}`,
                    'Content-Type': 'application/json'
                }
            });
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        // Always clear local storage regardless of API call result
        localStorage.removeItem('token');
        localStorage.removeItem('user');

        // Redirect to home page
        window.location.href = '/';
    }
}

/**
 * Update header navigation based on authentication state
 */
function updateAuthButton() {
    const authButton = document.getElementById('auth-button');

    if (!authButton) return;

    if (isUserLoggedIn()) {
        const user = getCurrentUser();
        const userName = user?.email?.split('@')[0] || 'Użytkownik';

        // Change to logout button
        authButton.textContent = 'Wyloguj się';
        authButton.href = '#';
        authButton.onclick = (e) => {
            e.preventDefault();
            logout();
        };

        // Optional: Add user info display
        authButton.title = `Zalogowany jako: ${user?.email || ''}`;
    } else {
        // Show login button
        authButton.textContent = 'Zaloguj się';
        authButton.href = '/navigation/login';
        authButton.onclick = null;
        authButton.title = '';
    }

    // Additionally hide any other .login-btn buttons (except the header auth button) when logged in
    const loginButtons = document.querySelectorAll('.login-btn');
    loginButtons.forEach(btn => {
        if (btn.id === 'auth-button') return; // keep header button visible
        btn.style.display = isUserLoggedIn() ? 'none' : '';
    });
}

// ==================== Event Animations ====================

document.addEventListener('DOMContentLoaded', () => {
    // Update auth button on page load
    updateAuthButton();

    // Event card flip: initialize map on first hover
    const flipCards = document.querySelectorAll('.event-card');
    flipCards.forEach(card => {
        card.addEventListener('mouseenter', () => {
            if (card.dataset.mapInited === '1') return;
            const addr = card.getAttribute('data-address');
            const mapContainer = card.querySelector('.event-map');
            if (!addr || !mapContainer || typeof L === 'undefined') return;
            initEventMap(mapContainer, addr)
                .then(() => { card.dataset.mapInited = '1'; })
                .catch((e) => { console.warn('Map init failed for address', addr, e); });
        });
    });

    // Event card animations (legacy list animations if any <li> under .events)
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

    // ==================== Upcoming Events Calendar ====================
    const upcomingBtn = document.querySelector('.btn-upcoming-events');
    let originalEventsGrid = null;
    let showingCalendar = false;
    if (upcomingBtn) {
        upcomingBtn.addEventListener('click', async (e) => {
            e.preventDefault();
            try {
                // Toggle back to list if calendar is currently shown
                if (showingCalendar) {
                    const cal = document.querySelector('.calendar-wrapper');
                    if (cal && originalEventsGrid) {
                        cal.replaceWith(originalEventsGrid);
                    }
                    upcomingBtn.textContent = 'Zobacz wszystkie';
                    showingCalendar = false;
                    return;
                }

                const grid = document.querySelector('.events-grid');
                if (!grid) return;
                originalEventsGrid = grid; // keep original element for restoration

                // Fetch upcoming events
                const resp = await fetch('/events/upcoming');
                const events = resp.ok ? await resp.json() : [];

                // Replace grid with calendar container
                const calendarWrapper = document.createElement('div');
                calendarWrapper.className = 'calendar-wrapper';
                grid.replaceWith(calendarWrapper);

                // Render calendar for current month
                const today = new Date();
                renderCalendar(calendarWrapper, events, new Date(today.getFullYear(), today.getMonth(), 1));

                // Update button label to allow toggling back
                upcomingBtn.textContent = 'Pokaż listę';
                showingCalendar = true;
            } catch (err) {
                console.error('Failed to load upcoming events:', err);
            }
        });
    }
});

// Build and render a simple calendar and mark event days
function renderCalendar(container, events, monthDate) {
    // Normalize events by yyyy-mm-dd
    const eventsByDay = {};
    (events || []).forEach(ev => {
        const d = new Date(ev.start_date);
        if (isNaN(d)) return;
        const key = d.toISOString().slice(0, 10);
        if (!eventsByDay[key]) eventsByDay[key] = [];
        eventsByDay[key].push(ev);
    });

    // Clear container
    container.innerHTML = '';

    const header = document.createElement('div');
    header.className = 'calendar-header';

    const prevBtn = document.createElement('button');
    prevBtn.className = 'calendar-nav';
    prevBtn.textContent = '◀';
    const nextBtn = document.createElement('button');
    nextBtn.className = 'calendar-nav';
    nextBtn.textContent = '▶';

    const title = document.createElement('div');
    title.className = 'calendar-title';
    const monthFormatter = new Intl.DateTimeFormat('pl-PL', { month: 'long', year: 'numeric' });
    title.textContent = monthFormatter.format(monthDate);

    header.appendChild(prevBtn);
    header.appendChild(title);
    header.appendChild(nextBtn);

    const grid = document.createElement('div');
    grid.className = 'calendar-grid';

    // Weekday headers (Mon-Sun)
    const weekdays = ['Pn', 'Wt', 'Śr', 'Cz', 'Pt', 'So', 'Nd'];
    weekdays.forEach(d => {
        const w = document.createElement('div');
        w.className = 'calendar-weekday';
        w.textContent = d;
        grid.appendChild(w);
    });

    const year = monthDate.getFullYear();
    const month = monthDate.getMonth();

    const firstDay = new Date(year, month, 1);
    const lastDay = new Date(year, month + 1, 0);

    // Calculate offset: JS getDay() -> 0 Sun, 1 Mon ... ; we want Mon=0
    let startOffset = firstDay.getDay() - 1;
    if (startOffset < 0) startOffset = 6; // if Sunday

    const totalDays = lastDay.getDate();

    // Add leading empty cells
    for (let i = 0; i < startOffset; i++) {
        const empty = document.createElement('div');
        empty.className = 'calendar-day empty';
        grid.appendChild(empty);
    }

    // Add day cells
    for (let day = 1; day <= totalDays; day++) {
        const cell = document.createElement('div');
        cell.className = 'calendar-day';

        const dateEl = document.createElement('div');
        dateEl.className = 'day-number';
        dateEl.textContent = String(day);
        cell.appendChild(dateEl);

        const cellDate = new Date(year, month, day);
        const key = new Date(Date.UTC(cellDate.getFullYear(), cellDate.getMonth(), cellDate.getDate()))
            .toISOString().slice(0, 10);
        const dayEvents = eventsByDay[key] || [];

        if (dayEvents.length > 0) {
            cell.classList.add('has-event');
            const dots = document.createElement('div');
            dots.className = 'event-dots';
            // up to 3 dots
            dayEvents.slice(0, 3).forEach(() => {
                const dot = document.createElement('span');
                dot.className = 'event-dot';
                dots.appendChild(dot);
            });
            cell.appendChild(dots);

            // Tooltip list
            const tip = document.createElement('div');
            tip.className = 'event-tip';
            tip.innerHTML = dayEvents.map(ev => `• ${escapeHtml(ev.name)}`).join('<br>');
            cell.appendChild(tip);
        }

        grid.appendChild(cell);
    }

    const calendar = document.createElement('div');
    calendar.className = 'calendar';
    calendar.appendChild(header);
    calendar.appendChild(grid);

    container.appendChild(calendar);

    // Navigation handlers
    prevBtn.addEventListener('click', () => {
        const prev = new Date(year, month - 1, 1);
        renderCalendar(container, events, prev);
    });
    nextBtn.addEventListener('click', () => {
        const next = new Date(year, month + 1, 1);
        renderCalendar(container, events, next);
    });
}

function escapeHtml(str) {
    return String(str)
        .replace(/&/g, '&amp;')
        .replace(/</g, '&lt;')
        .replace(/>/g, '&gt;')
        .replace(/"/g, '&quot;')
        .replace(/'/g, '&#039;');
}

// ==================== Maps on Event Card Back ====================
async function geocodeAddress(address) {
    const url = `https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(address)}`;
    const resp = await fetch(url, {
        headers: {
            'Accept': 'application/json'
        }
    });
    if (!resp.ok) throw new Error(`Geocode failed: ${resp.status}`);
    const data = await resp.json();
    if (!Array.isArray(data) || data.length === 0) throw new Error('No results');
    const { lat, lon, display_name } = data[0];
    return { lat: parseFloat(lat), lon: parseFloat(lon), name: display_name };
}

async function initEventMap(container, address) {
    try {
        const { lat, lon } = await geocodeAddress(address);
        // Initialize Leaflet map
        const map = L.map(container, { zoomControl: true, attributionControl: true });
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap contributors'
        }).addTo(map);
        const pos = [lat, lon];
        map.setView(pos, 15);
        L.marker(pos).addTo(map);
        // Invalidate size after flip animation to render tiles correctly
        setTimeout(() => { try { map.invalidateSize(); } catch(_) {} }, 50);
        setTimeout(() => { try { map.invalidateSize(); } catch(_) {} }, 700);
    } catch (e) {
        console.warn('Failed to init map for address', address, e);
        // Fallback: show a simple message
        container.innerHTML = `<div style="display:flex;align-items:center;justify-content:center;height:100%;color:#555;">
            Nie można załadować mapy
        </div>`;
    }
}
