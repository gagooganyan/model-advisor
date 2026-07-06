"""
Generate SKILL.md model tables from models.json.
Usage: python data/generate_skill.py

Reads data/models.json → updates SKILL.md tables.
Keeps all non-table content intact.
"""
import json
import os
import re

DATA_FILE = os.path.join(os.path.dirname(__file__), "models.json")
SKILL_FILE = os.path.join(os.path.dirname(__file__), "..", "SKILL.md")

def load_models():
    with open(DATA_FILE) as f:
        return json.load(f)

def build_top15_table(models):
    """Build markdown table for top 15 models."""
    rows = []
    rows.append("| # | Модель | Coding | Intel | Agentic | Code ELO | $/M вход | $/M выход | Контекст | Файлы/картинки |")
    rows.append("|---|--------|--------|-------|---------|----------|----------|-----------|----------|----------------|")
    
    # Modality helper
    def modality_icon(mod):
        if "file" in mod:
            return "✅"
        if "image" in mod and "file" not in mod:
            return "🖼️"
        if "audio" in mod or "video" in mod:
            return "🔊📹"
        return "❌ text"
    
    for i, m in enumerate(models["top_models"][:15], 1):
        rid = m["id"].split("/")[-1]
        pin = m["prompt_price_per_m"]
        pout = m["completion_price_per_m"]
        ctx = m["context_k"]
        mod = m["modality"]
        icon = modality_icon(mod)
        elo = m["code_elo"]
        if elo == 0:
            elo_str = "—"
        else:
            elo_str = f"**{elo}**" if elo >= 1310 else str(elo)
        
        rows.append(
            f"| {i} | {rid} | {m['coding_index']} | {m['intelligence_index']} | "
            f"{m['agentic_index']} | {elo_str} | {pin:.2f} | {pout:.2f} | {ctx}k | {icon} |"
        )
    return "\n".join(rows)

def build_free_table(models):
    """Build markdown table for free models."""
    rows = []
    rows.append("| Модель | Coding | Intel | Code ELO | Контекст | Для чего |")
    rows.append("|--------|--------|-------|----------|----------|----------|")
    
    purpose_map = {
        "nvidia/nemotron-3-ultra": "Лучший бесплатный, сложные задачи",
        "google/gemma-4-31b": "Мультимодал бесплатно",
        "google/gemma-4-26b": "Средние задачи + картинки",
        "nvidia/nemotron-3-super": "Бюджетный кодер",
        "openai/gpt-oss-120b": "OpenAI open-weight",
        "qwen/qwen3-coder": "Чистый код, огромный контекст",
    }
    
    for m in models["free_models"][:10]:
        rid = m["id"].split("/")[-1]
        elo = m["code_elo"] if m["code_elo"] > 0 else "—"
        purpose = "Бесплатная модель"
        for key, val in purpose_map.items():
            if key in m["id"]:
                purpose = val
                break
        
        rows.append(
            f"| {rid} | {m['coding_index']} | {m['intelligence_index']} | "
            f"{elo} | {m['context_k']}k | {purpose} |"
        )
    return "\n".join(rows)

def update_skill_md(top15_table, free_table):
    """Update SKILL.md tables in-place."""
    with open(SKILL_FILE, encoding="utf-8") as f:
        content = f.read()
    
    # Replace top-15 table (between ## ТОП-15 and ## Бесплатные)
    pattern = r"(## ТОП-15.*?\n\n)(\|.*?\n)+\n"
    replacement = f"## ТОП-15 моделей (подтверждённые тесты)\n\n{top15_table}\n\n"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    # Replace free table (between ## Бесплатные and ## Как анализировать)
    pattern = r"(## Бесплатные.*?\n\n)(\|.*?\n)+\n"
    replacement = f"## Бесплатные модели\n\n{free_table}\n\n"
    content = re.sub(pattern, replacement, content, flags=re.DOTALL)
    
    with open(SKILL_FILE, "w", encoding="utf-8") as f:
        f.write(content)
    
    print("SKILL.md tables updated")

if __name__ == "__main__":
    models = load_models()
    top15 = build_top15_table(models)
    free = build_free_table(models)
    update_skill_md(top15, free)
    print(f"Updated at: {models['updated_at']}")
    print(f"Top models: {len(models['top_models'])}")
    print(f"Free models: {len(models['free_models'])}")
