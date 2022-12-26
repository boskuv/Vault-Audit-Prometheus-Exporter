"""Configuration parser"""
import configparser
from dataclasses import dataclass


@dataclass
class Vault:
    audit_file: str


@dataclass
class Prometheus:
    port: int


@dataclass
class Config:
    vault: Vault
    prometheus: Prometheus


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    vault_configuration = config["vault"]
    prometheus_configuration = config["port"]

    return Config(
        vault=Vault(
            audit_file=vault_configuration.get("audit_file"),
        ),
        prometheus=Prometheus(
            port=prometheus_configuration.get("port"),
        ),
    )
