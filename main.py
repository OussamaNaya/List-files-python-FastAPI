from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os

app = FastAPI()

# Dossier où les fichiers uploadés seront stockés
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Pour servir les fichiers statiques (les fichiers uploadés)
app.mount("/uploads", StaticFiles(directory=UPLOAD_FOLDER), name="uploads")

# Pour les pages HTML (dashboard)
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=PlainTextResponse)
async def home():
    return "Welcome to the FastAPI server!"


@app.post("/upload-file")
async def upload_file(file: UploadFile = File(...)):
    file_location = os.path.join(UPLOAD_FOLDER, file.filename)

    with open(file_location, "wb") as f:
        f.write(await file.read())

    return JSONResponse(
        content={"message": "Fichier reçu", "filename": file.filename},
        status_code=200
    )


@app.get("/dashboard")
async def dashboard(request: Request):
    files = os.listdir(UPLOAD_FOLDER)
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "files": files}
    )


# Permet de lancer avec python main.py
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)


# uvicorn main:app --reload