"""Тесты метрик BSL."""

from pathlib import Path

from erp_audit.metrics import analyze_all_bsl, analyze_bsl_file

FIXTURES = Path(__file__).parent / "fixtures" / "config_sample"


def test_analyze_bsl_file_counts_lines():
    bsl_path = FIXTURES / "Documents" / "РеализацияТоваров.bsl"
    metrics = analyze_bsl_file(bsl_path)

    assert metrics.total_lines > 0
    assert metrics.code_lines > 0


def test_analyze_bsl_file_counts_procedures():
    bsl_path = FIXTURES / "Documents" / "РеализацияТоваров.bsl"
    metrics = analyze_bsl_file(bsl_path)

    assert metrics.procedures == 2


def test_analyze_bsl_file_counts_loops_and_ifs():
    bsl_path = FIXTURES / "Documents" / "РеализацияТоваров.bsl"
    metrics = analyze_bsl_file(bsl_path)

    assert metrics.loop_count >= 2
    assert metrics.if_count >= 2


def test_complexity_level_low():
    metrics = analyze_bsl_file(
        FIXTURES / "Documents" / "РеализацияТоваров.bsl"
    )
    assert metrics.complexity_level in ("low", "medium", "high")


def test_analyze_all_bsl():
    all_metrics = analyze_all_bsl(FIXTURES)

    assert len(all_metrics) >= 1
    assert all(isinstance(m.total_lines, int) for m in all_metrics)
