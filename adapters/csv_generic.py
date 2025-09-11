import csv, yaml
from typing import List, Dict, Any
from .base import Adapter, parse_dt

def _load_mapping():
    with open("config.yml", "r", encoding="utf-8") as f:
        cfg = yaml.safe_load(f)
    return cfg.get("csv_generic_mapping", {})

class CSVGenericAdapter(Adapter):
    def parse_orders(self, csv_path: str) -> List[Dict[str, Any]]:
        mapping = _load_mapping().get("orders", {})
        out = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                total = (row.get(mapping.get("total","total")) or "0").replace(",","").replace("$","")
                out.append({
                    "id": row.get(mapping.get("id","order_id")),
                    "created_at": parse_dt(row.get(mapping.get("created_at","created_at"))),
                    "status": (row.get(mapping.get("status","status")) or "").strip().lower(),
                    "total": float(total or 0),
                    "currency": row.get(mapping.get("currency","currency"), "ARS"),
                })
        return out

    def parse_inventory(self, csv_path: str) -> List[Dict[str, Any]]:
        mapping = _load_mapping().get("inventory", {})
        out = []
        with open(csv_path, newline="", encoding="utf-8") as f:
            r = csv.DictReader(f)
            for row in r:
                out.append({
                    "sku": row.get(mapping.get("sku","sku")),
                    "title": row.get(mapping.get("title","title")),
                    "stock": int((row.get(mapping.get("stock","stock")) or 0)),
                })
        return out
