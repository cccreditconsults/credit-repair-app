# backend/fastapi_app/app/main.py
from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# If you added pipeline.py earlier, keep these imports.
# If not, you can comment them out temporarily.
try:
    from .pipeline import extract_pdf_text, normalize_report
except Exception:
    extract_pdf_text = None
    normalize_report = None

# --- Create the app FIRST (before any @app.route decorators) ---
app = FastAPI(title="Credit Repair API", version="0.1.0")

# --- CORS (open for troubleshooting; tighten later to your Vercel URL) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # e.g., ["https://your-app.vercel.app", "http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Routes ---
@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...), bureau: str = "TransUnion"):
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a .pdf file")

    data = await pdf.read()
    if not data:
        raise HTTPException(status_code=400, detail="Empty file")

    # If parser is available, use it; otherwise return a stub so the frontend works.
    if extract_pdf_text and normalize_report:
        try:
            text = extract_pdf_text(data)
            normalized = normalize_report(text, bureau=bureau)
        except Exception as e:
            raise HTTPException(status_code=400, detail=f"Parse error: {e}")
    else:
        normalized = {"bureau": bureau, "bytes_received": len(data)}

    return {
        "report_id": "demo",
        "violations": [],
        "normalized": normalized,
    }

from .pipeline import extract_pdf_text, normalize_report
from . import rules
from .db import get_client
from datetime import date, timedelta

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...), bureau: str = "TransUnion"):
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a .pdf file")
    data = await pdf.read()
    text = extract_pdf_text(data)
    normalized = normalize_report(text, bureau=bureau)
    violations = rules.run(normalized)

    sb = get_client()
    # store normalized JSON
    ins = sb.table("reports").insert({
        "bureau": bureau,
        "parsed_json": normalized
    }).execute()

    report_id = ins.data[0]["id"] if ins.data else "demo"
    return {"report_id": report_id, "violations": violations, "normalized": normalized}
