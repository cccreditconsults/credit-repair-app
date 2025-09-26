from pdfminer.high_level import extract_text
from dateutil.parser import parse as dtparse
import re, uuid

def extract_pdf_text(pdf_bytes: bytes) -> str:
    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=True) as f:
        f.write(pdf_bytes); f.flush()
        return extract_text(f.name)

def normalize_report(text: str, bureau: str = "TransUnion"):
    """Very simple, regex-based extractor. Good enough to prove it works; refine later."""
    tradelines = []
    # Split blocks by blank lines and look for common fields
    for blk in re.split(r"\n{2,}", text):
        if re.search(r"(?i)(Company|Creditor|Furnisher)", blk) and re.search(r"(?i)(Status|Charge[-\s]?Off)", blk):
            furnisher = _grab(r"(?i)(Company|Creditor|Furnisher)[:\s]+(.+)", blk)
            status    = _grab(r"(?i)Status[:\s]+(.+)", blk) or ("Charged Off" if re.search(r"(?i)charge[-\s]?off", blk) else "Unknown")
            acct_last4= _grab(r"(?i)Account Number[^\d]*(\d{3,4})", blk)
            opened    = _date(_grab(r"(?i)Opened[:\s]+(.+)", blk))
            dofd      = _date(_grab(r"(?i)(Date of First Delinquency|DOFD)[:\s]+(.+)", blk, group=2))
            dla       = _date(_grab(r"(?i)Date Last Active[:\s]+(.+)", blk))
            dlp       = _date(_grab(r"(?i)Date Last Payment[:\s]+(.+)", blk))
            balance   = _num(_grab(r"(?i)Balance[:\s\$]+([0-9,.\-]+)", blk))
            highcred  = _num(_grab(r"(?i)(High\s*Credit|Credit Limit)[:\s\$]+([0-9,.\-]+)", blk, group=2))

            tradelines.append({
                "id": str(uuid.uuid4()),
                "furnisher": furnisher or "Unknown",
                "account_number_hash": ("last4_" + acct_last4) if acct_last4 else None,
                "status": status,
                "opened_date": opened,
                "dofd": dofd,
                "dla": dla,
                "dlp": dlp,
                "balance": balance,
                "high_credit": highcred,
                "remarks": [],
                "is_open": bool(re.search(r"(?i)\bOpen\b", blk) and not re.search(r"(?i)\bClosed\b", blk)),
                "chargeoff": bool(re.search(r"(?i)charge[-\s]?off", blk)),
            })

    inquiries = []
    for ln in text.splitlines():
        m = re.search(r"(?i)inquiry[:\s]+(.+?)\s+(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})", ln)
        if m:
            inquiries.append({"inquirer": m.group(1).strip(), "type": "hard", "date": _date(m.group(2))})

    return {
        "bureau": bureau,
        "tradelines": tradelines,
        "collections": [],   # add later
        "inquiries": inquiries
    }

def _grab(pat, text, group=2):
    m = re.search(pat, text)
    return m.group(group if m and m.lastindex and m.lastindex >= group else 1) if m else None

def _date(s):
    if not s: return None
    try: return dtparse(s, dayfirst=False, fuzzy=True).date().isoformat()
    except: return None

def _num(s):
    if not s: return None
    try:
        return float(re.sub(r"[^\d.\-]", "", s).replace(",", ""))
    except:
        return None
