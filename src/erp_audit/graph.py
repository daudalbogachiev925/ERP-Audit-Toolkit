"""Построение графа зависимостей между объектами 1С."""

from __future__ import annotations

import re
from pathlib import Path

import networkx as nx

from erp_audit.parser import iter_objects

REF_PATTERN = re.compile(r"<Type>([A-Za-zА-Яа-я]+\.[A-Za-zА-Яа-я_0-9]+)</Type>")


def _extract_references(path: Path) -> list[str]:
    """Извлекает имена объектов, на которые ссылается файл."""
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []

    refs = []
    for match in REF_PATTERN.finditer(text):
        target = match.group(1).split(".", 1)[1]
        refs.append(target)
    return refs


def build_graph(config_dir: Path) -> nx.DiGraph:
    """Строит ориентированный граф зависимостей.

    Args:
        config_dir: корень выгрузки конфигурации.

    Returns:
        nx.DiGraph с узлами и рёбрами.
    """
    objects = list(iter_objects(config_dir))
    names = {obj.name for obj in objects}

    graph = nx.DiGraph()

    for obj in objects:
        graph.add_node(obj.name, type=obj.type, path=str(obj.path))

    for obj in objects:
        for ref in _extract_references(obj.path):
            if ref in names and ref != obj.name:
                graph.add_edge(obj.name, ref)

    return graph


def find_orphans(graph: nx.DiGraph) -> list[str]:
    """Возвращает объекты, на которые никто не ссылается."""
    return [node for node, deg in graph.in_degree() if deg == 0]


def find_cycles(graph: nx.DiGraph, max_length: int = 5) -> list[list[str]]:
    """Возвращает циклические зависимости."""
    cycles = []
    for cycle in nx.simple_cycles(graph):
        if len(cycle) <= max_length:
            cycles.append(cycle)
    return cycles


def top_hubs(graph: nx.DiGraph, k: int = 10) -> list[tuple[str, int]]:
    """Топ-k узлов по количеству входящих ссылок."""
    return sorted(graph.in_degree(), key=lambda x: -x[1])[:k]


def subgraph_around(graph: nx.DiGraph, node: str, depth: int = 2) -> nx.DiGraph:
    """Подграф вокруг узла до заданной глубины."""
    if node not in graph:
        return nx.DiGraph()

    nodes = {node}
    frontier = {node}
    for _ in range(depth):
        next_frontier = set()
        for n in frontier:
            next_frontier.update(graph.successors(n))
            next_frontier.update(graph.predecessors(n))
        nodes |= next_frontier
        frontier = next_frontier - nodes

    return graph.subgraph(nodes).copy()
