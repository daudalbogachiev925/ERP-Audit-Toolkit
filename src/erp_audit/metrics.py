"""Метрики BSL-кода (встроенный язык 1С)."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

PROCEDURE_PATTERN = re.compile(r"^\s*(?:Процедура|Функция)\s+", re.MULTILINE)
IF_PATTERN = re.compile(r"\bЕсли\b")
LOOP_PATTERN = re.compile(r"\bЦикл\b")
TRY_PATTERN = re.compile(r"\bПопытка\b")


@dataclass
class BslMetrics:
    """Метрики одного BSL-файла."""

    path: Path
    total_lines: int = 0
    code_lines: int = 0
    comment_lines: int = 0
    procedures: int = 0
    if_count: int = 0
    loop_count: int = 0
    try_count: int = 0
    max_nesting: int = 0

    @property
    def complexity(self) -> int:
        """Простая оценка цикломатической сложности."""
        return self.if_count * 2 + self.loop_count * 3 + self.try_count * 2

    @property
    def complexity_level(self) -> str:
        """Уровень сложности для отчёта."""
        c = self.complexity
        if c > 500:
            return "high"
        if c > 100:
            return "medium"
        return "low"


def _count_nesting(text: str) -> int:
    """Оценка максимальной вложенности по отступам."""
    max_indent = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        stripped = line.lstrip("\t ")
        indent = len(line) - len(stripped)
        max_indent = max(max_indent, indent)
    return max_indent // 4


def analyze_bsl_file(path: Path) -> BslMetrics:
    """Анализирует один BSL-файл."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return BslMetrics(path=path)

    lines = text.splitlines()
    comment_lines = sum(1 for line in lines if line.strip().startswith("//"))

    return BslMetrics(
        path=path,
        total_lines=len(lines),
        code_lines=len(lines) - comment_lines,
        comment_lines=comment_lines,
        procedures=len(PROCEDURE_PATTERN.findall(text)),
        if_count=len(IF_PATTERN.findall(text)),
        loop_count=len(LOOP_PATTERN.findall(text)),
        try_count=len(TRY_PATTERN.findall(text)),
        max_nesting=_count_nesting(text),
    )


def analyze_all_bsl(config_dir: Path) -> list[BslMetrics]:
    """Анализирует все BSL-файлы в директории."""
    return [analyze_bsl_file(p) for p in config_dir.rglob("*.bsl")]
