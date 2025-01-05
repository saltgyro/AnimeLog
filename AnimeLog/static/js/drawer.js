document.addEventListener("DOMContentLoaded", function () {
    // メニュー用のトグルボタン
    const menuToggleButton = document.getElementById("menu-toggle");
    const menu = document.getElementById("menu");
    
    // メニューの表示/非表示
    menuToggleButton.addEventListener("click", function () {
        if (menu.classList.contains("hidden")) {
            menu.classList.remove("hidden");
            menu.classList.add("visible");
        } else {
            menu.classList.remove("visible");
            menu.classList.add("hidden");
        }
    });
});
