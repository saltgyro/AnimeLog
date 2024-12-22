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

//addEventListener は「特定のイベントが発生したときに実行する関数（リスナー）」を登録するためのメソッドです。
//document はウェブページ全体（HTMLドキュメント）を表します。
//DOMContentLoaded はイベントの一種で、「HTMLの構造が完全に読み込まれたとき」に発生します。
//関数 (function() {...}イベントが発生したときに実行される処理（コールバック関数）を定義しています。
document.addEventListener("DOMContentLoaded", function () {
    const buttons = document.querySelectorAll("button[data-status]");
    console.log("イベントが呼び出された:", buttons);


    //data-status 属性を持つすべてのボタンを取得し、それを変数 buttons に格納
    //buttons.forEach(button => { ... }) は、buttons というリスト（NodeList）の各要素に対して繰り返し処理を
    buttons.forEach(button => {
        button.addEventListener("click", function () {

            // クリックされたボタンの情報を出力
            console.log("クリックされたボタン:", this);
            console.log("データステータス:", this.dataset.status);
            console.log("データアニメID:", this.dataset.animeId);

            const animeId = this.dataset.animeId;
            const status = this.dataset.status;
            console.log("CSRFトークン:", csrfToken);
            console.log(updateStatusUrl);
            fetch(updateStatusUrl, {  
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken":  getCookie('csrftoken')
                },
                body: JSON.stringify({
                    anime_id: animeId,
                    status: status,
                }),
            })
            .then(response => response.json())
            .then(data => {
                console.log("データ更新成功:", data);
                
                // 動的にボタンの状態を変更
                document.getElementById("watched-btn").className = data.is_watched ? "btn-active" : "btn-inactive";
                document.getElementById("favorite-btn").className = data.is_favorite ? "btn-active" : "btn-inactive";
                document.getElementById("plan-to-watch-btn").className = data.is_plan_to_watch ? "btn-active" : "btn-inactive";

                // 視聴済が解除されたらお気に入りを無効化
                document.getElementById("favorite-btn").disabled = !data.is_watched;
            })
            .catch(error => console.error("エラーが発生しました:", error));
        });
    });
});


//ユーザー評価
document.addEventListener("DOMContentLoaded", function () {
    const ratingButton = document.getElementById("rating-submit");
    if (ratingButton) {
        ratingButton.addEventListener("click", function () {
            const animeId = this.dataset.animeId;
            const rating = parseFloat(document.getElementById("rating-input").value);

            if (isNaN(rating) || rating < 0 || rating > 5) {
                alert("評価は0〜5の間で入力してください。");
                return;
            }

            fetch("/anime/update_rating/", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": getCookie("csrftoken")
                },
                body: JSON.stringify({
                    anime_id: animeId,
                    rating: rating
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.message) {
                    alert(data.message);
                } else if (data.error) {
                    console.error(data.error);
                }
            })
            .catch(error => console.error("エラーが発生しました:", error));
        });
    }
});
