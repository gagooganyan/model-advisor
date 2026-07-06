"""
Fetch latest model benchmarks and pricing from OpenRouter API.
Usage: python data/update.py
Requires: OPENROUTER_API_KEY env var
"""
import json
import os
import urllib.request

API_URL = "https://openrouter.ai/api/v1/models"
OUTPUT_FILE = os.path.join(os.path.dirname(__file__), "models.json")

def fetch_models():
    req = urllib.request.Request(API_URL)
    if os.environ.get("OPENROUTER_API_KEY"):
        req.add_header("Authorization", f"Bearer {os.environ['OPENROUTER_API_KEY']}")
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)["data"]

def extract_benchmarks(models):
    """Extract top models with confirmed benchmarks."""
    scored = []
    free = []
    
    for m in models:
        b = m.get("benchmarks", {})
        aa = b.get("artificial_analysis", {})
        coding = aa.get("coding_index") or 0
        intelligence = aa.get("intelligence_index") or 0
        agentic = aa.get("agentic_index") or 0
        
        da = b.get("design_arena", [])
        code_elo = 0
        for e in da:
            if e.get("category") == "codecategories":
                code_elo = e.get("elo", 0)
        
        pricing = m.get("pricing", {})
        prompt_price = float(pricing.get("prompt", "0")) * 1_000_000
        completion_price = float(pricing.get("completion", "0")) * 1_000_000
        
        ctx = m.get("context_length", 0) // 1024
        mod = m.get("architecture", {}).get("modality", "")
        
        total = coding + intelligence + agentic
        
        entry = {
            "id": m["id"],
            "name": m.get("name", ""),
            "coding_index": coding,
            "intelligence_index": intelligence,
            "agentic_index": agentic,
            "code_elo": code_elo,
            "total_score": total,
            "context_k": ctx,
            "modality": mod,
            "prompt_price_per_m": round(prompt_price, 2),
            "completion_price_per_m": round(completion_price, 2),
        }
        
        if total > 0:
            scored.append(entry)
        
        if m["id"].endswith(":free") or (prompt_price == 0 and completion_price == 0):
            free.append(entry)
    
    scored.sort(key=lambda x: (x["total_score"], x["code_elo"]), reverse=True)
    free.sort(key=lambda x: (x["coding_index"], x["code_elo"]), reverse=True)
    
    return {
        "updated_at": "",
        "top_models": scored[:15],
        "free_models": [f for f in free if f["coding_index"] > 0 or f["code_elo"] > 0][:10],
        "total_models_indexed": len(scored),
    }

if __name__ == "__main__":
    import datetime
    print("Fetching models from OpenRouter...")
    models = fetch_models()
    data = extract_benchmarks(models)
    data["updated_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    # Detect new/changed models
    old_ids = set()
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            old = json.load(f)
            old_ids = {m["id"] for m in old.get("top_models", [])}
    
    new_ids = {m["id"] for m in data["top_models"]}
    dropped = old_ids - new_ids
    entered = new_ids - old_ids
    
    if entered:
        print(f"\n🆕 NEW MODELS: {', '.join(entered)}")
    if dropped:
        print(f"⬇️  DROPPED: {', '.join(dropped)}")
    
    # Price changes
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE) as f:
            old = json.load(f)
            old_prices = {m["id"]: (m["prompt_price_per_m"], m["completion_price_per_m"]) 
                         for m in old.get("top_models", [])}
            for m in data["top_models"]:
                old_p = old_prices.get(m["id"])
                if old_p and (old_p[0] != m["prompt_price_per_m"] or old_p[1] != m["completion_price_per_m"]):
                    print(f"💰 PRICE CHANGE: {m['id']} ${old_p[0]:.2f}/${old_p[1]:.2f} → ${m['prompt_price_per_m']:.2f}/${m['completion_price_per_m']:.2f}")
    
    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    
    print(f"\nUpdated {len(data['top_models'])} top models + {len(data['free_models'])} free models")
    print(f"Total indexed: {data['total_models_indexed']}")
