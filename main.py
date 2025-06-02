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

# 1. Point to your dist directory (where index.html, assets/, and _redirects live).
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DIST_DIR = os.path.join(BASE_DIR, "dist")

# 2. Mount the entire dist folder at "/" so:
#    • "/index.html" → dist/index.html
#    • "/assets/... " → dist/assets/...
#    • "/_redirects" → dist/_redirects
#    • any other path (e.g. "/dashboard") not found in dist/ serves index.html
app.mount(
    "/",
    StaticFiles(directory=DIST_DIR, html=True),
    name="static",
)