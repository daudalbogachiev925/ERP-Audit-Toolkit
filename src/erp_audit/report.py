"""Генерация HTML-отчёта."""

from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path

import networkx as nx
from jinja2 import Environment, FileSystemLoader, select_autoescape

from erp_audit.graph import find_cycles, find_orphans, top_hubs
from erp_audit.metrics import BslMetrics


def _serialize_bsl(metrics: list[BslMetrics]) -> list[dict]:
    """Сериализует BSL-метрики для шаблона."""
    return [
        {
            "path": str(m.path),
            "total_lines": m.total_lines,
            "code_lines": m.code_lines,
            "procedures": m.procedures,
            "if_count": m.if_count,
            "loop_count": m.loop_count,
            "complexity": m.complexity,
            "complexity_level": m.complexity_level,
            "max_nesting": m.max_nesting,
        }
        for m in metrics
    ]


def generate_report(
    graph: nx.DiGraph,
    bsl_metrics: list[BslMetrics],
    output_path: Path,
    templates_dir: Path | None = None,
) -> None:
    """Генерирует HTML-отчёт.

    Args:
        graph: граф зависимостей.
        bsl_metrics: список метрик BSL.
        output_path: путь для сохранения HTML.
        templates_dir: директория с Jinja2-шаблонами.
    """
    if templates_dir is None:
        templates_dir = Path(__file__).parent / "templates"

    env = Environment(
        loader=FileSystemLoader(str(templates_dir)),
        autoescape=select_autoescape(["html", "xml"]),
    )
    template = env.get_template("report.html")

    hubs = top_hubs(graph, k=20)
    orphans = find_orphans(graph)
    cycles = find_cycles(graph, max_length=4)

    type_counts: dict[str, int] = {}
    for _, data in graph.nodes(data=True):
        t = data.get("type", "Unknown")
        type_counts[t] = type_counts.get(t, 0) + 1

    total_lines = sum(m.total_lines for m in bsl_metrics)
    total_procedures = sum(m.procedures for m in bsl_metrics)

    html = template.render(
        generated_at=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        total_objects=graph.number_of_nodes(),
        total_edges=graph.number_of_edges(),
        total_bsl_files=len(bsl_metrics),
        total_lines=total_lines,
        total_procedures=total_procedures,
        type_counts=type_counts,
        hubs=hubs,
        orphans=orphans[:50],
        orphans_total=len(orphans),
        cycles=cycles,
        cycles_total=len(cycles),
        bsl_metrics=_serialize_bsl(
            sorted(bsl_metrics, key=lambda m: -m.total_lines)[:30]
        ),
        hubs_json=json.dumps(hubs),
        types_json=json.dumps(type_counts),
    )

    output_path.write_text(html, encoding="utf-8")
