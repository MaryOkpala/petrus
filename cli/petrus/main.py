import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box
from petrus.provision import provision_environment
from petrus.destroy import destroy_environment
from petrus.status import get_status
from petrus.policy import check_policy

console = Console()

BANNER = r"""
[bold blue]
  ____       _                 
 |  _ \ ___ | |_ _ __ _   _ ___ 
 | |_) / _ \| __| '__| | | / __|
 |  __/  __/| |_| |  | |_| \__ \\
 |_|   \___| \__|_|   \__,_|___/
[/bold blue]
[dim]Internal Developer Platform — self-service infrastructure[/dim]
"""

@click.group()
def cli():
    """Petrus — Internal Developer Platform CLI.
    
    Provision, manage, and destroy cloud environments
    without filing a ticket.
    """
    pass

@cli.command()
def version():
    """Show Petrus version."""
    console.print("[bold blue]Petrus[/bold blue] v0.1.0")

@cli.command()
@click.option("--type", "env_type", required=True,
              type=click.Choice(["web-app", "api", "data-pipeline", "ai-ml"]),
              help="Environment type to provision")
@click.option("--team", required=True, help="Your team name")
@click.option("--env", "environment", required=True,
              type=click.Choice(["dev", "staging", "prod"]),
              help="Environment name")
@click.option("--region", default="us-east-1", help="AWS region")
@click.option("--instance-type", default="t3.medium", help="EC2 instance type")
@click.option("--approved", is_flag=True, default=False,
              help="Platform team approval flag for large instances")
@click.option("--dry-run", is_flag=True, default=False,
              help="Validate and plan without provisioning")
def provision(env_type, team, environment, region, instance_type, approved, dry_run):
    """Provision a new cloud environment.
    
    Examples:
    
      petrus provision --type web-app --team payments --env dev
      
      petrus provision --type ai-ml --team data-science --env staging
      
      petrus provision --type api --team platform --env prod --instance-type m5.large --approved
    """
    console.print(BANNER)

    request = {
        "environment_type": env_type,
        "team": team,
        "environment": environment,
        "region": region,
        "instance_type": instance_type,
        "approved": approved,
        "nat_gateway": environment != "dev",
        "current_environment_count": 0,
        "tags": {
            "team": team,
            "environment": environment,
            "cost_center": team
        }
    }

    console.print(Panel(
        f"[bold]Provisioning request[/bold]\n\n"
        f"  Type:      [cyan]{env_type}[/cyan]\n"
        f"  Team:      [cyan]{team}[/cyan]\n"
        f"  Env:       [cyan]{environment}[/cyan]\n"
        f"  Region:    [cyan]{region}[/cyan]\n"
        f"  Instance:  [cyan]{instance_type}[/cyan]",
        title="Petrus",
        border_style="blue"
    ))

    console.print("\n[bold yellow]Checking policies...[/bold yellow]")
    allowed, violations = check_policy(request)

    if not allowed:
        console.print("\n[bold red]Policy check FAILED[/bold red]")
        for v in violations:
            console.print(f"  [red]x[/red] {v}")
        console.print("\n[dim]Fix the violations above and try again.[/dim]")
        raise SystemExit(1)

    console.print("[bold green]Policy check PASSED[/bold green]")

    if dry_run:
        console.print("\n[bold yellow]Dry run mode — no resources will be created.[/bold yellow]")
        console.print("[dim]Remove --dry-run to provision for real.[/dim]")
        return

    console.print("\n[bold blue]Starting provisioning...[/bold blue]")
    provision_environment(request, console)

@cli.command()
@click.option("--team", required=True, help="Team name")
@click.option("--env", "environment", required=True,
              type=click.Choice(["dev", "staging", "prod"]),
              help="Environment to destroy")
@click.option("--force", is_flag=True, default=False,
              help="Skip confirmation prompt")
def destroy(team, environment, force):
    """Destroy a provisioned environment.
    
    Example:
    
      petrus destroy --team payments --env dev
    """
    if not force:
        confirm = click.confirm(
            f"Destroy {team}-{environment}? This cannot be undone.",
            default=False
        )
        if not confirm:
            console.print("[dim]Aborted.[/dim]")
            return

    console.print(f"\n[bold red]Destroying {team}-{environment}...[/bold red]")
    destroy_environment(team, environment, console)

@cli.command()
@click.option("--team", default=None, help="Filter by team")
def status(team):
    """Show status of all provisioned environments.
    
    Examples:
    
      petrus status
      
      petrus status --team payments
    """
    get_status(team, console)

@cli.command()
@click.option("--type", "env_type", required=True,
              type=click.Choice(["web-app", "api", "data-pipeline", "ai-ml"]))
@click.option("--team", required=True)
@click.option("--env", "environment", required=True,
              type=click.Choice(["dev", "staging", "prod"]))
@click.option("--instance-type", default="t3.medium")
@click.option("--region", default="us-east-1")
def validate(env_type, team, environment, instance_type, region):
    """Validate a provisioning request against policies without provisioning.
    
    Example:
    
      petrus validate --type web-app --team payments --env prod --instance-type m5.large
    """
    request = {
        "environment_type": env_type,
        "team": team,
        "environment": environment,
        "region": region,
        "instance_type": instance_type,
        "approved": False,
        "nat_gateway": environment != "dev",
        "current_environment_count": 0,
        "tags": {
            "team": team,
            "environment": environment,
            "cost_center": team
        }
    }

    console.print(f"\n[bold]Validating request...[/bold]")
    allowed, violations = check_policy(request)

    if allowed:
        console.print("[bold green]PASSED[/bold green] — request is valid and would be provisioned.")
    else:
        console.print("[bold red]FAILED[/bold red] — request violates the following policies:\n")
        for v in violations:
            console.print(f"  [red]x[/red] {v}")

if __name__ == "__main__":
    cli()
