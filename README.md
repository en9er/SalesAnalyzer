
# Sales Analyzer

Простой REST API сервис для анализа продаж ресторана, реализованный на FastAPI.

---

# Возможности

- Анализ списка продаж за день
- Расчёт:
  - общей выручки (`total_revenue`)
  - общей маржи (`total_margin`)
  - маржинальности блюд
- Определение:
  - топ-3 блюд по маржинальности
  - low-margin блюд (`margin < 30%`)
- Генерация бизнес-рекомендаций
- Валидация входных данных через Pydantic
- Dependency Injection через FastAPI Depends
- Docker-ready инфраструктура
- Poetry для управления зависимостями

---

# Архитектура проекта

```text
sales_analyzer/
├── core/               # Бизнес-логика и вычисления
├── web/                # FastAPI API слой
├── infrastructure/     # Инфраструктурная часть + конфигурация
```

## Основные компоненты

### `core/calculator.py`

Содержит чистые функции для вычислений:

- `calculate_revenue`
- `calculate_cost`
- `calculate_margin`

### `web/services/sales_analyzer.py`

Главный сервис анализа продаж:

- расчёт маржинальности
- поиск low-margin блюд
- расчёт total revenue
- расчёт total margin
- сортировка блюд

### `web/services/suggestions.py`

Сервис генерации бизнес-рекомендаций.

Примеры рекомендаций:

- `"Увеличить цену на Цезарь с курицей"`
- `"Маргарита продаётся хорошо - можно добавить в рекомендации"`

### `web/api/v1/sales_analyzer.py`

REST endpoint:

```http
POST /analyze_sales
```

---

# Endpoint

## POST `/analyze_sales`

Принимает JSON со списком продаж.

## Пример запроса

```json
{
  "sales": [
    {
      "dish": "Паста Карбонара",
      "cost_price": 180,
      "selling_price": 450,
      "quantity": 12
    },
    {
      "dish": "Цезарь с курицей",
      "cost_price": 140,
      "selling_price": 390,
      "quantity": 8
    },
    {
      "dish": "Маргарита",
      "cost_price": 90,
      "selling_price": 320,
      "quantity": 25
    }
  ]
}
```

---

# Пример ответа

```json
{
  "top_margin_dishes": [
    ["Маргарита", 71.875],
    ["Цезарь с курицей", 64.10],
    ["Паста Карбонара", 60.0]
  ],
  "loss_making": [],
  "total_revenue": 15220,
  "total_margin": 10620,
  "suggestions": [
    "Маргарита продаётся хорошо - можно добавить в рекомендации"
  ]
}
```

---

# Формулы

## Revenue

```text
Revenue = Σ(selling_price × quantity)
```

## Total Cost

```text
Cost = Σ(cost_price × quantity)
```

## Margin %

```text
Margin % = ((selling_price - cost_price) / selling_price) × 100
```

## Total Margin

```text
Total Margin = Revenue - Cost
```

---

# Используемые технологии

- Python 3
- FastAPI
- Pydantic
- Poetry
- Docker
- Uvicorn

---

# Запуск проекта

## 1. Клонирование репозитория

```bash
git clone https://github.com/your-username/SalesAnalyzer.git
```

```bash
cd SalesAnalyzer
```

---

# Запуск через Poetry

## 1. Виртуальное окружение. Установка Poetry

```bash
python -m venv .venv
source .venv/bin/activate
pip install poetry=="1.8.5"
```

## 2. Установка зависимостей

```bash
poetry install
```

## 3. Запуск сервера

```bash
uvicorn sales_analyzer.web.main:fastapi_app --reload
```

---

# Запуск через Docker

## Сборка и запуск контейнера

```bash
docker compose up --build
```

---

# Swagger документация

После запуска документация доступна по адресу:

```text
http://localhost:8000/docs
```

---

# Особенности реализации

## Оптимизация поиска low-margin блюд

Список блюд предварительно сортируется по маржинальности.

После нахождения первого блюда с маржой ниже порога (`30%`) возвращается весь оставшийся массив без дополнительных проверок:

```python
if margin < LOSS_MAKING_MARGIN_THRESHOLD:
    return dish_margin_info[i:]
```

Сложность:

- сортировка: `O(n log n)`
- поиск low-margin: `O(k)`

---

# Возможные улучшения

- Добавить базу данных
- Добавить авторизацию
- История аналитики
- Аналитика по дням / неделям
- Графики и dashboard
- Асинхронная обработка
- Кэширование
- ML-рекомендации для ценообразования

---

# Почему FastAPI

Для реализации был выбран FastAPI, так как он предоставляет:

- высокую производительность
- автоматическую OpenAPI документацию
- удобную валидацию через Pydantic
- встроенный Dependency Injection
- хорошую масштабируемость для микросервисной архитектуры

---

# Результат

Сервис реализует полноценный pipeline анализа продаж:

1. Приём продаж
2. Валидация данных
3. Расчёт бизнес-метрик
4. Поиск проблемных позиций
5. Генерация рекомендаций
6. Возврат аналитики через REST API
