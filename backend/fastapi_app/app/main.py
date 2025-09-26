from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Credit Repair API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow all for testing; lock to Vercel domain later
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/health")
def health():
    return {"status":"ok"}

@app.post("/upload-report")
async def upload_report(pdf: UploadFile = File(...)):
    data = await pdf.read()
    return {
        "report_id": "demo",
        "violations": [],
        "normalized": {"bytes_received": len(data)}
    }
