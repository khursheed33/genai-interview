# 01 — REST Foundations: The Restaurant Menu

Imagine a restaurant. The **menu** lists dishes (resources). You (client) point at item 5 (URI), say "one dosa please" (GET), waiter (HTTP) brings it (representation). You never walk into the kitchen (server internals hidden). That's REST.

## 1. REST = 6 house rules (constraints)

| Rule | Kid story | What it means |
|---|---|---|
| Client-Server | You order, kitchen cooks — separate jobs | UI and server evolve independently |
| Stateless | Waiter has amnesia — every order carries full details | No server session memory; each request has auth + params (scales horizontally) |
| Cacheable | "Same dosa as last time?" — reuse | Responses say `Cache-Control: max-age=60` so clients/CDNs reuse |
| Uniform interface | Same menu format everywhere | Resources (nouns in URI) + methods (verbs) + representations (JSON) + links |
| Layered | Waiter → captain → kitchen — you only see waiter | Proxies/gateways/CDNs invisible to client |
| Code-on-demand (optional) | QR code plays a song | Server sends executable JS — rarely used |

## 2. Resources = nouns, never verbs

- URI names a **thing**, method says the **action**.
- ✅ `GET /orders/101`, `POST /orders`, `GET /orders?status=paid&sort=-created`
- ❌ `GET /getOrder?id=101`, `POST /createOrder`, `GET /orders/getPaid`
- Plurals for collections (`/orders`), singular for singletons (`/profile`), kebab-case (`/order-items`), no trailing verbs, no file extensions.
- Nesting max 2–3 deep: `/orders/101/items` ok; `/users/9/orders/101/items/4/tax` — flatten with query params instead.
- Real world (Swiggy): `POST /orders` (place), `GET /orders/101` (track), `PATCH /orders/101` (change address), `DELETE /orders/101` (cancel before dispatch).

## 3. Methods = the 7 utensils

| Method | Safe? | Idempotent? | Kid story | Use |
|---|---|---|---|---|
| GET | ✅ | ✅ | Read menu, no kitchen change | fetch, search |
| HEAD | ✅ | ✅ | "Is dosa available?" (headers only, no body) | existence/size checks |
| OPTIONS | ✅ | ✅ | "What can I order here?" | CORS preflight, discovery |
| PUT | ❌ | ✅ | Replace full tiffin — doing twice = same tiffin | full replace (`PUT /profile`) |
| DELETE | ❌ | ✅ | Cancel order — cancelling twice, still cancelled | remove (2nd call → 404 but same effect) |
| POST | ❌ | ❌ | Place NEW order — twice = 2 dosas! | create, actions |
| PATCH | ❌ | ❌* | Change address line — depends | partial update |

- **Safe** = never changes server state (read-only). **Idempotent** = repeating N times = same effect as once (matters for retries!).
- ⚠️ Classic trap: "Is DELETE idempotent?" **Yes** — effect (gone) is same; status may differ (200 then 404). "Is PATCH idempotent?" **Only if** operation is (set-address yes, increment-counter no).
- GenAI hook: LLM calls are POST (non-idempotent, billed per call!) → always send `Idempotency-Key` so retries don't double-charge. More in `08-resilience.md`.

## 4. Richardson Maturity Model = levels of restaurant manners

- **L0 — Swamp:** one URI (`POST /api`), all in body (`{"action":"getOrder"}`). That's RPC, not REST.
- **L1 — Resources:** many URIs (`/orders`, `/users`) but only POST/GET misused.
- **L2 — Verbs + status:** proper methods + status codes (`201 Created`, `404`). Most "good" APIs live here.
- **L3 — Hypermedia (HATEOAS):** responses include next-step links so clients don't hardcode flows:

```json
{ "id": 101, "status": "paid",
  "_links": { "self": "/orders/101", "cancel": "/orders/101/cancel", "track": "/tracking/101" } }
```

Real world: Swiggy "track / cancel / reorder" buttons come from links, not app hardcoding. Interview line: **"L2 + links = L3; links decouple client from URL construction."**

## Recap

- Nouns in URI, verbs in methods; stateless + cacheable + layered.
- Safe = read-only; idempotent = repeat-safe (PUT/DELETE yes, POST no).
- L2 is the bar, L3 links future-proof flows. Idempotency keys protect retries (esp. LLM billing).

Next: status codes + errors + versioning + pagination → `02-status-errors-versioning.md`. Runnable: `../examples/01_rest_design.py`.
