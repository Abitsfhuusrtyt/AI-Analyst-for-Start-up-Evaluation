# AI-Analyst-for-Start-up-Evaluation

AI Analyst for Startup Evaluation converts messy founder materials into an investor-ready one-pager in minutes. An investor uploads a pitch deck; the system parses the PDF, extracts key signals (ARR/MRR, growth, users), and detects evidence-backed risk flags such as “no competitors” claims or ARR↔MRR inconsistencies. It then computes a transparent, adjustable score and generates a concise deal note with cited snippets and a downloadable file.

The prototype demonstrates the end-to-end flow—upload → extract → risk flags → score → note—implemented as a lightweight Streamlit app. The production design maps to Google Cloud (Cloud Storage, Document AI/Cloud Vision, Vertex/Gemini, BigQuery, Firebase). This approach prioritizes speed, transparency, and reliability: extract-then-reason to reduce hallucinations, explicit citations for every flag, and a clear rubric investors can tune.
Evidence-first risk flags: Every alert includes a cited snippet/slide reference.

Transparent, tunable scoring: Clear rubric with weight sliders; no black-box magic.

Extract-then-reason pipeline: Structured JSON first → fewer hallucinations, faster responses.

Investor-ready in <5 minutes: From upload to downloadable deal note.

Cloud-native & extensible: Easy to plug in Gemini, BigQuery benchmarks, and public data (jobs/news/GitHub).
