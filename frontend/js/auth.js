// API base URL
const API_URL = 'http://127.0.0.1:5000';

// Check if user is already logged in
function checkAuth() {
    const token = localStorage.getItem('access_token');
    if (token && window.location.pathname.includes('index.html')) {
        // User is logged in, redirect to today page
        window.location.href = 'today.html';
    }
}

// Run on page load
checkAuth();

// Get the form element
const authForm = document.querySelector('.auth-form');

if (authForm) {
    authForm.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent page reload

        // Determine if this is login or signup
        const isSignup = window.location.pathname.includes('signup.html');
        
        // Get form values
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;
        
        let endpoint, bodyData;
        
        if (isSignup) {
            const username = document.getElementById('username').value;
            endpoint = '/signup';
            bodyData = { username, email, password };
        } else {
            endpoint = '/login';
            bodyData = { email, password };
        }

        try {
            // Show loading (optional - you can add a spinner later)
            const submitBtn = authForm.querySelector('.primary-btn');
            const originalText = submitBtn.textContent;
            submitBtn.textContent = 'Loading...';
            submitBtn.disabled = true;

            // Make API request
            const response = await fetch(API_URL + endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(bodyData)
            });

            const data = await response.json();

            // Reset button
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;

            if (response.ok) {
                // Success!
                if (isSignup) {
                    alert('Account created! Please log in.');
                    window.location.href = 'index.html';
                } else {
                    // Store token and user data
                    localStorage.setItem('access_token', data.access_token);
                    localStorage.setItem('user', JSON.stringify(data.user));
                    
                    // Redirect to main app
                    window.location.href = 'today.html';
                }
            } else {
                // Show error
                alert(data.message || 'Something went wrong');
            }
        } catch (error) {
            console.error('Error:', error);
            alert('Cannot connect to server. Make sure Flask is running!');
            
            // Reset button
            const submitBtn = authForm.querySelector('.primary-btn');
            submitBtn.textContent = originalText;
            submitBtn.disabled = false;
        }
    });
}


