const searchForm = document.getElementById("searchForm");
const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

if (searchForm) {
    searchForm.addEventListener("submit", async function (event) {
        event.preventDefault();

        const query = searchInput.value.trim();

        if (query === "") {
            searchResults.textContent = "検索ワードを入力してください。";
            return;
        }

        searchResults.textContent = "検索中……";

        try {
            const response = await fetch(
                "/api/search?q=" + encodeURIComponent(query)
            );

            const data = await response.json();

            searchResults.innerHTML = "";

            if (data.error) {
                searchResults.textContent = data.error;
                return;
            }

            if (!data.results || data.results.length === 0) {
                searchResults.textContent = "検索結果がありません。";
                return;
            }

            for (const result of data.results) {
                const item = document.createElement("div");
                item.className = "result-item";

                const title = document.createElement("a");
                title.className = "result-title";
                title.textContent = result.title || "無題";
                title.href = result.url;
                title.target = "_blank";
                title.rel = "noopener noreferrer";

                const url = document.createElement("div");
                url.className = "result-url";
                url.textContent = result.url || "";

                const snippet = document.createElement("p");
                snippet.className = "result-snippet";
                snippet.textContent = result.content || "";

                item.appendChild(title);
                item.appendChild(url);
                item.appendChild(snippet);

                searchResults.appendChild(item);
            }

        } catch (error) {
            searchResults.textContent =
                "検索サーバーに接続できませんでした。";
        }
    });
}