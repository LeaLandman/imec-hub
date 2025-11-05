
#!/usr/bin/env python3
import os, time, requests

API_BASE = os.getenv("API_BASE", "http://localhost:8000")
API_KEY = os.getenv("API_KEY", "devapikey")

def post(path, payload):
    url = f"{API_BASE}{path}"
    r = requests.post(url, json=payload, headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"}, timeout=30)
    r.raise_for_status()
    return r.json()

def run():
    legal = {
        "id": f"li_seed_{int(time.time())}",
        "title": "Rail Interoperability Regulation",
        "instrument_type": "regulation",
        "country_id": "IL",
        "source_id": "src_il_oj_20250412",
        "status": "adopted",
        "adoption_date": "2025-04-12",
        "segments": ["rail","data"],
        "topics": ["standards","safety"],
        "summary_fr": "Règlement d'interopérabilité ferroviaire (Israël).",
        "summary_en": "Rail interoperability regulation (Israel).",
        "summary_ar": "لائحة قابلية التشغيل البيني للسكك الحديدية (إسرائيل).",
        "credibility_score": 0.8
    }
    print(post("/legal", legal))

    budget = {
        "id": f"bud_seed_{int(time.time())}",
        "amount_original": 500000000,
        "currency": "USD",
        "date": "2025-09-01",
        "segment": "port",
        "countries_involved": ["AE"],
        "source_id": "src_ae_oj_20250320",
        "summary_fr": "Capex portuaire lié à IMEC (EAU).",
        "summary_en": "Port capex related to IMEC (UAE).",
        "summary_ar": "إنفاق رأسمالي للموانئ مرتبط بـ IMEC (الإمارات).",
        "credibility_score": 0.82
    }
    print(post("/budgets", budget))

if __name__ == "__main__":
    run()
