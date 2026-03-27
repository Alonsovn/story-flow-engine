import typer
import asyncio
from src.app.infrastructure.external.jira.dependencies import get_jira_repository

# Initialize Typer app
app = typer.Typer()

@app.command()
def fetch_epic(issue_id: str):
    """
    Fetch details of an epic from JIRA using the issue ID.
    
    Args:
        issue_id (str): The key of the epic to retrieve.
    
    Example:
        `python -m cli fetch-epic TEST-123`
    """
    async def main():
        # Retrieve JiraApiRepository instance
        jira_repo = get_jira_repository()
        try:
            # Await the async get_epic method
            epic = await jira_repo.get_epic(issue_id)
            typer.echo("Epic Summary:")
            typer.echo(f"Key: {epic.key}")
            typer.echo(f"Summary: {epic.summary}")
            typer.echo(f"Description: {epic.description}")
        except Exception as e:
            typer.echo(f"Error fetching epic: {e}")

    # Use asyncio.run to handle the async call
    asyncio.run(main())
