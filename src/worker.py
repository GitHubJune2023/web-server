from flask import Flask
from workers import wsgi

app = Flask(__name__)

@app.get("/")
def home():
    return {"message": "My Python Worker is running!"}

Default = wsgi.entrypoint(app)
