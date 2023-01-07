import time
from pathlib import Path

from prometheus_client import start_http_server

from app.config import load_config
from app.utils.logger import customize_logging
from app.handlers import check_file_changes, analyze_audit_file


"""
TODO
- audit file rotation
- memorize the line offset in db
- compare hash tmp and log
- yaml config
- /home/user/Projects/vault/Vault-Audit-Prometheus-Exporter/app/handlers/analyze_audit_file.py:32: FutureWarning: The frame.append method is deprecated and will be removed from pandas in a future version. Use pandas.concat instead.


import pyhash
hasher = pyhash.metro_64()
hasher("")
"""


if __name__ == "__main__":
    config = load_config(
        "exporter.ini"
    )  # TODO: 1) check if exists 2) sys.argv[1] or default

    # logger = customize_logging(
    #     filepath=Path(config.logging.path),
    #     level=config.logging.level,
    #     retention=config.logging.retention,
    #     rotation=config.logging.rotation,
    #     _format=config.logging.format,
    # )

    start_http_server(config.prometheus.port)

    event_handler = analyze_audit_file.AuditFileModificationHandler(
        config.vault.audit_file
    )
    observer = check_file_changes.FileObserver(
        event_handler, config.vault.audit_file
    )  # TODO: check if exists
    observer.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()
