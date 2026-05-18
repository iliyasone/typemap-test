from typing import TYPE_CHECKING, Literal, cast

import typemap_extensions as typing
from typemap.type_eval import eval_typing, format_helper


class Mapped[T]:
    pass


def mapped_column[T]() -> Mapped[T]:
    return cast(Mapped[T], object())


type ColumnType[T] = typing.GetArg[T, Mapped, Literal[0]]

type RowValues[T] = typing.NewTypedDict[
    *[
        typing.Member[column.name, ColumnType[column.type], Literal["NotRequired"]]
        for column in typing.Iter[typing.Attrs[T]]
        if typing.IsAssignable[column.type, Mapped]
    ]
]


class Select[T]:
    pass


class Update[T]:
    pass


def select[T](model: type[T]) -> Select[T]:
    return Select()


def update[T](model: type[T]) -> Update[T]:
    return Update()


# Dict-shaped because the current mypy prototype does not yet accept
# Unpack[RowValues[T]] for dependent **kwargs.
def filter_by[T](stmt: Select[T], values: RowValues[T]) -> Select[T]:
    return stmt


def values[T](stmt: Update[T], new_values: RowValues[T]) -> Update[T]:
    return stmt


class User:
    id: Mapped[int] = mapped_column()
    name: Mapped[str] = mapped_column()
    age: Mapped[int] = mapped_column()


if TYPE_CHECKING:
    where_values: RowValues[User] = {"name": "Ada"}
    update_values: RowValues[User] = {"age": 42}

    reveal_type(where_values)
    reveal_type(filter_by(select(User), where_values))
    reveal_type(values(update(User), update_values))

    # These are rejected by the proposed type:
    # bad_value_type: RowValues[User] = {"name": 123}
    # bad_key: RowValues[User] = {"does_not_exist": True}


if __name__ == "__main__":
    row_values = eval_typing(RowValues[User])
    print(format_helper.format_class(row_values))
    print(f"optional keys: {sorted(row_values.__optional_keys__)}")
