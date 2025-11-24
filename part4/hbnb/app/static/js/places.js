// ---------------- UTILITY FUNCTIONS ----------------

// Get a cookie value by name
function getCookie(name) {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [key, value] = cookie.trim().split('=');
        if (key === name) return decodeURIComponent(value);
    }
    return null;
}

// Display login error messages
function showLoginError(message) {
    let errorBox = document.getElementById("login-error");

    if (!errorBox) {
        errorBox = document.createElement("div");
        errorBox.id = "login-error";
        errorBox.style.color = "red";
        errorBox.style.marginTop = "10px";
        const loginForm = document.getElementById("login-form");
        if (loginForm) loginForm.appendChild(errorBox);
    }

    errorBox.textContent = message;
}

// ---------------- LOGIN / LOGOUT ----------------
async function loginUser(email, password) {
    try {
        const response = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ email, password }),
            credentials: "include"
        });

        if (response.ok) {
            const data = await response.json();
            document.cookie = `token=${data.access_token}; path=/`;
            window.location.href = "/";
        } else {
            const err = await response.json();
            showLoginError(err.message || "Invalid email or password");
        }
    } catch (error) {
        showLoginError("Network error — check if API is running");
        console.error("Login error:", error);
    }
}

window.logout = function () {
    fetch("/api/v1/auth/logout", { method: "POST", credentials: "include" })
        .then(res => res.json())
        .then(() => { window.location.href = "/login"; })
        .catch(err => console.error("Logout error:", err));
};

// ---------------- EVENT LISTENERS ----------------
document.addEventListener('DOMContentLoaded', () => {
    // ---------------- LOGIN FORM ----------------
    const loginForm = document.getElementById('login-form');
    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();
            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();
            await loginUser(email, password);
        });
    }

    // ---------------- MAIN PAGE / PLACES ----------------
    const placesGrid = document.getElementById('placesGrid');
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');

    if (!placesGrid) return; // Exit if not on main page

    // Populate price filter dropdown
    function populatePriceFilter() {
        if (!priceFilter) return;
        const options = [10, 50, 100, 'All'];
        priceFilter.innerHTML = '';
        options.forEach(opt => {
            const optionElement = document.createElement('option');
            optionElement.value = opt;
            optionElement.textContent = opt;
            priceFilter.appendChild(optionElement);
        });
    }
    populatePriceFilter();

    // Filter places by price
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const places = document.querySelectorAll('#placesGrid .place');
            places.forEach(place => {
                const price = parseFloat(place.dataset.price);
                if (selectedPrice === 'All' || price <= parseFloat(selectedPrice)) {
                    place.style.display = 'block';
                } else {
                    place.style.display = 'none';
                }
            });
        });
    }

    // Check user authentication and fetch places
    function checkAuthentication() {
        const token = getCookie('token');
        if (!token) {
            if (loginLink) loginLink.style.display = 'block';
        } else {
            if (loginLink) loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // Fetch places from API
    async function fetchPlaces(token) {
        try {
            const response = await fetch("/api/v1/places", {
                method: "GET",
                headers: {
                    "Content-Type": "application/json",
                    "Authorization": `Bearer ${token}`
                }
            });

            if (!response.ok) throw new Error(`HTTP error! status: ${response.status}`);
            const places = await response.json();
            displayPlaces(places);
        } catch (error) {
            console.error("Error fetching places:", error);
        }
    }

    // Display places in #placesGrid
    function displayPlaces(places) {
        placesGrid.innerHTML = '';
        places.forEach(place => {
            const div = document.createElement('div');
            div.className = 'place';
            div.dataset.price = place.price;
            div.innerHTML = `
                <h3>${place.name}</h3>
                <p>${place.description}</p>
                <p><strong>Location:</strong> ${place.city}, ${place.state}</p>
                <p><strong>Price:</strong> $${place.price}</p>
            `;
            placesGrid.appendChild(div);
        });
    }

    // Initial authentication check
    checkAuthentication();
});

