from fastapi import FastAPI, UploadFile, File, HTTPException

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...)):
    if not pdf.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=415, detail="Please upload a .pdf file")
    data = await pdf.read()
    return {"report_id":"demo","violations":[],"normalized":{"bytes_received":len(data)}}

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://YOUR-APP.vercel.app",  # <-- your actual Vercel site
    "http://localhost:3000"
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
    # Stub response so frontend works
    return {
        "report_id": "demo",
        "violations": [],
        "normalized": {"bureau": bureau, "bytes_received": len(data)}
    }
VERCEL_ORIGIN = "https://<your-app>.vercel.app"  # your actual site URL
ALLOWED_ORIGINS = [VERCEL_ORIGIN, "http://localhost:3000"]
