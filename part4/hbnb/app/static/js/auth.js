// =============================
// LOGOUT FUNCTION
// =============================
window.logout = function () {
    fetch("/api/v1/auth/logout", {
        method: "POST",
        credentials: "include"
    })
    .then(res => res.json())
    .then(() => {
        window.location.href = "/login";
    })
    .catch(err => console.error("Logout error:", err));
};

// =============================
// LOGIN FORM HANDLER
// =============================
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value.trim();
            const password = document.getElementById('password').value.trim();

            await loginUser(email, password);
        });
    }
});

// =============================
// LOGIN FUNCTION
// =============================
async function loginUser(email, password) {
    try {
        const response = await fetch("/api/v1/auth/login", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify({ email, password }),
            credentials: "include"
        });

        if (response.ok) {
            const data = await response.json();

            // Backup token in cookie
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

// =============================
// ERROR MESSAGE FUNCTION
// =============================
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

// =============================
// GENERIC COOKIE READER
// Needed for index page
// =============================
function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(";").shift();
    return null;
}

