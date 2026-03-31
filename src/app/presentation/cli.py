import json

import typer
import asyncio
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
            "create_epic": "Create a new epic in JIRA",
            "exit": "Exit the application",
        }
        menu_choice = inquirer.select(
            message="Select an option:",
            choices=[{"name": description, "value": key} for key, description in menu_options.items()],
        ).execute()

        if menu_choice == "get_epic":
            jira_key = inquirer.text(message="Enter the JIRA key:").execute()
            fetch_epic(jira_key)
        elif menu_choice == "create_epic":
            file_path = inquirer.text(message="Enter the path to the Epic file:").execute()
            create_epic(file_path)
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

def create_epic(file_path: str):
    """
    Create a new epic in JIRA.

    Calls the JIRA API to create the epic and displays the result.
    """
    async def main():
        # Retrieve JiraApiRepository instance
        jira_repo = get_jira_repository()

        try:
            with open(file_path, 'r') as file:
                epic_data = file.read()

            # Parse Markdown data to extract epic details
            lines = epic_data.splitlines()

            summary = None
            description_lines = []
            priority_name = None

            for line in lines:
                if line.startswith('**Summary**:'):
                    summary = line.split(':', 1)[1].strip()
                elif line.startswith('**Priority**:'):
                    priority_name = line.split(':', 1)[1].strip()
                else:
                    description_lines.append(line)

            description = '\n'.join(description_lines).strip()

            if not summary or not priority_name:
                raise ValueError("Missing required fields: 'Summary' and/or 'Priority' in the Markdown file.")

            priority = Priority.from_string(priority_name)

            priority = Priority.from_string(priority_name)
        except (FileNotFoundError, json.JSONDecodeError, KeyError) as e:
            typer.echo(f"Invalid file or content. Error: {e}")
            return

        # Call the async create_epic method
        new_epic = await jira_repo.create_epic(
            summary=summary, description=description, priority=priority
        )

        typer.echo("Epic Successfully Created!")
        typer.echo(f"Key: {new_epic.key}")
        typer.echo(f"Summary: {new_epic.summary}")
        typer.echo(f"Description: {new_epic.description}")



if __name__ == "__main__":
    show_welcome_message()
    interactive_menu(skip_initial_prompt=False)