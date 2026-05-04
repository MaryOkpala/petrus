from rich.console import Console
from rich.table import Table
from rich import box

MOCK_ENVIRONMENTS = [
    {
        "team": "payments",
        "environment": "dev",
        "type": "web-app",
        "namespace": "payments-dev",
        "status": "Healthy",
        "pods": "3/3",
        "region": "us-east-1",
        "age": "2d"
    },
    {
        "team": "data-science",
        "environment": "staging",
        "type": "ai-ml",
        "namespace": "data-science-staging",
        "status": "Healthy",
        "pods": "2/2",
        "region": "us-east-1",
        "age": "5h"
    },
    {
        "team": "platform",
        "environment": "prod",
        "type": "api",
        "namespace": "platform-prod",
        "status": "Healthy",
        "pods": "4/4",
        "region": "us-east-1",
        "age": "7d"
    }
]

def get_status(team_filter: str, console: Console):
    """Display status of all provisioned environments."""

    environments = MOCK_ENVIRONMENTS
    if team_filter:
        environments = [e for e in environments if e["team"] == team_filter]

    if not environments:
        console.print(f"[yellow]No environments found for team '{team_filter}'.[/yellow]")
        return

    table = Table(
        title="Petrus — environment status",
        box=box.ROUNDED,
        show_header=True,
        header_style="bold blue"
    )

    table.add_column("Team", style="cyan")
    table.add_column("Environment")
    table.add_column("Type", style="dim")
    table.add_column("Namespace")
    table.add_column("Pods")
    table.add_column("Status")
    table.add_column("Region", style="dim")
    table.add_column("Age", style="dim")

    for env in environments:
        status_color = "green" if env["status"] == "Healthy" else "red"
        table.add_row(
            env["team"],
            env["environment"],
            env["type"],
            env["namespace"],
            env["pods"],
            f"[{status_color}]{env['status']}[/{status_color}]",
            env["region"],
            env["age"]
        )

    console.print(table)
    console.print(f"\n[dim]{len(environments)} environment(s) total[/dim]")
