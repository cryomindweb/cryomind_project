function checkAuth() {
    const token = localStorage.getItem("jwt");
    const role = localStorage.getItem("role");

    if (!token) {
        return redirectToLogin();
    }
    if (role !== "administrador") {
        return redirectToLogin();
    }
}

function redirectToLogin() {
    localStorage.removeItem("jwt");
    localStorage.removeItem("role"); // Limpia también el rol, por seguridad
    window.location.href = "/403";
}

checkAuth();
