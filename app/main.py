from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from app.routes import auth
from fastapi.templating import Jinja2Templates
from pathlib import Path
import uvicorn

app = FastAPI()

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Add template directory
BASE_DIR = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Login route
@app.get("/login", response_class=HTMLResponse)
def show_login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Run the app (local development only)
if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)
