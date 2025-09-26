from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from .pipeline import extract_pdf_text, normalize_report  # <-- add this import

app = FastAPI(title="Credit Repair API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # tighten later to your Vercel domain
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...), bureau: str = "TransUnion"):
    data = await pdf.read()
    text = extract_pdf_text(data)
    normalized = normalize_report(text, bureau=bureau)
    # For now, skip rules; just return parsed structure
    return {
        "report_id": "demo",
        "violations": [],           # rules come next
        "normalized": normalized
    }
