# Mirrored file from app.py to support existing run scripts
from app import app

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
