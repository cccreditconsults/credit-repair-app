from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Repair API", version="0.1.0")

# Allow your Vercel site to call the API (tighten allow_origins later)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
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
