# backend/fastapi_app/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List

# ⬇️ Import your simple parser (added earlier in app/pipeline.py)
from .pipeline import extract_pdf_text, normalize_report

# -------------------------------------------------------
# 1) UPDATE THIS with your live Vercel URL (no trailing slash)
#    Example: "https://credit-app.vercel.app"
VERCEL_ORIGIN = "https://YOUR-APP.vercel.app"
ALLOWED_ORIGINS: List[str] = [VERCEL_ORIGIN, "http://localhost:3000"]
# -------------------------------------------------------

app = FastAPI(title="Credit Repair API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,   # tighten CORS to your site
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...), bureau: str = "TransUnion"):
    # Basic validation
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a .pdf file")

    # Read file bytes
    data = await pdf.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    try:
        # Extract raw text and normalize to structured fields
        text = extract_pdf_text(data)
        normalized = normalize_report(text, bureau=bureau)
    except Exception as e:
        # Surface parser errors cleanly to the frontend
        raise HTTPException(status_code=400, detail=f"Parse error: {e}")

    # For now, rules not applied yet -> return empty violations
    return {
        "report_id": "demo",
        "violations": [],
        "normalized": normalized
    }
