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

    // 検索リセットボタンを取得
    document.getElementById('reset-search').addEventListener('click', () => {
        // 現在のURLを取得
        let currentUrl = new URL(window.location.href);
        
        // URLパラメータを削除
        currentUrl.searchParams.delete('genre');
        currentUrl.searchParams.delete('tag');
        currentUrl.searchParams.delete('season');
        currentUrl.searchParams.delete('studio');
        currentUrl.searchParams.delete('status');
        currentUrl.searchParams.delete('sort');
        currentUrl.searchParams.delete('search');

        // リセットしたURLに遷移
        window.location.href = currentUrl.toString();  // ページ遷移
    });

    
    
});
