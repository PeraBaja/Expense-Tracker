from dataclasses import dataclass, field
from datetime import datetime, date as Date


@dataclass
class ExpenseRecord:
    id: int
    description: str
    amount: float
    category: str | None = field(default=None)
    date: Date = field(default=Date.today())
