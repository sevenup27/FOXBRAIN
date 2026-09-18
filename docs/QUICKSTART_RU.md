# FOXBRAIN — быстрый старт

## 1. Запуск

В папке проекта:

```bash
python app.py
```

Windows:

```bash
py -3 app.py
```

Открой:

http://127.0.0.1:8000

## 2. Проверка

В отдельном терминале:

```bash
python -m unittest discover -s tests -v
```

## 3. GitHub

```bash
git init
git add .
git commit -m "Initial FOXBRAIN observation terminal"
git branch -M main
git remote add origin YOUR_REPOSITORY_URL
git push -u origin main
```

## 4. Что важно

- Showcase-режим работает локально без API-ключей.
- Сигналы BUY / SELL / WAIT являются базовыми наблюдательными сигналами.
- Сделки автоматически не выполняются.
- `data/` не нужно публиковать.
- Для live-режима сначала нужно проверить конкретную пару и сеть.
