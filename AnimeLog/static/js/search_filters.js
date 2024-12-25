const selectedConditions = {}; // 検索条件を保存するオブジェクト
console.log('呼び出されました');
document.querySelectorAll('.drawer [data-drawer-type]').forEach(button => {
    button.addEventListener('click', (event) => {
        const type = event.target.getAttribute('data-type');
        const id = event.target.getAttribute('data-id');
        
        // 検索条件を更新（既存条件との組み合わせ対応）
        if (selectedConditions[type]) {
            const index = selectedConditions[type].indexOf(id);
            if (index > -1) {
                selectedConditions[type].splice(index, 1); // 解除
            } else {
                selectedConditions[type].push(id); // 条件追加
            }
        } else {
            selectedConditions[type] = [id];
        }

        console.log(selectedConditions); // デバッグ用
    });
});


function fetchSearchResults() {
    const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

    fetch('/search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken,
        },
        body: JSON.stringify(selectedConditions),
    })
    .then(response => response.json())
    .then(data => {
        // 結果をページに反映
        const animeList = document.querySelector('.anime-list');
        animeList.innerHTML = ''; // 一旦クリア
        data.results.forEach(anime => {
            const item = document.createElement('div');
            item.innerHTML = `
                <div class="anime-item">
                    <a href="/anime_tracker/anime_detail/${anime.id}">
                        <img src="${anime.thumbnail}" alt="${anime.title}" width="150">
                        <p>${anime.title}</p>
                    </a>
                </div>
            `;
            animeList.appendChild(item);
        });
    });
}


