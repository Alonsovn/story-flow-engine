import httpx
from datetime import datetime

from src.app.domain.entities import Epic, IssueStatus
from src.app.domain.value_objects import IssueId


class JiraApiRepository:
    def __init__(self, base_url: str, email: str, api_token: str):
        """
        Initialize the JiraApiRepository with base URL and authentication details.

        Args:
            base_url (str): The base URL of the Jira instance (e.g., "https://your-domain.atlassian.net").
            email (str): The email address associated with the API token.
            api_token (str): The API token for authentication.
        """
        self.base_url = base_url
        self.email = email
        self.api_token = api_token

    async def get_epic(self, issue_id: IssueId) -> Epic:
        """
        Retrieve details of an epic by its key from Jira.

        Args:
            issue_id (IssueId): The IssueId of the epic to retrieve.

        Returns:
            Epic: The Epic domain entity.

        Raises:
            httpx.HTTPError: If the API request fails.
        """
        url = f"{self.base_url}/rest/agile/1.0/epic/{issue_id.key}"
        
        async with httpx.AsyncClient() as client:
            response = await client.get(
                url,
                auth=(self.email, self.api_token),
                headers={"Accept": "application/json"}
            )
            response.raise_for_status()
            data = response.json()

        # Map Jira response to Epic entity
        def parse_jira_datetime(dt_str: str) -> datetime:
            """Parse Jira datetime format to datetime object."""
            # Handle timezone format like -0500 -> -05:00
            if dt_str[-5] in ('+', '-') and dt_str[-3] != ':':
                dt_str = dt_str[:-2] + ':' + dt_str[-2:]
            return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

        return Epic.create(
            key=data["key"],
            numeric_id=int(data["id"]),
            summary=data["fields"]["summary"],
            description=data["fields"].get("description", ""),
            status=IssueStatus.from_jira_status(data["fields"]["status"]["name"]),
            created_at=parse_jira_datetime(data["fields"]["created"]),
            updated_at=parse_jira_datetime(data["fields"]["updated"]),
            reporter=data["fields"].get("reporter", {}).get("displayName"),
            priority=data["fields"].get("priority", {}).get("name") if data["fields"].get("priority") else None,
            labels=data["fields"].get("labels", []),
            story_points=data["fields"].get("customfield_10011"),
        )