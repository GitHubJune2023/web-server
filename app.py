import os
from urllib.parse import urlparse

import requests
from flask import Flask, request, render_template_string

app = Flask(__name__)

ALLOWED_HOSTS = {"example.com", "httpbin.org"}

PAGE = """
<!doctype html>
<html>
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Web Gateway</title>
<style>
body { font: 16px Arial; max-width: 760px; margin: 40px auto; padding: 20px; background: #f3f5f9; }
input { box-sizing: border-box; width: 75%; padding: 12px; }
button { padding: 12px; cursor: pointer; }
pre { white-space: pre-wrap; overflow-wrap: anywhere; background: white; padding: 15px; }
</style>
</head>
<body>
<h1>Web Gateway</h1>
<p>Fetch a page from an approved test website.</p>
<form method="post">
<input name="url" type="url" placeholder="https://example.com" value="{{ url }}" required>
<button type="submit">Fetch</button>
</form>
{% if result %}<h2>Response</h2><pre>{{ result }}</pre>{% endif %}
{% if error %}<p>{{ error }}</p>{% endif %}
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def home():
    url = ""
    result = ""
    error = ""

    if request.method == "POST":
        url = request.form.get("url", "").strip()
        parsed = urlparse(url)

        if (
            parsed.scheme != "https"
            or not parsed.hostname
            or parsed.hostname.lower() not in ALLOWED_HOSTS
            or parsed.username
            or parsed.password
        ):
            error = "Use HTTPS and an approved hostname."
        else:
            try:
                response = requests.get(
                    url,
                    timeout=8,
                    allow_redirects=False,
                    headers={"User-Agent": "EducationalWebGateway/1.0"},
                )
                content_type = response.headers.get("Content-Type", "")

                if response.is_redirect:
                    error = "Redirects are disabled in this demo."
                elif "text/" not in content_type and "json" not in content_type:
                    error = "This demo only displays text and JSON."
                else:
                    result = f"HTTP {response.status_code}\n\n{response.text[:20000]}"
            except requests.RequestException:
                error = "The destination could not be reached."

    return render_template_string(
        PAGE, url=url, result=result, error=error
    )

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=int(os.environ.get("PORT", "5000"))
    )
