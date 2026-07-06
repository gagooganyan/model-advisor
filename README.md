# 🤖 Model Advisor — умный выбор AI-модели под задачу

[![Agent Skills](https://img.shields.io/badge/Agent_Skills-Compatible-6e3bf0?logo=robot)](https://agentskills.io)
[![Platforms](https://img.shields.io/badge/Platforms-41-blue)](https://agentskills.io/clients)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Stars](https://img.shields.io/github/stars/gagooganyan/model-advisor?style=social)](https://github.com/gagooganyan/model-advisor)

**Agent Skill для AI: после получения ТЗ рекомендует оптимальные модели, считает стоимость и даёт полностью бесплатный вариант.**

> ⚡ Работает в **41 среде**: Claude Code, VS Code Copilot, Cursor, OpenCode, Codex CLI, Gemini CLI, Cursor, Windsurf, Terminal-агенты, Cloud-платформы.

---

## 🎯 Что делает

Вы описываете задачу — Model Advisor выдаёт:

| Этап | Модель | Почему | Стоимость |
|------|--------|--------|-----------|
| Архитектура | Claude Opus 4.8 | Intel 55.7 — лучшая логика | $0.42 |
| Код | GLM 5.2 | Code ELO 1360 — №1 | $0.07 |
| Отладка | DeepSeek V4 Pro | $0.87/M — дёшево | $0.04 |
| **Итого** | | | **$0.53** |

И дополнительно:
- 💎 / ⚖️ / 💰 — три сценария цены
- 🆓 **Бесплатный вариант** на :free моделях OpenRouter
- 🏠 **Локальные модели** для конфиденциальных данных

---

## 📊 Данные — не «воздух»

Все бенчмарки подтверждены реальными тестами, не рейтингами:

| Источник | Что измеряет |
|----------|-------------|
| **Artificial Analysis** | coding_index, intelligence_index, agentic_index — стандартизированные прогоны на тысячах задач |
| **Design Arena Code ELO** | Слепые head-to-head сравнения кода человеком — какой код лайкают чаще |
| **OpenRouter API** | Актуальные цены за 1M токенов напрямую из API |

> ❌ Никаких «мы считаем эту модель топовой». Только ELO-рейтинги, индексы и цены.

---

## 🚀 Установка (30 секунд)

### Claude Code
```bash
npx skills add gagooganyan/model-advisor
# или вручную:
mkdir -p ~/.claude/skills/model-advisor
cp SKILL.md ~/.claude/skills/model-advisor/
```

### OpenCode
```bash
# Добавь в opencode.jsonc:
# "skills": {"paths": ["путь/к/model-advisor"]}
```

### VS Code / GitHub Copilot
```bash
mkdir -p .github/copilot/skills/model-advisor
cp SKILL.md .github/copilot/skills/model-advisor/
```

### Cursor
```bash
mkdir -p .cursor/skills/model-advisor
cp SKILL.md .cursor/skills/model-advisor/
```

### Codex CLI / Gemini CLI / Goose / Mistral Vibe / etc.
```bash
# Везде одинаково — скопируй SKILL.md в skills-директорию:
cp SKILL.md .codex/skills/model-advisor/
```

---

## 📦 Что в репозитории

```
model-advisor/
├── SKILL.md              # Универсальный скилл (41 платформа)
├── data/
│   ├── models.json       # JSON с бенчмарками и ценами
│   ├── update.py         # Автообновление из OpenRouter API
│   └── free_models.json  # Бесплатные модели с тестами
├── .github/
│   └── workflows/
│       └── update.yml    # GitHub Action: автообновление еженедельно
├── README.md             # Этот файл
├── README.ru.md          # Русская версия
├── CONTRIBUTING.md       # Как помочь проекту
├── CHANGELOG.md          # История изменений
└── LICENSE               # MIT
```

---

## 🔄 Автообновление данных

Бенчмарки и цены обновляются **автоматически каждую неделю** через GitHub Actions:

```yaml
name: Update Model Data
on:
  schedule:
    - cron: '0 0 * * 1'  # Каждый понедельник
  workflow_dispatch:       # Ручной запуск
```

Запусти вручную: `python data/update.py` (требует API-ключ OpenRouter)

---

## 📈 Сравнение с аналогами

| Функция | Model Advisor | Chat-based выбор | Гугл «какая модель лучше» |
|---------|:---:|:---:|:---:|
| Реальные бенчмарки | ✅ Artificial Analysis + ELO | ❌ мнение модели | ❌ блоги 2024 года |
| Точная стоимость в $ | ✅ по токенам | ❌ | ❌ |
| Бесплатный вариант | ✅ :free модели | ❌ | ❌ |
| Локальные модели | ✅ Ollama/LM Studio | ❌ | ❌ |
| 41 платформа | ✅ | ❌ | ❌ |
| Автообновление цен | ✅ еженедельно | ❌ | ❌ |

---

## 🤝 Contributing

Принимаем PR! Особенно ценно:
- 🆕 Новые бенчмарки/источники
- 🐛 Исправления в SKILL.md
- 🌍 Переводы инструкций
- 💡 Идеи формата ответа

[CONTRIBUTING.md](CONTRIBUTING.md)

---

## 📜 Лицензия

MIT — используй как хочешь. [LICENSE](LICENSE)

---

## ⭐ Поддержи проект

Поставь звезду, расскажи коллегам, отправь PR. Каждая звезда = один разработчик, который перестал переплачивать за AI.

---

**[GitHub](https://github.com/gagooganyan/model-advisor) · [Issues](https://github.com/gagooganyan/model-advisor/issues) · [Discussions](https://github.com/gagooganyan/model-advisor/discussions)**
