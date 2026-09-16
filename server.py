from http.server import HTTPServer, SimpleHTTPRequestHandler
from urllib.parse import urlparse, parse_qs, quote
import json
import urllib.request


# 後で実際のSearXNGインスタンスを設定する
SEARXNG_URL = "http://127.0.0.1:8080/search"


class NEXUSHandler(SimpleHTTPRequestHandler):

    def do_GET(self):
        parsed = urlparse(self.path)

        if parsed.path == "/api/search":
            self.search(parsed)
        else:
            super().do_GET()

    def search(self, parsed):
        params = parse_qs(parsed.query)
        query = params.get("q", [""])[0].strip()

        if not query:
            self.send_json({"results": []})
            return

        search_url = (
            SEARXNG_URL
            + "?q=" + quote(query)
            + "&format=json"
            + "&language=ja"
            + "&safesearch=2"
        )

        try:
            request = urllib.request.Request(
                search_url,
                headers={
                    "User-Agent": "NEXUS/1.0"
                }
            )

            with urllib.request.urlopen(request, timeout=10) as response:
                data = json.loads(
                    response.read().decode("utf-8")
                )

            results = []

            for item in data.get("results", [])[:10]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "content": item.get("content", "")
                })

            self.send_json({
                "results": results
            })

        except Exception as error:
            print("Search error:", error)

            self.send_json({
                "error": "検索サーバーに接続できませんでした。"
            })

    def send_json(self, data):
        body = json.dumps(
            data,
            ensure_ascii=False
        ).encode("utf-8")

        self.send_response(200)
        self.send_header(
            "Content-Type",
            "application/json; charset=utf-8"
        )
        self.send_header(
            "Content-Length",
            str(len(body))
        )
        self.end_headers()

        self.wfile.write(body)


if __name__ == "__main__":
    server = HTTPServer(
        ("localhost", 8000),
        NEXUSHandler
    )

    print("NEXUS running at http://localhost:8000")
    server.serve_forever()