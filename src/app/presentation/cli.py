import typer
import asyncio
from src.app.application.use_cases import CreateEpicWithStories
from src.app.domain.exceptions import BusinessRuleViolationException
from src.app.infrastructure.external.jira.dependencies import get_jira_repository
from src.app.domain.value_objects import IssueId, Priority
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


def interactive_menu(skip_initial_prompt=False):
    """Handles the interactive user menu."""
    while True:
        if not skip_initial_prompt:
            skip_initial_prompt = True
        else:
            typer.echo("\nPress Enter to go back to the main menu...")
            input()
        os.system('cls' if os.name == 'nt' else 'clear')
        show_welcome_message()
        menu_options = {
            "get_epic": "Retrieve an epic and its stories by JIRA key",
            "create_epic_with_stories": "Load an epic and its stories from a folder and upload to JIRA",
            "exit": "Exit the application",
        }
        menu_choice = inquirer.select(
            message="Select an option:",
            choices=[{"name": description, "value": key} for key, description in menu_options.items()],
        ).execute()

        if menu_choice == "get_epic":
            jira_key = inquirer.text(message="Enter the JIRA key:").execute()
            fetch_epic(jira_key)
        elif menu_choice == "create_epic_with_stories":
            folder_path = inquirer.text(
                message="Enter the path to the folder containing epic.md and stories.md:"
            ).execute()
            if not folder_path:
                folder_path = "data/EPIC-0-foundational"

            create_epic_with_stories(folder_path)
        elif menu_choice == "exit":
            typer.echo("Thanks for using Story Flow Engine! Have a great day!")
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


def create_epic_with_stories(folder_path: str):
    """
    Load an epic and its stories from a folder and create them in JIRA.

    Reads `epic.md` (required) and `stories.md` (optional) from the given
    folder, creates the epic, then creates each story linked to it. Story
    creation failures are reported individually and do not stop the rest.

    Args:
        folder_path (str): Path to a folder containing `epic.md` and,
            optionally, `stories.md` (e.g. "data/EPIC-0-foundational").
    """

    async def main():
        jira_repo = get_jira_repository()
        use_case = CreateEpicWithStories(jira_repository=jira_repo)

        try:
            result = await use_case.execute(folder_path)
        except BusinessRuleViolationException as e:
            typer.echo(f"Could not create epic: {e}")
            return

        typer.echo("Epic Successfully Created!")
        typer.echo(f"Key: {result.epic.key}")
        typer.echo(f"Summary: {result.epic.summary}")
        typer.echo(f"Description: {result.epic.description}")

        if not result.story_results:
            return

        typer.echo("")
        typer.echo(f"Stories ({len(result.story_results)}):")
        for story_result in result.story_results:
            if story_result.success:
                typer.echo(f"  [OK] {story_result.story_id} -> {story_result.key}")
            else:
                typer.echo(f"  [FAILED] {story_result.story_id}: {story_result.error}")

    # Use asyncio.run to handle the async call
    asyncio.run(main())


if __name__ == "__main__":
    show_welcome_message()
    interactive_menu(skip_initial_prompt=False)
