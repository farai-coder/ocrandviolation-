
from fastapi import FastAPI, File, UploadFile, Form, Depends
from fastapi.responses import JSONResponse
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import io
import datetime
from models import Violation
from fastapi import APIRouter
from database import SessionLocal
from sqlalchemy.orm import Session
# Load OCR model and processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-printed")



def get_db():
    """
    Dependency override to get a SQLAlchemy session.
    Remember to close it at the end.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
router = APIRouter()    

@router.post("/")
async def perform_ocr(
    image: UploadFile = File(...),
    timestamp: str = Form(...),
    lane_id: int = Form(..., description="ID of the lane where the violation occurred"),
    db: Session = Depends(get_db) 
):
    if image.content_type != "image/jpeg":
        return JSONResponse(status_code=400, content={"error": "Only JPG images are allowed."})

    contents = await image.read()
    image_pil = Image.open(io.BytesIO(contents)).convert("RGB")

    # Run OCR
    pixel_values = processor(images=image_pil, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Save the violation record
    violation = Violation(
        timestamp=datetime.datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"),
        pictures=contents,
        license_plate=extracted_text,
        lane_id=lane_id  # Assuming lane_id is fixed for this example
    )
    
    db.add(violation)
    db.commit()
    
    return {"message": "OCR complete"}


@router.get("/")
async def get_all_violations(db: Session = Depends(get_db)):
    violations = db.query(Violation).all()
    return violations

