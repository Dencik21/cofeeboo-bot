from aiohttp import web
import os

async def home(request):
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8" />
        <title>Cofeeboo ☕</title>
        <style>
            body { background: #111; color: #fff; font-family: Arial; text-align: center; padding-top: 20vh; }
            h1 { color: #ffcc66; }
            a { color: #5e3eff; text-decoration: none; font-size: 18px; }
        </style>
    </head>
    <body>
        <h1>☕ Cofeeboo работает!</h1>
        <p>Это ваш сайт Railway.</p>
        <a href="https://t.me/CofeebooBot">Открыть Telegram бота</a>
    </body>
    </html>
    """
    return web.Response(text=html, content_type="text/html")

app = web.Application()
app.router.add_get("/", home)

port = int(os.environ.get("PORT", 8080))
web.run_app(app, host="0.0.0.0", port=port)
