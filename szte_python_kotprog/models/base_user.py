"""Alap felhasználó adattároló modell"""
from szte_python_kotprog.models.county import County


class BaseUser:
    """Felhasználó modell"""
    counties: list[County]
    alias: str
    
    def __init__(self, alias: str, counties: list[County]) -> None:
        self.alias = alias
        self.counties = counties

    def __str__(self) -> str:
        return f"{self.alias} - {self.counties}"
