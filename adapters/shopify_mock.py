import csv
from typing import List, Dict, Any
from .base import Adapter, parse_dt

class ShopifyMockAdapter(Adapter):
    def parse_orders(self, csv_path: str) -> List[Dict[str, Any]]:
        out = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                out.append({
                    "id": row.get("Name"),
                    "created_at": parse_dt(row.get("Created at","")),
                    "status": (row.get("Financial Status","") or "").strip().lower(),
                    "total": float((row.get("Total","0") or "0").replace(",","")),
                    "currency": row.get("Currency","ARS"),
                })
        return out

    def parse_inventory(self, csv_path: str) -> List[Dict[str, Any]]:
        out = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                out.append({
                    "sku": row.get("Variant SKU"),
                    "title": row.get("Title"),
                    "stock": int((row.get("Quantity Available") or 0)),
                })
        return out
