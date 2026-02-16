from dataclasses import dataclass, field
from datetime import datetime, date as Date


@dataclass
class ExpenseRecord:
    id: int
    amount: float
    description: str
    date: Date = field(default=Date.today())
