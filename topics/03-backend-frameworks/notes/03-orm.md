# 03 — ORM: Librarian Who Speaks Python (SQLAlchemy + friends)

Raw SQL is cooking on open fire. An ORM is a librarian: you ask in Python, it fetches/translates, tracks changes, and files migrations.

## 1. Core pieces (SQLAlchemy 2.0 style)

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, Session


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    orders: Mapped[list["Order"]] = relationship(back_populates="user", lazy="selectin")
```

- **Engine** = road to DB (pool inside!). **Session** = shopping basket: `add()` collects, `commit()` pays once (unit-of-work), `rollback()` on error. **Never share a Session across requests** — one per request via DI (`get_db` yields + closes).
- **Relationships**: `user.orders` (one→many), `back_populates` both sides. **Lazy loading trap**: `lazy="select"` fires 1 query per user in a loop = **N+1** (topic 02's GraphQL twin!). Fix: `selectin`/`joinedload` — 100 users' orders in 2 queries. Demo in `../examples/03_sqlalchemy_nplus1.py` with a query counter.
- Transactions: `with session.begin():` block commits or rolls back whole basket (money move + ledger insert = atomic).

## 2. Migrations = house renovation log (Alembic / Prisma Migrate / TypeORM)

Never `CREATE TABLE` by hand in prod. Write model → `alembic revision --autogenerate` → review SQL → `alembic upgrade head`. Review the diff like code! Rollback = `downgrade`. CI runs migrations, never app startup racing (one migrator job!).

## 3. Repository = friendly counter (hides SQL from handlers)

```python
class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def get(self, oid):
        return self.db.get(Order, oid)

    def create(self, **kw):
        o = Order(**kw)
        self.db.add(o)
        self.db.commit()
        return o
```

Handler takes `repo=Depends(get_repo)` → unit tests pass a fake repo (no DB!). Same pattern in Prisma (`prisma.order.findMany`), TypeORM (`repo.find({relations})`), Sequelize.

## 4. Survival rules

- Pool sized (`pool_size=10, max_overflow=20`) + `PgBouncer` in prod; `pool_pre_ping=True` kills dead connections.
- `IntegrityError` → `409 Conflict` (duplicate email), never 500. `commit` per request, `rollback` on exception, `close` always (DI `finally`).
- JSONB (`pgvector` later!) for flexible LLM metadata; indexes on FK + filter columns (`EXPLAIN` in topic 06).

One-liner: **"Session per request, eager-load loops (kill N+1), migrate like code, repo hides SQL."**
