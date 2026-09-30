"""03_sqlalchemy_nplus1.py — librarian + the N+1 trap (with query counter).

Run: uv run python topics/03-backend-frameworks/examples/03_sqlalchemy_nplus1.py
"""

from sqlalchemy import ForeignKey, String, create_engine, event, select
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.pool import StaticPool

COUNT = {"n": 0}
engine = create_engine("sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool)


@event.listens_for(engine, "before_cursor_execute")
def count_q(conn, cur, stmt, params, ctx, multiparams):
    COUNT["n"] += 1


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="orders")


Base.metadata.create_all(engine)
with Session(engine) as s:
    for i in range(5):
        u = User(name=f"u{i}")
        s.add(u)
        s.add_all([Order(item=f"dosa-{i}-{j}", user=u) for j in range(2)])
    s.commit()

# NAIVE: 1 (users) + 5 (orders each) = 6 queries
with Session(engine) as s:
    COUNT["n"] = 0
    total = sum(len(u.orders) for u in s.scalars(select(User)))
    naive_q = COUNT["n"]
print("naive queries:", naive_q, "| items:", total)
assert naive_q == 6 and total == 10

# FIXED: selectinload -> 2 queries (users + all orders in one IN (...))
with Session(engine) as s:
    COUNT["n"] = 0
    users = s.scalars(select(User).options(selectinload(User.orders))).all()
    total = sum(len(u.orders) for u in users)
    fixed_q = COUNT["n"]
print("eager queries:", fixed_q)
assert fixed_q == 2 and total == 10


# Repository hides SQL; duplicate email -> caller maps IntegrityError to 409
class OrderRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, item, user_id):
        o = Order(item=item, user_id=user_id)
        self.db.add(o)
        self.db.commit()
        return o.id


with Session(engine) as s:
    assert OrderRepo(s).create("idli", 1) > 0
print("OK — N+1 killed with selectinload; session per request; repo hides SQL")
