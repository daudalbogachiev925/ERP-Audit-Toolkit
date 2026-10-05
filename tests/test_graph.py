"""Тесты графа зависимостей."""

from pathlib import Path

from erp_audit.graph import build_graph, find_cycles, find_orphans, top_hubs

FIXTURES = Path(__file__).parent / "fixtures" / "config_sample"


def test_build_graph_has_nodes():
    graph = build_graph(FIXTURES)

    assert graph.number_of_nodes() >= 2
    assert "Контрагенты" in graph.nodes
    assert "РеализацияТоваров" in graph.nodes


def test_build_graph_has_edges():
    graph = build_graph(FIXTURES)

    assert graph.number_of_edges() >= 1
    assert graph.has_edge("РеализацияТоваров", "Контрагенты")


def test_find_orphans():
    graph = build_graph(FIXTURES)
    orphans = find_orphans(graph)

    assert "РеализацияТоваров" in orphans
    assert "Контрагенты" not in orphans


def test_top_hubs():
    graph = build_graph(FIXTURES)
    hubs = top_hubs(graph, k=5)

    assert len(hubs) >= 1
    names = [n for n, _ in hubs]
    assert "Контрагенты" in names


def test_find_cycles_empty():
    graph = build_graph(FIXTURES)
    cycles = find_cycles(graph, max_length=4)

    assert isinstance(cycles, list)
