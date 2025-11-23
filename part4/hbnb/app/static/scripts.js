/* 
  This is a SAMPLE FILE to get you started.
  Please, follow the project instructions to complete the tasks.
*/
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

