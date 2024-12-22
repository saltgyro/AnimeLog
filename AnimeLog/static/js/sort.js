function applySort() {
    const sortOption = document.getElementById("sort-select").value;

    const currentUrl = new URL(window.location.href);

    // 現在のURLのクエリパラメータを設定
    currentUrl.searchParams.set("sort", sortOption);

    // クエリパラメータを設定
    const [sortField, sortOrder] = sortOption.split('-');
    
    currentUrl.searchParams.set('sort', sortField);
    currentUrl.searchParams.set('order', sortOrder);

    // 新しいURLにリダイレクト
    window.location.href = currentUrl.toString();
}