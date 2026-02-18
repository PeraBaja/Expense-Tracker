from dataclasses import dataclass, field
from datetime import date
from pathlib import Path


@dataclass
class ArgsSchema:
    action: str
    description: str | None = field(default=None)
    id: int | None = field(default=None)
    amount: float | None = field(default=None)
    category: str | None = field(default=None)
    month: str | None = field(default=None)
    date_made: date | None = field(default=None)
    list: bool | None = field(default=None)
    to_path: Path | None = field(default=None)
