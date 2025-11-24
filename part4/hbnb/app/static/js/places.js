    // LOGOUT FUNCTION
    window.logout = function () {
        fetch("/api/v1/auth/logout", {
            method: "POST",
            credentials: "include"
        })
        .then(res => res.json())
        .then(() => {
            // Redirect to login page
            window.location.href = "/login";
        })
        .catch(err => console.error("Logout error:", err));
    };

});

document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // Call API login function
            await loginUser(email, password);
        });
    }
});

// LOGIN FUNCTION
async function loginUser(email, password) {
    try {
        const response = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            credentials: "include"  // allow API to set cookies
        });

        // SUCCESS?
        if (response.ok) {
            const data = await response.json();

            // Store token manually too (backup)
            document.cookie = `token=${data.access_token}; path=/`;

            // Redirect to main page
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

// DISPLAY ERROR MESSAGE
function showLoginError(message) {
    let errorBox = document.getElementById("login-error");

    if (!errorBox) {
        errorBox = document.createElement("div");
        errorBox.id = "login-error";
        errorBox.style.color = "red";
        errorBox.style.marginTop = "10px";
        document.getElementById("login-form").appendChild(errorBox);
    }

    errorBox.textContent = message;
}

document.addEventListener('DOMContentLoaded', () => {

    // LOGOUT FUNCTION
    window.logout = function () {
        fetch("/api/v1/auth/logout", {
            method: "POST",
            credentials: "include"
        })
        .then(res => res.json())
        .then(() => {
            // Redirect to login page
            window.location.href = "/login";
        })
        .catch(err => console.error("Logout error:", err));
    };

});

// ---------------- LOGIN ----------------
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            // Call API login function
            await loginUser(email, password);
        });
    }
});

// LOGIN FUNCTION
async function loginUser(email, password) {
    try {
        const response = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            credentials: "include"  // allow API to set cookies
        });

        if (response.ok) {
            const data = await response.json();

            // Store token manually too (backup)
            document.cookie = `token=${data.access_token}; path=/`;

            // Redirect to main page
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

// DISPLAY ERROR MESSAGE
function showLoginError(message) {
    let errorBox = document.getElementById("login-error");

    if (!errorBox) {
        errorBox = document.createElement("div");
        errorBox.id = "login-error";
        errorBox.style.color = "red";
        errorBox.style.marginTop = "10px";
        document.getElementById("login-form").appendChild(errorBox);
    }

    errorBox.textContent = message;
}

// ---------------- MAIN PAGE / PLACES ----------------
document.addEventListener('DOMContentLoaded', () => {
    // Only run if #places-list exists (we are on the main page)
    const placesList = document.getElementById('places-list');
    const loginLink = document.getElementById('login-link');
    const priceFilter = document.getElementById('price-filter');

    if (!placesList) return;  // Exit if not main page
    // -----------------------------
    // Populate price filter dropdown
    // -----------------------------
    function populatePriceFilter() {
        if (!priceFilter) return;

        const options = [10, 50, 100, 'All'];
        priceFilter.innerHTML = ''; // Clear existing options

        options.forEach(opt => {
            const optionElement = document.createElement('option');
            optionElement.value = opt;
            optionElement.textContent = opt;
            priceFilter.appendChild(optionElement);
        });
    }

    // Call it here to fill the dropdown
    populatePriceFilter();

    if (priceFilter) {
    priceFilter.addEventListener('change', (event) => {
        const selectedPrice = event.target.value;
        const places = document.querySelectorAll('#places-list .place');

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



    // Helper to get cookie
    function getCookie(name) {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [key, value] = cookie.trim().split('=');
            if (key === name) return decodeURIComponent(value);
        }
        return null;
    }

    // Check authentication
    function checkAuthentication() {
        const token = getCookie('token');

        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
            fetchPlaces(token);
        }
    }

    // Fetch places
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

    // Display places
    function displayPlaces(places) {
        placesList.innerHTML = ''; // Clear previous

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
            placesList.appendChild(div);
        });
    }

    // Client-side filtering
    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const places = document.querySelectorAll('#places-list .place');

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

    // Initialize
    checkAuthentication();
});

