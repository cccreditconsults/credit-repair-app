from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Repair API", version="0.1.0")

# Allow your Vercel site to call the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # for quick testing; tighten later to your Vercel domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...), bureau: str = "TransUnion"):
    # Minimal stub so the frontend works
    data = await pdf.read()
    return {
        "report_id": "demo",
        "violations": [],
        "normalized": {"bureau": bureau, "bytes_received": len(data)}
    }
