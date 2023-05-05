"""Base for user models"""

from szte_python_kotprog.models.county import County


class BaseUser:
    """User model base class"""
    alias: str
    counties: list[County]

    def __init__(self, alias: str) -> None:
        self.alias = alias
        self.counties: list[County] = []

    def __str__(self) -> str:
        return f"{self.alias}"
