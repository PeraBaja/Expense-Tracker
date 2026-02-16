from dataclasses import dataclass, field
from datetime import datetime, date as Date


@dataclass
class ExpenseRecord:
    amount: float
    description: str
    date: Date = field(default=Date.today())
