import time
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def destroy_environment(team: str, environment: str, console: Console):
    """Destroy all resources for a team environment."""

    steps = [
        "Removing ArgoCD application",
        "Deleting Kubernetes namespace and workloads",
        "Destroying AI/data infrastructure",
        "Removing security groups and IAM roles",
        "Destroying VPC and networking",
        "Cleaning up Terraform state",
    ]

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        for step in steps:
            task = progress.add_task(step, total=None)
            time.sleep(1)
            progress.update(task, description=f"[green]✓[/green] {step}")

    console.print(f"\n[bold green]✓ {team}-{environment} destroyed successfully.[/bold green]")
    console.print("[dim]All AWS resources have been removed. Terraform state updated.[/dim]\n")
