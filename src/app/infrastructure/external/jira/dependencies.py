from src.app.infrastructure.external.jira.jira_api_repository_impl import JiraApiRepositoryImpl
from src.app.config.app_config import AppConfig

def get_jira_repository() -> JiraApiRepositoryImpl:
    """
    Create and return an instance of JiraApiRepository.
    Configuration is handled via AppConfig.
    """
    config = AppConfig.instance()
    jira_config = config.get_config("jira")
    
    return JiraApiRepositoryImpl(jira_config)