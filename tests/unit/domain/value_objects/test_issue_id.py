import pytest

from src.app.domain.value_objects import IssueId


class TestIssueIdCreation:
    def test_create_with_key_and_numeric_id(self):
        issue = IssueId(key="PROJ-123", numeric_id=123)
        assert issue.key == "PROJ-123"
        assert issue.numeric_id == 123

    def test_from_string_extracts_numeric_id(self):
        issue = IssueId.from_string("PROJ-456")
        assert issue.key == "PROJ-456"
        assert issue.numeric_id == 456

    def test_from_string_invalid_key(self):
        issue = IssueId.from_string("INVALID")
        assert issue.key == "INVALID"
        assert issue.numeric_id == 0


class TestIssueIdImmutability:
    def test_is_frozen(self):
        issue = IssueId(key="PROJ-1", numeric_id=1)
        with pytest.raises(AttributeError):
            issue.key = "OTHER-2"

    def test_equal_objects_have_same_hash(self):
        issue1 = IssueId(key="PROJ-1", numeric_id=1)
        issue2 = IssueId(key="PROJ-1", numeric_id=1)
        assert hash(issue1) == hash(issue2)

    def test_different_objects_have_different_hash(self):
        issue1 = IssueId(key="PROJ-1", numeric_id=1)
        issue2 = IssueId(key="PROJ-2", numeric_id=2)
        assert hash(issue1) != hash(issue2)


class TestIssueIdEquality:
    def test_equal_issue_ids(self):
        issue1 = IssueId(key="PROJ-1", numeric_id=1)
        issue2 = IssueId(key="PROJ-1", numeric_id=1)
        assert issue1 == issue2

    def test_different_keys_are_not_equal(self):
        issue1 = IssueId(key="PROJ-1", numeric_id=1)
        issue2 = IssueId(key="PROJ-2", numeric_id=1)
        assert issue1 != issue2

    def test_different_ids_are_not_equal(self):
        issue1 = IssueId(key="PROJ-1", numeric_id=1)
        issue2 = IssueId(key="PROJ-1", numeric_id=2)
        assert issue1 != issue2

    def test_not_equal_to_non_issue_id(self):
        issue = IssueId(key="PROJ-1", numeric_id=1)
        assert issue != "PROJ-1"


class TestIssueIdStringRepresentation:
    def test_str_returns_key(self):
        issue = IssueId(key="PROJ-123", numeric_id=123)
        assert str(issue) == "PROJ-123"
