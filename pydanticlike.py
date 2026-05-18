from typing import TYPE_CHECKING, cast

from pydantic import BaseModel

import typemap_extensions as typing


type ModelDump[T] = typing.NewTypedDict[
    *[typing.Member[field.name, field.type] for field in typing.Iter[typing.Attrs[T]]]
]


class User(BaseModel):
    id: int
    name: str


class PlainUser:
    id: int
    name: str


def model_dump[T](model: T) -> ModelDump[T]:
    return cast(ModelDump[T], model.__dict__)


if TYPE_CHECKING:
    user = User(id=1, name="Ada")

    reveal_type("===== EXISTING TYPES =====")
    # Current Pydantic: model_dump() returns dict[str, Any].
    dump = user.model_dump()
    reveal_type(dump)
    reveal_type(dump["id"])

    # Not rejected today, because both expressions are Any.
    missing = dump["ids"]
    wrong_type: int = dump["name"]

if TYPE_CHECKING:
    # Proposed source-level return type:
    # def model_dump[T](model: T) -> ModelDump[T]
    #
    # The same alias works for a normal annotated class. The current typemap
    # runtime crashes on ModelDump[User] because Attrs[User] walks through
    # Pydantic BaseModel internals.

    reveal_type("===== TYPES FOR PlainUser =====")
    plain_user = PlainUser()
    typed_dump = model_dump(plain_user)
    reveal_type(typed_dump)
    reveal_type(typed_dump["id"])
    reveal_type(typed_dump["name"])

    # Rejected by the proposed type.
    typed_missing = typed_dump["ids"]
    typed_wrong_type: int = typed_dump["name"]


if __name__ == "__main__":
    from typemap.type_eval import eval_typing
    from typemap.type_eval import format_helper, eval_call_with_types

    user = PlainUser()

    print(eval_call_with_types(model_dump, user))
