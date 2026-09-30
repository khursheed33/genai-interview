"""Solution: repo hides SQL; selectinload kills N+1; IntegrityError -> 409."""

from sqlalchemy import ForeignKey, String, create_engine, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    Session,
    mapped_column,
    relationship,
    selectinload,
)
from sqlalchemy.pool import StaticPool


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(120), unique=True)
    orders: Mapped[list["Order"]] = relationship(back_populates="user")


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    item: Mapped[str] = mapped_column(String(50))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    user: Mapped[User] = relationship(back_populates="orders")


def make_session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return Session(engine), engine


def to_status(exc):
    return 409 if isinstance(exc, IntegrityError) else 500


class UserRepo:
    def __init__(self, db: Session):
        self.db = db

    def create(self, name, email):
        u = User(name=name, email=email)
        self.db.add(u)
        self.db.commit()
        return u.id

    def get(self, uid):
        u = self.db.get(User, uid)
        return None if u is None else {"id": u.id, "name": u.name, "email": u.email}

    def list_with_orders(self):
        users = self.db.scalars(select(User).options(selectinload(User.orders))).all()
        return [{"name": u.name, "n_orders": len(u.orders)} for u in users]
