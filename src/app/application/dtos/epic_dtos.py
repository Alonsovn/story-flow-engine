from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

from .story_dtos import StoryDtoResponse


class EpicDtoResponse(BaseModel):
    """Data Transfer Object for Epic responses."""
    key: str
    numeric_id: int
    summary: str
    description: str
    status: str
    assignee: Optional[str]
    reporter: Optional[str]
    priority: Optional[str]
    labels: List[str]
    story_points: Optional[int]
    created_at: datetime
    updated_at: datetime
    user_stories: List[StoryDtoResponse] = Field(default_factory=list)

