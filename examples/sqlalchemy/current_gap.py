from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    age: Mapped[int]


class Post(Base):
    __tablename__ = "post"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    title: Mapped[str]


class Server(Base):
    __tablename__ = "server"

    id: Mapped[int] = mapped_column(primary_key=True)


if TYPE_CHECKING:
    # Typed today: SQLAlchemy 2.0 preserves selected column tuple types.
    reveal_type(select(User.id, User.name))

    # Not rejected today, even though these are suspicious or invalid.
    reveal_type(select(User).filter_by(name=123))
    reveal_type(select(User).filter_by(does_not_exist=True))
    reveal_type(update(User).values(name=123))
    reveal_type(update(User).values(does_not_exist=True))
    reveal_type(select(User).where(User.age == "old"))
    reveal_type(select(User).join(Server))


if __name__ == "__main__":
    cases = {
        "filter_by wrong value type": select(User).filter_by(name=123),
        "update wrong value type": update(User).values(name=123),
        "where wrong value type": select(User).where(User.age == "old"),
    }

    for label, statement in cases.items():
        print(f"{label}: compiles as {statement.compile()}")

    for label, make_statement in {
        "filter_by unknown column": lambda: select(User).filter_by(does_not_exist=True),
        "update unknown column": lambda: update(User).values(does_not_exist=True),
        "implicit unrelated join": lambda: select(User).join(Server),
    }.items():
        try:
            statement = make_statement()
            print(f"{label}: compiles as {statement.compile()}")
        except SQLAlchemyError as exc:
            print(f"{label}: {type(exc).__name__}: {exc}")
