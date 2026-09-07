import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route("/")
def home():
    return "Running"

def run():
    try:
        import src.main
    except Exception:
        import traceback
        traceback.print_exc()

t = Thread(target=run, daemon=True)
t.start()

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))

    app.run(host="0.0.0.0", port=port)