function applySort() {
    const sortOption = document.getElementById("sort-select").value;

    const currentUrl = new URL(window.location.href);

    // 現在のURLのクエリパラメータを設定
    currentUrl.searchParams.set("sort", sortOption); // 'sort' パラメータだけを設定

    // 新しいURLにリダイレクト
    window.location.href = currentUrl.toString();
}
