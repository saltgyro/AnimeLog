const selectedConditions = {}; // 検索条件を保存するオブジェクト

document.addEventListener('DOMContentLoaded', () => {
    // すべてのボタンを取得し、クリックイベントを設定
    document.querySelectorAll('.genre-button, .tag-button, .season-button, .studio-button').forEach(button => {
        button.addEventListener('click', (event) => {
            const type = event.target.getAttribute('data-type'); // 条件の種類 (例: genre, tag, season, studio)
            const id = event.target.getAttribute('data-id'); // 各条件のID

            // 検索条件を更新
            if (!selectedConditions[type]) {
                selectedConditions[type] = [];
            }

            const index = selectedConditions[type].indexOf(id);
            if (index > -1) {
                // 条件削除
                selectedConditions[type].splice(index, 1);
                event.target.classList.remove('btn-primary');
                event.target.classList.add('btn-outline-primary');
            } else {
                // 条件追加
                selectedConditions[type].push(id);
                event.target.classList.remove('btn-outline-primary');
                event.target.classList.add('btn-primary');
            }

            console.log(`条件が更新されました:`, selectedConditions); // デバッグ用

            // 検索結果を取得
            fetchSearchResults();
        });
    });

    console.log('DOMContentLoaded: ボタンイベントが設定されました');
});

function fetchSearchResults() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    console.log('送信する検索条件:', selectedConditions);
    fetch('/anime_tracker/search/', {  // DjangoのURL
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(selectedConditions), // 検索条件をJSON形式で送信
    })
    .then(response => response.json())
    .then(data => {
        console.log(data); // 結果を確認
        const animeList = document.querySelector('.anime-list');
        animeList.innerHTML = ''; // 既存のリストをクリア

        data.results.forEach(anime => {
            const item = document.createElement('div');
            item.classList.add('anime-item');
            item.innerHTML = `
                <a href="/anime_tracker/anime_detail/${anime.id}">
                    <img src="${anime.thumbnail}" alt="${anime.title}" width="150">
                    <p>${anime.title}</p>
                </a>
            `;
            animeList.appendChild(item);
        });
    })
    .catch(error => {
        console.error('検索結果の取得に失敗しました:', error);
        alert('検索結果の取得に失敗しました。詳細はコンソールを確認してください。');
    });
}
