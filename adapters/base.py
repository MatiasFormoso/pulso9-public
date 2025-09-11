from abc import ABC, abstractmethod
from typing import List, Dict, Any
from datetime import datetime

CanonicalOrder = Dict[str, Any]
CanonicalInventory = Dict[str, Any]

class Adapter(ABC):
    @abstractmethod
    def parse_orders(self, csv_path: str) -> List[CanonicalOrder]:
        ...

    @abstractmethod
    def parse_inventory(self, csv_path: str) -> List[CanonicalInventory]:
        ...

def parse_dt(s: str) -> datetime:
    s = (s or "").strip()
    fmts = [
        "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d",
        "%d/%m/%Y %H:%M:%S", "%d/%m/%Y %H:%M", "%d/%m/%Y",
        "%m/%d/%Y %H:%M:%S", "%m/%d/%Y"
    ]
    for f in fmts:
        try:
            return datetime.strptime(s, f)
        except Exception:
            pass
    raise ValueError(f"No pude parsear fecha: {s}")
