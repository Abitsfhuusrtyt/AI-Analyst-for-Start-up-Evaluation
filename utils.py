import re, textwrap
def snippet(text, start, end, window=90):
    s = max(0, start - window); e = min(len(text), end + window)
    return text[s:e].replace('\n',' ')
def find_metrics(text):
    metrics = []
    pattern = r'(\$?\s?[\d\.,]+(?:\s?[kKmMbB])?)\s*(ARR|MRR|revenue|users|growth|GMV)'
    for m in re.finditer(pattern, text, flags=re.IGNORECASE):
        val, name = m.group(1).strip(), m.group(2).upper()
        metrics.append({"name": name, "value": val, "evidence": snippet(text, m.start(), m.end())})
    return metrics
def risks(text, metrics):
    flags = []
    if re.search(r'\bno competitors?\b', text, flags=re.IGNORECASE):
        span = re.search(r'\bno competitors?\b', text, re.IGNORECASE).span()
        flags.append({"type":"market","message":"Unrealistic 'no competitors' claim","evidence":snippet(text, *span)})
    if not re.search(r'\b(ARR|MRR|gross margin|CAC|LTV)\b', text, flags=re.IGNORECASE):
        flags.append({"type":"finance","message":"Missing unit economics (ARR/MRR, margins, CAC/LTV)","evidence":""})
    arr = None; mrr = None
    for m in metrics:
        if m["name"] == "ARR": arr = m["value"]
        if m["name"] == "MRR": mrr = m["value"]
    def to_num(s):
        s = s.replace('$','').replace(',','').strip().lower()
        mult = 1
        if s.endswith('k'): mult, s = 1_000, s[:-1]
        if s.endswith('m'): mult, s = 1_000_000, s[:-1]
        if s.endswith('b'): mult, s = 1_000_000_000, s[:-1]
        try: return float(s)*mult
        except: return None
    if arr and mrr:
        a = to_num(arr); m = to_num(mrr)
        if a and m and (a < 8*m or a > 20*m):
            flags.append({"type":"inconsistency","message":"ARR not ~12× MRR","evidence":f"ARR={arr}, MRR={mrr}"})
    return flags
def score(weights, metrics, flags):
    base = 60
    traction_bonus = 5 if any(m["name"] in ["ARR","MRR","USERS","REVENUE","GMV"] for m in metrics) else 0
    market_bonus = 0
    penalty = min(20, len(flags)*5)
    subscores = {"team": weights.get("team",25), "market": 25 + market_bonus, "traction": 25 + traction_bonus, "risk_penalty": penalty}
    overall = min(100, base + traction_bonus + market_bonus - penalty)
    return overall, subscores
