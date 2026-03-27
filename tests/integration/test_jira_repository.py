import pytest
import respx
from httpx import Response

from src.app.domain.entities import Epic
from src.app.domain.value_objects import IssueId
from src.app.infrastructure.external.jira.jira_api_repository import JiraApiRepository


@pytest.fixture
def jira_repository():
    """
    Fixture to create a JiraApiRepository instance for testing.
    """
    return JiraApiRepository(
        base_url="https://test-jira.atlassian.net",
        email="test@example.com",
        api_token="test_key",
    )


@pytest.mark.asyncio
@respx.mock
async def test_get_epic_success(jira_repository):
    """
    Test successful retrieval of an Epic from the Jira API.
    This is the "Red" test that will fail initially.
    """
    # Arrange
    epic_key = "PROJ-1"
    mock_response = {
        "id": "10001",
        "key": epic_key,
        "fields": {
            "summary": "Test Epic from API",
            "description": "A detailed description.",
            "status": {"name": "To Do"},
            "creator": {"displayName": "Test User"},
            "reporter": {"displayName": "Test User"},
            "priority": {"name": "High"},
            "labels": ["backend", "api"],
            "customfield_10011": 8.0,  # Story Points
            "created": "2025-01-01T10:00:00.000-0500",
            "updated": "2025-01-02T11:00:00.000-0500",
        },
    }

    # Mock the HTTP request to the Jira API
    respx.get(
        f"https://test-jira.atlassian.net/rest/agile/1.0/epic/{epic_key}"
    ).mock(
            side_effect=lambda request: (
                        Response(200, json=mock_response)
                        if request.headers.get("Authorization") else Response(401)
            )
    )

    # Act
    epic = await jira_repository.get_epic(IssueId.from_string(epic_key))

    # Assert
    assert epic is not None
    assert isinstance(epic, Epic)
    assert epic.key == epic_key
    assert epic.summary == "Test Epic from API"
    assert epic.story_points.value == 8
    assert len(epic.labels) == 2
    assert epic.labels.has_label_named("backend")