import os
from app import create_app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    debug = os.getenv("FLASK_DEBUG", "True") == "True"

    print("Server Flask sedang berjalan...")
    app.run(host="0.0.0.0", port=port, debug=debug)
