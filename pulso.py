import argparse, logging, yaml
from datetime import datetime, timedelta
from zoneinfo import ZoneInfo

from adapters.csv_generic import CSVGenericAdapter
from adapters.shopify_mock import ShopifyMockAdapter
from senders.email_sender import send_email

def load_cfg():
    with open("config.yml","r",encoding="utf-8") as f:
        return yaml.safe_load(f)

def day_bounds(tz_name: str, for_date: str | None):
    tz = ZoneInfo(tz_name)
    if for_date:
        d0 = datetime.strptime(for_date, "%Y-%m-%d").replace(tzinfo=tz)
    else:
        now = datetime.now(tz)
        d0 = (now - timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
    d1 = d0 + timedelta(days=1)
    return d0, d1

def aggregate(orders, inventory, tz_name: str, threshold: int, for_date: str | None):
    y0, y1 = day_bounds(tz_name, for_date)
    orders_y = [o for o in orders if y0.replace(tzinfo=None) <= o["created_at"] < y1.replace(tzinfo=None)]
    n_total = len(orders_y)
    ingresos = sum(o["total"] for o in orders_y if o["status"] == "paid")
    rech = sum(1 for o in orders_y if o["status"] == "rejected")
    pend = sum(1 for o in orders_y if o["status"] == "pending")
    currency = orders_y[0]["currency"] if orders_y else "ARS"
    low = [it for it in inventory if int(it["stock"]) <= threshold]
    return {
        "fecha": y0.strftime("%Y-%m-%d"),
        "n_total": n_total,
        "ingresos": ingresos,
        "rechazados": rech,
        "pendientes": pend,
        "currency": currency,
        "stock_bajo": [{"sku": it["sku"], "title": it["title"], "stock": it["stock"]} for it in low],
    }

def render_txt(agg, currency_symbol="$"):
    lines = [
        f"Pulso 9 — {agg['fecha']}",
        "",
        f"Pedidos: {agg['n_total']}",
        f"Ingresos: {currency_symbol}{agg['ingresos']:.2f}",
        f"Pendientes: {agg['pendientes']}  |  Rechazados: {agg['rechazados']}",
        "",
        "Stock bajo (<= umbral):",
    ]
    if not agg["stock_bajo"]:
        lines.append("  - Sin alertas")
    else:
        for it in agg["stock_bajo"]:
            lines.append(f"  - {it['sku']} — {it['title']} (stock={it['stock']})")
    return "\n".join(lines)

def main():
    parser = argparse.ArgumentParser(description="Pulso 9 — Public Demo")
    parser.add_argument("--source", choices=["csv","shopify_mock"], required=True)
    parser.add_argument("--orders", required=True)
    parser.add_argument("--inventory", required=True)
    parser.add_argument("--to_email")
    parser.add_argument("--for_date")  # YYYY-MM-DD
    parser.add_argument("--stock_threshold", type=int)
    parser.add_argument("--log-level", default="INFO")

    args = parser.parse_args()
    logging.basicConfig(level=getattr(logging, args.log_level.upper(), logging.INFO),
                        format="%(asctime)s %(levelname)s %(message)s")

    cfg = load_cfg()
    tz = cfg.get("timezone", "America/Argentina/Cordoba")
    threshold = args.stock_threshold or cfg.get("stock_low_threshold_default", 5)

    logging.info("Source: %s", args.source)
    if args.source == "csv":
        adapter = CSVGenericAdapter()
    else:
        adapter = ShopifyMockAdapter()

    logging.info("Reading orders from %s", args.orders)
    orders = adapter.parse_orders(args.orders)

    logging.info("Reading inventory from %s", args.inventory)
    inventory = adapter.parse_inventory(args.inventory)

    agg = aggregate(orders, inventory, tz, threshold, args.for_date)
    body = render_txt(agg)

    logging.info("Report generated for %s", agg["fecha"])
    print(body)

    if args.to_email:
        subject = f"Pulso 9 — {agg['fecha']}"
        send_email(args.to_email, subject, body)

if __name__ == "__main__":
    main()
