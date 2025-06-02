from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import JSONResponse
from PIL import Image
from transformers import TrOCRProcessor, VisionEncoderDecoderModel
import io
import datetime

app = FastAPI()

# Load OCR model and processor
processor = TrOCRProcessor.from_pretrained("microsoft/trocr-small-printed")
model = VisionEncoderDecoderModel.from_pretrained("microsoft/trocr-small-printed")

# Store the OCR results in memory (in real apps, use a database)
ocr_results = []

@app.post("/ocr/")
async def perform_ocr(
    image: UploadFile = File(...),
    timestamp: str = Form(...)
):
    if image.content_type != "image/jpeg":
        return JSONResponse(status_code=400, content={"error": "Only JPG images are allowed."})

    contents = await image.read()
    image_pil = Image.open(io.BytesIO(contents)).convert("RGB")

    # Run OCR
    pixel_values = processor(images=image_pil, return_tensors="pt").pixel_values
    generated_ids = model.generate(pixel_values)
    extracted_text = processor.batch_decode(generated_ids, skip_special_tokens=True)[0]

    # Save result
    ocr_result = {
        "timestamp": timestamp,
        "text": extracted_text
    }
    ocr_results.append(ocr_result)

    return {"message": "OCR complete", "text": extracted_text}


@app.get("/texts/")
async def get_texts():
    return ocr_results
