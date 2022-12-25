"""Configuration parser"""
import configparser
from dataclasses import dataclass


@dataclass
class Vault:
    audit_file: str


@dataclass
class Config:
    vault: Vault


def load_config(path: str):
    config = configparser.ConfigParser()
    config.read(path)

    vault_configuration = config["vault"]

    return Config(
        vault=Vault(
            audit_file=vault_configuration.get("audit_file"),
        ),
    )
