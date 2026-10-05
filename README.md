# ERP Audit Toolkit

Комплексный аудит конфигурации 1С:ERP за минуты.

[![CI](https://github.com/USERNAME/erp-audit-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/USERNAME/erp-audit-toolkit/actions)
[![Python](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Проблема

Перед доработкой 1С:ERP нужно понять, что внутри: сколько объектов, где связанность, какие модули сложные, где узкие места. Ручной аудит занимает дни.

## Решение

Инструмент парсит выгрузку конфигурации (XML + BSL), строит граф зависимостей, считает метрики, генерирует HTML-отчёт.

## Возможности

- Парсинг метаданных из выгрузки Конфигуратора.
- Граф зависимостей между объектами (NetworkX).
- Поиск хабов, сирот, циклических зависимостей.
- BSL-метрики: строки, процедуры, вложенность, сложность.
- Оценка трудозатрат на ревью.
- HTML-отчёт с графиками.
- CLI-интерфейс.

## Установка

```bash
pip install erp-audit-toolkit
```

Для разработки:

```bash
git clone https://github.com/USERNAME/erp-audit-toolkit
cd erp-audit-toolkit
pip install -e ".[dev]"
```

## Использование

### Базовый запуск

```bash
erp-audit --input config_dump/ --output report.html
```

Где `config_dump/` — это папка с выгрузкой конфигурации (Конфигуратор → «Выгрузить конфигурацию в файлы»).

### С параметрами

```bash
erp-audit --input config_dump/ --output report.html --top 30 --verbose
```

Опции:

| Опция | Описание | По умолчанию |
|-------|----------|--------------|
| `--input, -i` | Путь к выгрузке конфигурации | обязательный |
| `--output, -o` | Путь для HTML-отчёта | `report.html` |
| `--top, -t` | Сколько топ-объектов показать | `20` |
| `--verbose, -v` | Подробный вывод | `false` |

### Пример вывода

```
ERP Audit Toolkit
Вход: config_dump/
Выход: report.html

✓ Готово

Объектов метаданных: 1247
Связей: 3891
BSL-файлов: 412
Строк кода: 187 543
Сирот: 23
Циклов: 4

Отчёт: report.html
```

## Скриншот

![report](docs/screenshot.png)

*Отчёт содержит: сводные метрики, распределение объектов по типам (pie chart), топ связанных объектов, список сирот, найденные циклы, топ-30 самых больших BSL-модулей с оценкой сложности.*

## Архитектура

```
┌──────────────────┐
│  config_dump/    │  ← выгрузка конфигурации 1С
│  (XML + BSL)     │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│  parser.py       │  ← парсинг XML-метаданных
│                  │
└────────┬─────────┘
         │
         ├──────────────┬───────────────┐
         ▼              ▼               ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│  graph.py    │ │  metrics.py  │ │  report.py   │
│  NetworkX    │ │  BSL-анализ  │ │  Jinja2 +    │
│              │ │              │ │  Plotly      │
└──────┬───────┘ └──────┬───────┘ └──────┬───────┘
       │                │                │
       └────────────────┴────────────────┘
                        │
                        ▼
                ┌──────────────┐
                │ report.html  │
                └──────────────┘
```

### Модули

| Файл | Ответственность |
|------|-----------------|
| `src/erp_audit/parser.py` | Парсинг XML-файлов метаданных |
| `src/erp_audit/graph.py` | Построение и анализ графа зависимостей |
| `src/erp_audit/metrics.py` | Метрики BSL-модулей |
| `src/erp_audit/report.py` | Генерация HTML-отчёта |
| `src/erp_audit/cli.py` | CLI-интерфейс |

## Разработка

### Требования

- Python 3.10+
- pip

### Установка для разработки

```bash
git clone https://github.com/USERNAME/erp-audit-toolkit
cd erp-audit-toolkit
pip install -e ".[dev]"
```

### Команды

```bash
make install     # установка без dev-зависимостей
make dev         # установка с dev-зависимостями
make test        # запуск тестов с покрытием
make lint        # ruff + mypy
make format      # black + ruff --fix
make clean       # очистка кэшей
make build       # сборка пакета
```

### Запуск тестов

```bash
pytest tests/ -v
```

С покрытием:

```bash
pytest tests/ --cov=erp_audit --cov-report=html
```

### Структура проекта

```
erp-audit-toolkit/
├── README.md
├── LICENSE
├── pyproject.toml
├── requirements.txt
├── Makefile
├── .gitignore
├── .github/
│   └── workflows/
│       └── ci.yml
├── src/
│   └── erp_audit/
│       ├── __init__.py
│       ├── parser.py
│       ├── graph.py
│       ├── metrics.py
│       ├── report.py
│       ├── cli.py
│       └── templates/
│           └── report.html
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_parser.py
│   ├── test_graph.py
│   ├── test_metrics.py
│   └── fixtures/
│       └── config_sample/
└── docs/
    └── screenshot.png
```

## CI

При каждом push в `main` и в pull request:

- Линтинг (ruff).
- Проверка форматирования (black).
- Типизация (mypy).
- Тесты (pytest) на Python 3.10, 3.11, 3.12.

## Лицензия

MIT — см. [LICENSE](LICENSE).

## Контакты

- Автор: Your Name
- Email: you@example.com
- LinkedIn: [your-profile](https://linkedin.com/in/your-profile)
