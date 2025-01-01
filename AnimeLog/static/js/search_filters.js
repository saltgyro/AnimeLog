const selectedConditions = {}; // 検索条件を保存するオブジェクト

document.addEventListener('DOMContentLoaded', () => {
    // すべてのボタンを取得し、クリックイベントを設定
    document.querySelectorAll('.genre-button, .tag-button, .season-button, .studio-button').forEach(button => {
        button.addEventListener('click', (event) => {
            var type = event.target.getAttribute('data-type'); // 条件の種類 (例: genre, tag, season, studio)
            var id = event.target.getAttribute('data-id'); // 各条件のID
            var currentUrl = window.location.href;
            var newUrl = new URL(currentUrl);

            // 既存の検索条件を取得
            var params = newUrl.searchParams;

            // 複数のタグを選択可能にするために、既存のタグを追加
            if (params.has(type)) {
                // すでに同じタイプのパラメータが存在する場合、追加する
                let existingValues = params.getAll(type);
                existingValues.push(id);
                params.delete(type);  // 既存の値を削除
                existingValues.forEach(value => {
                    params.append(type, value);  // 新しい値を追加
                });
            } else {
                // タグがまだ選択されていない場合はそのまま追加
                params.append(type, id);
            }

            // 新しいURLを適用
            newUrl.search = params.toString();
            window.location.href = newUrl; // ページ遷移
        });
    });
});

// document.addEventListener('DOMContentLoaded', () => {
//     // すべてのボタンを取得し、クリックイベントを設定
//     document.querySelectorAll('.genre-button, .tag-button, .season-button, .studio-button').forEach(button => {
//         button.addEventListener('click', (event) => {
//             var type = event.target.getAttribute('data-type'); // 条件の種類 (例: genre, tag, season, studio)
//             var id = event.target.getAttribute('data-id'); // 各条件のID
//             var currentUrl = window.location.href;
//             var newUrl = new URL(currentUrl);

//             // 既存の検索条件を取得
//             var params = newUrl.searchParams;

//             // クエリパラメータに選択した条件を追加
//             params.set(type, id); // 例: ?genre=1&tag=2&season=3

//             // 新しいURLを適用
//             newUrl.search = params.toString();
//             window.location.href = newUrl; // ページ遷移
            

//             console.log(`条件が更新されました:`, selectedConditions); // デバッグ用

//             // 検索結果を取得
//             fetchSearchResults();
//         });
//     });

//     console.log('DOMContentLoaded: ボタンイベントが設定されました');
// });

// function fetchSearchResults() {
//     const csrfToken = document.querySelector('input[name="csrfmiddlewaretoken"]').value;

//     console.log('送信する検索条件:', selectedConditions);
//     fetch('/anime_tracker/home/', {  // DjangoのURL
//         method: 'POST',
//         headers: {
//             'Content-Type': 'application/json',
//             'X-CSRFToken': csrfToken,
//         },
//         body: JSON.stringify(selectedConditions), // 検索条件をJSON形式で送信
//     })
//     .then(response => response.json())
//     .then(data => {
//         console.log(data); // 結果を確認
//         const animeList = document.querySelector('.anime-list');
//         animeList.innerHTML = ''; // 既存のリストをクリア

//         data.results.forEach(anime => {
//             const item = document.createElement('div');
//             item.classList.add('anime-item');
//             item.innerHTML = `
//                 <a href="/anime_tracker/anime_detail/${anime.id}">
//                     <img src="${anime.thumbnail}" alt="${anime.title}" width="150">
//                     <p>${anime.title}</p>
//                 </a>
//             `;
//             animeList.appendChild(item);
//         });
//     })
//     .catch(error => {
//         console.error('検索結果の取得に失敗しました:', error);
//         alert('検索結果の取得に失敗しました。詳細はコンソールを確認してください。');
//     });
// }
