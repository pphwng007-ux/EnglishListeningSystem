document.querySelectorAll(".nav a").forEach((link) => {
    if (link.pathname === window.location.pathname) {
        link.style.background = "var(--surface-strong)";
        link.style.color = "var(--primary)";
    }
});
