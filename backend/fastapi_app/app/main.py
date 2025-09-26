from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://YOUR-APP.vercel.app",   # <-- your real Vercel URL
    "http://localhost:3000"          # optional for local dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET","POST","OPTIONS"],
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
