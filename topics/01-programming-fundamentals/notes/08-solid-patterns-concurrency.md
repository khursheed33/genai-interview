# 08 — SOLID, DRY/KISS/YAGNI, Patterns, Concurrency

## 1. Principles = house rules (with real examples)

- **DRY:** Don't Repeat Yourself. 3rd copy-paste → extract function. Ex: one `charge(order)` used by UPI/card, not two copies.
- **KISS:** Keep It Simple. A plain `if` beats clever one-liner nobody debugs at 2 AM.
- **YAGNI:** You Aren't Gonna Need It. Don't build "future admin panel" before first user pays.

**SOLID** (one line each, Swiggy example):
- **S**ingle Responsibility: `Order` stores items; `BillPrinter` prints; `PaymentGateway` charges. One reason to change.
- **O**pen/Closed: add `CODPayment` without editing `Checkout` — via interface/Strategy.
- **L**iskov: any `Payment` subclass must work where `Payment` expected (no surprise exceptions).
- **I**nterface Segregation: `Bird(fly)` vs `Penguin` — don't force `fly()` on penguin; split `Walker`/`Flyer`.
- **D**ependency Inversion: `Checkout` depends on `Payment` *interface*, not `Razorpay` class. Inject mock in tests, real in prod. This is **Dependency Injection**.

## 2. Patterns = ready-made recipes (know when, not just how)

| Pattern | Kid story | Real use |
|---|---|---|
| Singleton | One class monitor | DB pool, config, logger (careful in tests — use DI instead) |
| Factory | Vending machine: press button, get toy | `make_llm("openai"/"ollama")`, payment gateway picker |
| Builder | Thali builder: add roti/sabzi step by step | SQL/RAG pipeline builder, `QueryBuilder` |
| Adapter | Plug converter (US→India) | Wrap legacy `OldPay` to new `pay(amount)` interface; S3→GCS |
| Decorator | Extra cheese layer | `@cache`, `@retry`, Express middleware |
| Strategy | Different routes to school | `UPIPay` vs `CardPay`, rerankers swap |
| Observer | Class group broadcast | EventEmitter, Kafka consumer, React state subscribe |
| Repository | Librarian who knows where books are | `OrderRepo.get(id)` hides SQL/Mongo; easy to mock |
| DI | Tiffin delivered, not cooked by you | FastAPI `Depends(get_db)`, pass `llm_client` into Agent |

Python Observer in 10 lines with list of callbacks; Strategy with dict of functions is often enough (no class needed).

## 3. Concurrency bugs = two kids, one chocolate

- **Race condition:** A reads balance 100, B reads 100, both +50, both write 150 (should be 200). Lost update. Fix: `Lock` / atomic op / DB transaction.
- **Deadlock:** A holds spoon waits fork, B holds fork waits spoon — both wait forever. Fix: lock ordering, timeouts (`lock.acquire(timeout=2)`), avoid nested locks.
- **Lock:** bathroom key — one at a time. **Semaphore(n):** auto with n seats — max 10 parallel LLM calls. **Thread-safe:** safe when many cooks touch (use `queue.Queue`, locks, immutable).
- Python: `threading.Lock`, `asyncio.Semaphore(10)`, `queue.Queue` (thread-safe), `multiprocessing.Queue` for processes.

```python
import threading

lock = threading.Lock()
balance = 100


def add():
    global balance
    for _ in range(1000):
        with lock:  # without this, final < 2100 randomly
            balance += 1
```

**Interview lines:** "Race = timing-dependent wrong result; deadlock = circular wait." / "Prefer DI + Strategy + Repository for testable GenAI services."
