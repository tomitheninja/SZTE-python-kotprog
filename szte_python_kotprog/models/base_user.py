"""Alap felhasználó adattároló modell"""
from szte_python_kotprog.models.county import County


class BaseUser:
    """Felhasználó modell"""
    alias: str
    
    def __init__(self, alias: str) -> None:
        self.alias = alias

    def __str__(self) -> str:
        return f"{self.alias} - {self.counties}"
