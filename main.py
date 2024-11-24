from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.routes import auth
from fastapi.templating import Jinja2Templates
import uvicorn

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Registrasi route dari auth
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Inisialisasi direktori template
templates = Jinja2Templates(directory="app/templates")  

# Route untuk halaman login
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})