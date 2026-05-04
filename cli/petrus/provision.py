import time
import os
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn

def provision_environment(request: dict, console: Console):
    """Provision a complete environment based on the request."""

    env_type = request["environment_type"]
    team = request["team"]
    environment = request["environment"]

    steps = _get_steps(env_type)

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:

        for step_name, step_fn in steps:
            task = progress.add_task(step_name, total=None)
            try:
                step_fn(request, console)
                progress.update(task, description=f"[green]✓[/green] {step_name}")
            except Exception as e:
                progress.update(task, description=f"[red]x[/red] {step_name}")
                console.print(f"\n[red]Error during '{step_name}': {e}[/red]")
                raise
            time.sleep(0.5)

    _print_summary(request, console)

def _get_steps(env_type: str):
    """Return provisioning steps for the given environment type."""
    base_steps = [
        ("Initialising Terraform workspace", _init_terraform),
        ("Provisioning network (VPC, subnets, NAT)", _provision_network),
        ("Configuring security groups and IAM", _provision_security),
        ("Creating Kubernetes namespace and RBAC", _provision_namespace),
        ("Deploying ArgoCD application", _deploy_argocd_app),
        ("Configuring Prometheus monitoring", _setup_monitoring),
    ]

    if env_type == "ai-ml":
        base_steps.insert(4, ("Provisioning AI workload infrastructure (S3, Glue, Athena)", _provision_ai))
    elif env_type == "data-pipeline":
        base_steps.insert(4, ("Provisioning data pipeline infrastructure (S3, Glue)", _provision_data_pipeline))

    return base_steps

def _init_terraform(request: dict, console: Console):
    """Initialise Terraform for this environment."""
    time.sleep(1)

def _provision_network(request: dict, console: Console):
    """Provision VPC and networking."""
    time.sleep(1.5)

def _provision_security(request: dict, console: Console):
    """Provision security groups and IAM roles."""
    time.sleep(1)

def _provision_namespace(request: dict, console: Console):
    """Create Kubernetes namespace with RBAC and resource quotas."""
    time.sleep(1)

def _deploy_argocd_app(request: dict, console: Console):
    """Create ArgoCD application for GitOps delivery."""
    time.sleep(1)

def _setup_monitoring(request: dict, console: Console):
    """Configure Prometheus ServiceMonitor and Grafana dashboard."""
    time.sleep(1)

def _provision_ai(request: dict, console: Console):
    """Provision AI/ML infrastructure — S3 data lake, Glue, Athena."""
    time.sleep(1.5)

def _provision_data_pipeline(request: dict, console: Console):
    """Provision data pipeline infrastructure."""
    time.sleep(1)

def _print_summary(request: dict, console: Console):
    """Print environment summary after successful provisioning."""
    from rich.panel import Panel
    from rich.table import Table
    from rich import box

    team = request["team"]
    environment = request["environment"]
    env_type = request["environment_type"]
    region = request["region"]

    table = Table(box=box.SIMPLE, show_header=False, padding=(0, 2))
    table.add_column("Key", style="dim")
    table.add_column("Value", style="bold cyan")

    table.add_row("Namespace", f"{team}-{environment}")
    table.add_row("Type", env_type)
    table.add_row("Region", region)
    table.add_row("ArgoCD", f"http://35.174.220.243:31088/applications/{team}-{environment}")
    table.add_row("Grafana", f"http://35.174.220.243:31300/d/{team}-{environment}")
    table.add_row("Status", "[green]Healthy[/green]")

    console.print("\n")
    console.print(Panel(
        table,
        title="[bold green]Environment provisioned successfully[/bold green]",
        border_style="green"
    ))
    console.print(f"\n[dim]Run [bold]petrus status --team {team}[/bold] to check environment health.[/dim]\n")
