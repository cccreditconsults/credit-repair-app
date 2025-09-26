def normalize_report(text: str, bureau: str = "TransUnion"):
    """
    Heuristic TU parser:
    - Only accept blocks that contain money or dates
    - Require a short 'Status' (avoid long boilerplate)
    - Look for common TU field labels
    """
    import re, uuid

    def has_money_or_dates(s):
        return bool(re.search(r"\$?\d{2,3}(?:[,\d]{0,3})*(?:\.\d{2})?", s)) or bool(
            re.search(r"\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}-\d{2}-\d{2}\b", s)
        )

    def short_status(s):
        # accept statuses up to ~60 chars; reject the long “represents the current status…” boilerplate
        return s and len(s.strip()) <= 60

    tradelines = []
    # Split into candidate blocks by double newlines
    for blk in re.split(r"\n{2,}", text):
        b = blk.strip()

        # Skip glossary / boilerplate / headers
        if len(b) < 60: 
            continue
        if not has_money_or_dates(b):
            continue
        if "represents the current status" in b.lower():
            continue

        # Try to extract fields using common TU labels
        furnisher = _grab(r"(?i)(Account Name|Creditor|Company|Furnisher)[:\s]+(.+)", b)
        status    = _grab(r"(?i)(Payment Status|Status)[:\s]+(.+)", b)
        opened    = _date(_grab(r"(?i)(Opened|Date Opened)[:\s]+(.+)", b))
        dlp       = _date(_grab(r"(?i)(Date Last Payment)[:\s]+(.+)", b))
        dla       = _date(_grab(r"(?i)(Date Last Active)[:\s]+(.+)", b))
        dofd      = _date(_grab(r"(?i)(Date of First Delinquency|DOFD)[:\s]+(.+)", b))
        balance   = _num(_grab(r"(?i)(Balance|Current Balance)[:\s\$]+([0-9,.\-]+)", b, group=2))
        highcred  = _num(_grab(r"(?i)(High\s*Credit|Credit Limit|High Balance)[:\s\$]+([0-9,.\-]+)", b, group=2))
        acct_last4= _grab(r"(?i)(Account Number)[^\d]*(\d{3,4})", b, group=2)

        # Must have at least furnisher + a status or a balance/date to count
        if not furnisher and not balance and not status:
            continue
        if status and not short_status(status):
            # reject long paragraphs mistakenly captured as status
            status = None

        tradelines.append({
            "id": str(uuid.uuid4()),
            "furnisher": (furnisher or "Unknown").strip(),
            "account_number_hash": ("last4_" + acct_last4) if acct_last4 else None,
            "status": (status or "Unknown").strip(),
            "opened_date": opened,
            "dofd": dofd,
            "dla": dla,
            "dlp": dlp,
            "balan
