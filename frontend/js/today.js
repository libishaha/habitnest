// Check if user is logged in
const token = localStorage.getItem('access_token');
const user = JSON.parse(localStorage.getItem('user') || '{}');

if (!token) {
    // Not logged in, redirect to login
    window.location.href = 'index.html';
} else {
    // Show username
    const usernameDisplay = document.getElementById('username-display');
    if (usernameDisplay && user.username) {
        usernameDisplay.textContent = `Hello, ${user.username}! 🌱`;
    }
}

// Logout function
function logout() {
    localStorage.removeItem('access_token');
    localStorage.removeItem('user');
    window.location.href = 'index.html';
}