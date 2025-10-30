from flask import Flask, send_from_directory
import os

app = Flask(__name__, static_folder="static", template_folder="templates")

# === Главная страница ===
@app.route("/")
def home():
    return send_from_directory("templates", "index.html")

# === Раздача файлов из static/ (видео, js, css) ===
@app.route("/static/<path:filename>")
def static_files(filename):
    return send_from_directory("static", filename)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
