import typer
import asyncio
from src.app.infrastructure.external.jira.dependencies import get_jira_repository
from src.app.domain.value_objects import IssueId
from InquirerPy import inquirer
import os
# Initialize Typer app with help when no command is provided
app = typer.Typer(no_args_is_help=False)

def show_welcome_message():
    """Display the welcome message."""
    typer.echo("╭──────────────────────────────────────────────────────────────╮")
    typer.echo("│   ███████╗████████╗ ██████╗ ██████╗ ██╗   ██╗                │")
    typer.echo("│   ██╔════╝╚══██╔══╝██╔═══██╗██╔══██╗╚██╗ ██╔╝                │")
    typer.echo("│   ███████╗   ██║   ██║   ██║██████╔╝ ╚████╔╝                 │")
    typer.echo("│   ╚════██║   ██║   ██║   ██║██╔══██╗  ╚██╔╝                  │")
    typer.echo("│   ███████║   ██║   ╚██████╔╝██║  ██║   ██║                   │")
    typer.echo("│   ╚══════╝   ╚═╝    ╚═════╝ ╚═╝  ╚═╝   ╚═╝                   │")
    typer.echo("│                                                              │")
    typer.echo("│        🤖 Story Flow Engine                                  │")
    typer.echo("│        Intelligent Jira Automation Assistant                 │")
    typer.echo("╰──────────────────────────────────────────────────────────────╯")
    typer.echo("")
    typer.echo("System ready.")
    typer.echo("")

def interactive_menu():
    """Handles the interactive user menu."""
    while True:
        typer.echo("\nPress Enter to go back to the main menu...")
        input()
        os.system('cls' if os.name == 'nt' else 'clear')
        show_welcome_message()
        menu_options = {
            "get_epic": "Retrieve an epic and its stories by JIRA key",
            "exit": "Exit the application",
        }
        menu_choice = inquirer.select(
            message="Select an option:",
            choices=[{"name": description, "value": key} for key, description in menu_options.items()],
        ).execute()

        if menu_choice == "get_epic":
            jira_key = inquirer.text(message="Enter the JIRA key:").execute()
            fetch_epic(jira_key)
        elif menu_choice == "exit":
            typer.echo("Goodbye!")
            break

def fetch_epic(issue_id: str):
    """
    Fetch details of an epic from JIRA using the issue ID.
    
    Args:
        issue_id (str): The key of the epic to retrieve.
    
    Example:
        `python -m cli fetch_epic TEST-123`
    """
    async def main():
        # Retrieve JiraApiRepository instance
        jira_repo = get_jira_repository()
        try:
            # Convert string to IssueId value object
            issue_id_vo = IssueId.from_string(issue_id)
            # Await the async get_epic method
            epic = await jira_repo.get_epic(issue_id_vo)
            typer.echo("Epic Summary:")
            typer.echo(f"Key: {epic.key}")
            typer.echo(f"Summary: {epic.summary}")
            typer.echo(f"Description: {epic.description}")
        except Exception as e:
            typer.echo(f"Error fetching epic: {e}")

    # Use asyncio.run to handle the async call
    asyncio.run(main())

if __name__ == "__main__":
    show_welcome_message()
    interactive_menu()