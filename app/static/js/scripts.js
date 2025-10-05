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

    // Event card animations
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
