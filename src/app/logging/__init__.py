from abc import ABCMeta, abstractmethod
import enum
import logging
import datetime


# -----------------------------------------------------------------------------
# CLASS LOG LEVEL
# -----------------------------------------------------------------------------
class LogLevel(enum.Enum):
    INFO = 0
    WARNING = 1
    ERROR = 2
    DEBUG = 3


# -----------------------------------------------------------------------------
# CLASS LOGGER BASE
# -----------------------------------------------------------------------------
class AbstractLogger:
    __metaclass__ = ABCMeta

    """
    A simple logger interface that provides abstraction of the actual
    implementation of the logger and enables injecting loggers to classes
    through dependency inversion principle.
    """

    @abstractmethod
    def debug(self, message: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def info(self, message: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def warning(self, message: str, **kwargs) -> dict:
        pass

    @abstractmethod
    def error(self, message: str, **kwargs) -> dict:
        pass


# -----------------------------------------------------------------------------
# CLASS LOG EVENT
# -----------------------------------------------------------------------------
class LogEvent:
    # -------------------------------------------------------------------------
    # CONSTRUCTOR
    # -------------------------------------------------------------------------
    def __init__(self, message, level: LogLevel):
        self._message: str = message
        self._level: LogLevel = level
        self._utc_datetime = datetime.datetime.utcnow()

    # -------------------------------------------------------------------------
    # METHOD UTC TIMESTAMP
    # -------------------------------------------------------------------------
    @property
    def utc_timestamp(self) -> datetime.datetime:
        return self._utc_datetime

    # -------------------------------------------------------------------------
    # METHOD DICT
    # -------------------------------------------------------------------------
    def dict(self) -> dict:
        return {
            "message": self._message,
            "level": self._level.name,
            "utc_datetime": self._utc_datetime,
        }

    # -------------------------------------------------------------------------
    # METHOD STR
    # -------------------------------------------------------------------------
    def __str__(self) -> str:
        return f"[{self._level.name}: " f"{str(self._utc_datetime)}]: {self._message}"


# -----------------------------------------------------------------------------
# CLASS SIMPLE LOGGER
# -----------------------------------------------------------------------------
class StandardOutputLogger(AbstractLogger):
    def __init__(self):
        logging.getLogger().setLevel(logging.DEBUG)

    # -------------------------------------------------------------------------
    # METHOD DEBUG
    # -------------------------------------------------------------------------
    def debug(self, message: str, **kwargs) -> dict:
        event = LogEvent(message=message, level=LogLevel.DEBUG)
        logging.debug(str(event))
        return event.dict()

    # -------------------------------------------------------------------------
    # METHOD INFO
    # -------------------------------------------------------------------------
    def info(self, message: str, **kwargs) -> dict:
        event = LogEvent(message=message, level=LogLevel.INFO)
        logging.info(str(event))
        return event.dict()

    # -------------------------------------------------------------------------
    # METHOD WARNING
    # -------------------------------------------------------------------------
    def warning(self, message: str, **kwargs) -> dict:
        event = LogEvent(message=message, level=LogLevel.WARNING)
        logging.warning(str(event))
        return event.dict()

    # -------------------------------------------------------------------------
    # METHOD ERROR
    # -------------------------------------------------------------------------
    def error(self, message: str, **kwargs) -> dict:
        event = LogEvent(message=message, level=LogLevel.ERROR)
        logging.error(str(event))
        return event.dict()
