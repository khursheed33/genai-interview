# 02 — Normalization: One Truth, Many Views (1NF → BCNF + when to break it)

## 1. The mess (one giant register)

```
orders_flat(order_id, customer, phone, items_csv, city, city_pin)
1 | Asha | 999 | "dosa,idli" | Blr | 560001
2 | Asha | 999 | "poha"      | Blr | 560001   <- Asha's phone/city copied twice!
```

Update phone once → miss a row → half-truths. That's an **anomaly** (update/delete/insert).

## 2. The ladder (each step deletes a copy)

- **1NF**: atomic cells, no lists — split `items_csv` into rows (`order_items`), one value per cell.
- **2NF**: no partial dependency (whole key!) — `city_pin` depends on `city`, not full `(order_id,item)` → move cities to own table.
- **3NF**: no transitive rides — `customer → city → pin` chain? `city` table holds `pin`, orders point at customer only.
- **BCNF**: every decider is a key (strict 3NF — exam favorite, rarely changes design in practice).

Result: `customers(id, name, phone)`, `orders(id, customer_id)`, `order_items(order_id, item)`, `cities(...)`. One fact lives in ONE place.

## 3. Denormalize on purpose (read-fast copies, write-carefully!)

JOINs cost at 10k RPS → keep a **read model**: `order_summary(order_id, customer_name, total)` refreshed by trigger/job (topic 03's trigger + topic 08's outbox!). Rule: **normalize writes (truth), denormalize reads (speed) — and NAME the sync job** (else copies rot silently).

- GenAI parallels: chunk `metadata` duplicated per embedding row (denormalized for filter speed!); materialized search indexes; CQRS read models (topic 08/10).

Demo both directions with row counts: `../examples/02_normalization.py`.
