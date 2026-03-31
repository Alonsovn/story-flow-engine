from datetime import datetime
from src.app.domain.entities import Epic, IssueStatus

class JiraApiHelpers:
    @staticmethod
    def parse_jira_datetime(dt_str: str) -> datetime:
        """Parse Jira datetime format to a Python datetime object."""
        if dt_str[-5] in ('+', '-') and dt_str[-3] != ':':
            dt_str = dt_str[:-2] + ':' + dt_str[-2:]
        return datetime.fromisoformat(dt_str.replace("Z", "+00:00"))

    @staticmethod
    def map_epic(data: dict) -> Epic:
        """
        Map Jira API response data to the Epic domain entity.

        Args:
            data (dict): Jira API response data.

        Returns:
            Epic: The mapped Epic entity.
        """
        return Epic.create(
            key=data["key"],
            numeric_id=int(data["id"]),
            summary=data["fields"].get("summary", ""),
            description=data["fields"].get("description", ""),
            status=IssueStatus.from_jira_status(data["fields"]["status"]["name"]),
            created_at=JiraApiHelpers.parse_jira_datetime(data["fields"]["created"]),
            updated_at=JiraApiHelpers.parse_jira_datetime(data["fields"]["updated"]),
            reporter=data["fields"].get("reporter", {}).get("displayName"),
            priority=data["fields"].get("priority", {}).get("name") if data["fields"].get("priority") else None,
            labels=data["fields"].get("labels", []),
            story_points=data["fields"].get("customfield_10011"),
        )