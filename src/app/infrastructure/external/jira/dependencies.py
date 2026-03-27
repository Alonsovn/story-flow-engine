from src.app.infrastructure.external.jira.jira_api_repository import JiraApiRepository
from src.app.config.app_config import AppConfig

def get_jira_repository() -> JiraApiRepository:
    """
    Create and return an instance of JiraApiRepository.
    Configuration is handled via AppConfig.
    """
    config = AppConfig.instance()
    jira_config = config.get_config("jira")
    
    return JiraApiRepository(
        base_url=jira_config["url"],
        email=jira_config["email"],
        api_token=jira_config["api_token"]
    )