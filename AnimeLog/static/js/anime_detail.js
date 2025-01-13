// クッキーから特定の名前の値を取得する関数
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";"); // クッキーを分割
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim(); // 余白を削除
            // クッキー名が一致するか確認
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
