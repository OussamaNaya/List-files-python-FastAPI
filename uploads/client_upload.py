import os
import requests

# URL de ton serveur FastAPI
SERVER_URL = "http://127.0.0.1:8000/upload-file"

def send_file(path):
    with open(path, "rb") as f:
        files = {"file": (os.path.basename(path), f)}
        response = requests.post(SERVER_URL, files=files)
        return response.json()

def main():
    folder = "."  # dossier actuel
    files = os.listdir(folder)

    for filename in files:
        path = os.path.join(folder, filename)

        if os.path.isfile(path):
            try:
                result = send_file(path)
                print(f"[OK] {filename} → envoyé")
            except Exception as e:
                print(f"[ERREUR] {filename}: {e}")

if __name__ == "__main__":
    main()
