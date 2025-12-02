from datetime import datetime
from enum import Enum
from typing import Optional


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


class Logger:   
    def __init__(self, name: str = 'app'):
        self.name: str = name

    def _log(self, level: LogLevel, message: str, exception: Optional[Exception] = None) -> None:
        timestamp: str = datetime.now().isoformat()
        log_message: str = f'[{timestamp}] [{level.value}] [{self.name}] {message}'
        
        if exception:
            log_message += f' | Exception: {type(exception).__name__}: {str(exception)}'
        
        print(log_message)

    def debug(self, message: str, exception: Optional[Exception] = None) -> None:
        self._log(LogLevel.DEBUG, message, exception)

    def info(self, message: str, exception: Optional[Exception] = None) -> None:
        self._log(LogLevel.INFO, message, exception)

    def warning(self, message: str, exception: Optional[Exception] = None) -> None:
        self._log(LogLevel.WARNING, message, exception)

    def error(self, message: str, exception: Optional[Exception] = None) -> None:
        self._log(LogLevel.ERROR, message, exception)

    def critical(self, message: str, exception: Optional[Exception] = None) -> None:
        self._log(LogLevel.CRITICAL, message, exception)


logger: Logger = Logger('app')
