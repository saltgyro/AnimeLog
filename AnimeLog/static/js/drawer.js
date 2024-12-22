document.addEventListener("DOMContentLoaded", function () {
    const toggleButton = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");
    
    toggleButton.addEventListener("click", function () {
        if (menu.classList.contains("hidden")) {
            menu.classList.remove("hidden");
            menu.classList.add("visible");
            
        } else {
            menu.classList.remove("visible");
            menu.classList.add("hidden");
            
        }
    });
});