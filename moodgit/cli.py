"""
MoodGit CLI — analyze emotional patterns in your git commits
"""

import sys
import os
import click
from pathlib import Path

from moodgit.analyzer import get_commits, analyze_emotions, compute_summary
from moodgit.display import (
    render_header, render_commits_table, render_summary, render_footer, console
)
from moodgit.report import generate_html


@click.command()
@click.argument("repo_path", default=".", type=click.Path(exists=True))
@click.option("--limit", "-n", default=30, show_default=True,
              help="Number of recent commits to analyze")
@click.option("--branch", "-b", default=None,
              help="Branch to analyze (default: current branch)")
@click.option("--html", "html_output", default=None, metavar="FILE",
              help="Export an HTML report to FILE (e.g. report.html)")
@click.option("--api-key", default=None, envvar="ANTHROPIC_API_KEY",
              help="Anthropic API key (or set ANTHROPIC_API_KEY env var)")
@click.option("--no-table", is_flag=True, default=False,
              help="Skip the per-commit table, show only summary")
def main(repo_path, limit, branch, html_output, api_key, no_table):
    """
    \b
    MoodGit — your commits have feelings 🎭
    
    Analyzes the emotional tone of git commit messages using Claude AI
    and renders a timeline showing stress peaks, hype moments, late nights,
    and your overall project vibe.

    \b
    Examples:
      moodgit                        # analyze current repo, last 30 commits
      moodgit /path/to/repo -n 50    # analyze another repo, 50 commits
      moodgit --html report.html     # also export HTML report
    """
    render_header()

    # --- Load commits ---
    console.print(f"[dim]Loading commits from[/dim] [bold]{repo_path}[/bold]...")
    try:
        commits, repo = get_commits(repo_path, limit=limit, branch=branch)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)

    repo_name = Path(repo.working_dir).name
    console.print(f"[dim]Found[/dim] [bold]{len(commits)}[/bold] [dim]commits in[/dim] [bold]{repo_name}[/bold]")

    if not commits:
        console.print("[yellow]No commits found on this branch.[/yellow]")
        sys.exit(0)

    # --- Analyze ---
    console.print("[dim]Sending to Claude for emotion analysis...[/dim]")
    try:
        analyzed = analyze_emotions(commits, api_key=api_key)
    except ValueError as e:
        console.print(f"[bold red]Error:[/bold red] {e}")
        sys.exit(1)
    except Exception as e:
        console.print(f"[bold red]API error:[/bold red] {e}")
        sys.exit(1)

    summary = compute_summary(analyzed)

    console.print()

    # --- Display ---
    if not no_table:
        render_commits_table(analyzed)
        console.print()

    render_summary(summary, repo_name)

    # --- HTML export ---
    if html_output:
        html = generate_html(analyzed, summary, repo_name)
        with open(html_output, "w", encoding="utf-8") as f:
            f.write(html)
        console.print(f"\n[bold green]✓[/bold green] HTML report saved to [bold]{html_output}[/bold]")

    render_footer()


if __name__ == "__main__":
    main()
