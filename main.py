from fastapi import FastAPI
from router import router as violations
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI()

app.include_router(violations, prefix="/violations", tags=["Violations"])

# add CORS middleware 

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

# Serve Static Files (Frontend)
build_path = os.path.join(os.path.dirname(__file__), "build")
app.mount("/static", StaticFiles(directory=os.path.join(build_path, "static")), name="static")

# Serve the index.html at root
@app.get("/{full_path:path}")
async def serve_frontend(full_path: str):
    index_path = os.path.join(build_path, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"error": "index.html not found"}