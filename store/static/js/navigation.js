document.addEventListener("DOMContentLoaded", function () {
    let currentPath = window.location.pathname;

    if (currentPath.includes("login")) {
        document.getElementById("login-dot").classList.add("active-dot");
    } else if (currentPath.includes("signup")) {
        document.getElementById("signup-dot").classList.add("active-dot");
    } else if (currentPath.includes("password_reset")) {
        document.getElementById("reset-dot").classList.add("active-dot");
    }
});
