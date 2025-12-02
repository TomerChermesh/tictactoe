from datetime import datetime
from enum import Enum
from pathlib import Path

from src.utils.files import append_to_file


class LogLevel(str, Enum):
    DEBUG = 'DEBUG'
    INFO = 'INFO'
    WARNING = 'WARNING'
    ERROR = 'ERROR'
    CRITICAL = 'CRITICAL'


from src.constants.logger import LOG_DIR_PATH, LOG_FILE_DATE_FORMAT

class Logger:
    def __init__(self, name: str = 'app'):
        self.name: str = name
        self.log_dir: Path = Path(LOG_DIR_PATH)

    def _get_log_file_path_for_today(self) -> str:
        today_str: str = datetime.now().strftime(LOG_FILE_DATE_FORMAT)
        return str(self.log_dir / f'{today_str}.log')

    def _log(self, level: LogLevel, message: str, exception: Exception | None = None) -> None:
        timestamp: str = datetime.now().isoformat()
        log_message: str = f'[{timestamp}] [{level.value}] [{self.name}] {message}'

        if exception:
            log_message += f' | Exception: {type(exception).__name__}: {str(exception)}'

        print(log_message)
        log_file_path: str = self._get_log_file_path_for_today()
        append_to_file(log_file_path, log_message)

    def debug(self, message: str) -> None:
        self._log(LogLevel.DEBUG, message, exception)

    def info(self, message: str) -> None:
        self._log(LogLevel.INFO, message, exception)

    def warning(self, message: str, exception: Exception | None = None) -> None:
        self._log(LogLevel.WARNING, message, exception)

    def error(self, message: str, exception: Exception | None = None) -> None:
        self._log(LogLevel.ERROR, message, exception)

    def critical(self, message: str, exception: Exception | None = None) -> None:
        self._log(LogLevel.CRITICAL, message, exception)


logger: Logger = Logger('app')
