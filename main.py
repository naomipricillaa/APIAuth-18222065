from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from app.routes import auth
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Register routes
app.include_router(auth.router, prefix="/auth", tags=["auth"])

# Add template directory
templates = Jinja2Templates(directory="templates")

@app.get("/login", response_class=HTMLResponse)
def show_login_page(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
