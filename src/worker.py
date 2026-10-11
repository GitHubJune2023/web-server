from flask import Flask
from workers import wsgi

app = Flask(__name__)

@app.get("/")
def home():
    return """
    <!doctype html>
    <html>
    <head>
      <meta name="viewport" content="width=device-width, initial-scale=1">
      <title>Web Gateway</title>
      <style>
        body {
          background: #101827;
          color: white;
          font-family: Arial, sans-serif;
          text-align: center;
          padding: 70px 20px;
        }
        .box {
          max-width: 550px;
          margin: auto;
          background: #1e293b;
          padding: 28px;
          border-radius: 18px;
        }
        input, button {
          padding: 13px;
          border: 0;
          border-radius: 8px;
          font-size: 16px;
        }
        input {
          box-sizing: border-box;
          width: 100%;
          margin-bottom: 12px;
        }
        button {
          background: #60a5fa;
          color: #101827;
          cursor: pointer;
          width: 100%;
        }
        p { color: #cbd5e1; }
      </style>
    </head>
    <body>
      <div class="box">
        <h1>Web Gateway</h1>
        <p>Your Python Worker is online.</p>
        <form action="/fetch" method="get">
          <input name="url" type="url"
                 placeholder="https://example.com" required>
          <button type="submit">Open website</button>
        </form>
        <p>Website fetching will be configured next.</p>
      </div>
    </body>
    </html>
    """

Default = wsgi.entrypoint(app)
