from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.routes import auth, hotels, recommendations
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import uvicorn
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,  # Set the logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    format="%(asctime)s - %(levelname)s - %(message)s",  # Logging format
)
logger = logging.getLogger("main")  # Logger instance

# Inisialisasi aplikasi FastAPI
app = FastAPI()

# Tambahkan mount untuk static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Registrasi route dari auth
app.include_router(auth.router, prefix="/auth", tags=["auth"])
app.include_router(hotels.router, prefix="/api", tags=["hotels"])
app.include_router(recommendations.router, prefix="/api", tags=["recommendations"])

# Inisialisasi direktori template
templates = Jinja2Templates(directory="app/templates")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.get("/search", response_class=HTMLResponse)
async def search_page(request: Request):
    return templates.TemplateResponse("search.html", {"request": request})

@app.get("/recommendations", response_class=HTMLResponse)
async def recommendations_page(request: Request):
    return templates.TemplateResponse("recommendations.html", {"request": request})

@app.get("/home", response_class=HTMLResponse)
async def home_page(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

if __name__ == "__main__":
    logger.info("Starting FastAPI server...")
    uvicorn.run(app, host="127.0.0.1", port=8000)
