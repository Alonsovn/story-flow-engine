from src.app.config.app_config import AppConfig
import logging

class AppLogger:
    """Singleton logger class for consistent logging across the app."""
    _instance = None

    @staticmethod
    def instance():
        """Static access method to get the singleton logger instance."""
        if AppLogger._instance is None:
            AppLogger()
        return AppLogger._instance

    def __init__(self):
        """Private constructor for setting up the logger."""
        if AppLogger._instance is not None:
            raise RuntimeError("Use instance() to get the AppLogger.")

        # Load log settings from AppConfig
        config = AppConfig.instance()  # Get the AppConfig instance
        log_config = config.get_config("logging", default={})

        # Extract logging configuration
        level = log_config.get("level", "INFO").upper()
        format = log_config.get("format", "%(levelname)s %(asctime)s - %(message)s [%(extra)s]")
        date_format = log_config.get("date_format", "%Y-%m-%d %H:%M:%S")

        # Set up the logger
        self.log = logging.getLogger("AppLogger")
        if not self.log.handlers:  # Avoid duplicate handlers
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(format, datefmt=date_format))
            self.log.addHandler(handler)
            self.log.setLevel(logging.getLevelName(level))

        AppLogger._instance = self

    def debug(self, message: str, **kwargs):
        self.log.debug(message, extra=kwargs)

    def info(self, message: str, **kwargs):
        self.log.info(message, extra=kwargs)

    def warning(self, message: str, **kwargs):
        self.log.warning(message, extra=kwargs)

    def error(self, message: str, **kwargs):
        self.log.error(message, extra=kwargs)