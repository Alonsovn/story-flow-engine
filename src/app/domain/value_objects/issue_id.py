from dataclasses import dataclass


@dataclass(frozen=True)
class IssueId:
    """
    Value object representing a Jira issue identifier.
    
    Immutable by design - the identifier of an issue should not change.
    """
    key: str
    numeric_id: int

    def __str__(self) -> str:
        return self.key

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, IssueId):
            return False
        return self.key == other.key and self.numeric_id == other.numeric_id

    def __hash__(self) -> int:
        return hash((self.key, self.numeric_id))

    @classmethod
    def from_string(cls, key: str) -> "IssueId":
        """
        Creates an IssueId from a string like 'PROJ-123'.
        Note: Numeric ID will be 0 when created this way (full ID requires API response).
        """
        parts = key.rsplit("-", 1)
        if len(parts) == 2 and parts[1].isdigit():
            return cls(key=key, numeric_id=int(parts[1]))
        return cls(key=key, numeric_id=0)
