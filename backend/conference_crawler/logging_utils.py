from __future__ import annotations

import sys
from datetime import datetime
from pathlib import Path

from loguru import logger


def setup_logging(log_dir: Path, command_name: str, log_level: str = "INFO") -> Path:
    log_dir.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    log_path = log_dir / f"{command_name}_{timestamp}.log"

    logger.remove()
    logger.add(
        sys.stderr,
        level="WARNING",
        colorize=True,
        enqueue=False,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}:{function}:{line}</cyan> - <level>{message}</level>",
    )
    logger.add(
        log_path,
        level=log_level.upper(),
        enqueue=True,
        encoding="utf-8",
        backtrace=True,
        diagnose=False,
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
    )
    logger.info("Log file: {}", log_path)
    return log_path
