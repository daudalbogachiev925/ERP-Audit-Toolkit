"""CLI интерфейс для ERP Audit Toolkit."""

from __future__ import annotations

from pathlib import Path

import click
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

from erp_audit.graph import build_graph, find_cycles, find_orphans, top_hubs
from erp_audit.metrics import analyze_all_bsl
from erp_audit.report import generate_report

console = Console()


@click.command()
@click.option(
    "--input", "-i",
    "input_dir",
    type=click.Path(exists=True, file_okay=False, path_type=Path),
    required=True,
    help="Путь к выгрузке конфигурации 1С.",
)
@click.option(
    "--output", "-o",
    "output_path",
    type=click.Path(path_type=Path),
    default="report.html",
    help="Путь для сохранения HTML-отчёта.",
)
@click.option(
    "--top", "-t",
    type=int,
    default=20,
    help="Сколько топ-объектов показать.",
)
@click.option(
    "--verbose", "-v",
    is_flag=True,
    help="Подробный вывод.",
)
def main(input_dir: Path, output_path: Path, top: int, verbose: bool) -> None:
    """Аудит конфигурации 1С:ERP."""
    console.print("[bold cyan]ERP Audit Toolkit[/bold cyan]")
    console.print(f"Вход:  [yellow]{input_dir}[/yellow]")
    console.print(f"Выход: [yellow]{output_path}[/yellow]\n")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console,
    ) as progress:
        task = progress.add_task("Парсинг...", total=4)

        progress.update(task, description="Построение графа...")
        graph = build_graph(input_dir)
        progress.advance(task)

        progress.update(task, description="Анализ BSL...")
        bsl_metrics = analyze_all_bsl(input_dir)
        progress.advance(task)

        progress.update(task, description="Поиск сирот и циклов...")
        orphans = find_orphans(graph)
        cycles = find_cycles(graph)
        hubs = top_hubs(graph, k=top)
        progress.advance(task)

        progress.update(task, description="Генерация отчёта...")
        generate_report(graph, bsl_metrics, output_path)
        progress.advance(task)

    console.print()
    console.print("[bold green]✓ Готово[/bold green]\n")

    console.print(f"Объектов метаданных: [cyan]{graph.number_of_nodes()}[/cyan]")
    console.print(f"Связей:              [cyan]{graph.number_of_edges()}[/cyan]")
    console.print(f"BSL-файлов:          [cyan]{len(bsl_metrics)}[/cyan]")
    console.print(f"Строк кода:          [cyan]{sum(m.total_lines for m in bsl_metrics):,}[/cyan]")
    console.print(f"Сирот:               [yellow]{len(orphans)}[/yellow]")
    console.print(f"Циклов:              [red]{len(cycles)}[/red]")

    if verbose and hubs:
        console.print("\n[bold]Топ объектов по связям:[/bold]")
        for name, deg in hubs[:10]:
            console.print(f"  {name}: {deg}")

    console.print(f"\nОтчёт: [bold]{output_path.absolute()}[/bold]")


if __name__ == "__main__":
    main()
