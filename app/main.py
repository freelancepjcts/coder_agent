from fastapi import FastAPI, HTTPException, Response
from fastapi.responses import HTMLResponse
from fastapi.exceptions import RequestValidationError
from app.exceptions.handlers import exception_handler
from app.routes import demo_controller, chat_controller

app = FastAPI(title="My App")

# Static files routing using standard Python file reading (requires no extra libraries like aiofiles)
@app.get("/", response_class=HTMLResponse)
def serve_index():
    try:
        with open("app/static/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="index.html not found")

@app.get("/static/style.css")
def serve_css():
    try:
        with open("app/static/style.css", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/css")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="style.css not found")

@app.get("/static/app.js")
def serve_js():
    try:
        with open("app/static/app.js", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="app.js not found")

@app.get("/coder", response_class=HTMLResponse)
def serve_coder_index():
    try:
        with open("app/static/coder.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="coder.html not found")

@app.get("/static/coder_style.css")
def serve_coder_css():
    try:
        with open("app/static/coder_style.css", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="text/css")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="coder_style.css not found")

@app.get("/static/coder_app.js")
def serve_coder_js():
    try:
        with open("app/static/coder_app.js", "r", encoding="utf-8") as f:
            return Response(content=f.read(), media_type="application/javascript")
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="coder_app.js not found")

# Global API prefix
app.include_router(demo_controller.router, prefix="/api")
app.include_router(chat_controller.router, prefix="/api")


app.add_exception_handler(Exception, exception_handler)
app.add_exception_handler(HTTPException, exception_handler)
app.add_exception_handler(RequestValidationError, exception_handler)
