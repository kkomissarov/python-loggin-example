import json
import logging.config
import datetime as dt
import sys


class JSONLoggerFormatter(logging.Formatter):
    def __init__(self, *, fmt_keys: dict[str, str] = None):
        super().__init__()
        self.fmt_keys = fmt_keys if fmt_keys is not None else {}

    def format(self, record: logging.LogRecord) -> str:
        message = self._build_message(record)
        return json.dumps(message)

    def _build_message(self, record: logging.LogRecord) -> dict:
        data = {key: getattr(record, value) for key, value in self.fmt_keys.items()}
        data.update({
            "created": dt.datetime.fromtimestamp(record.created, tz=dt.timezone.utc).isoformat(),
            "message": record.getMessage(),
        })
        if record.exc_info is not None:
            data["exc_info"] = self.formatException(record.exc_info)
        if record.stack_info is not None:
            data["stack_info"] = self.formatStack(record.stack_info)
        return data


with open('logging_config.json') as f:
    logger_config = json.load(f)

logging.config.dictConfig(logger_config)

logger = logging.getLogger('test_logging')


def log_exception(type, value, tb):
    logger.error("Uncaught exception", exc_info=(type, value, tb))

sys.excepthook = log_exception
