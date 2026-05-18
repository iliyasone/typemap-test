from typing import TYPE_CHECKING, ReadOnly, TypedDict, cast

import typemap_extensions as typing
from typemap.type_eval import eval_call_with_types, format_helper


class FieldArgs(TypedDict, total=False):
    default: ReadOnly[object]
    alias: ReadOnly[str]


class Field[T: FieldArgs](typing.InitField[T]):
    pass


type ModelDump[T] = typing.NewTypedDict[
    *[typing.Member[field.name, field.type] for field in typing.Iter[typing.Attrs[T]]]
]


class BaseModel:
    def model_dump[T: BaseModel](self: T) -> ModelDump[T]:
        return cast(ModelDump[T], self.__dict__)


class User(BaseModel):
    id: int = Field(default=0)
    name: str

# TODO: implement for real Pydantic types

if TYPE_CHECKING:
    user = User()
    dump = user.model_dump()

    reveal_type(dump)
    reveal_type(dump["id"])
    reveal_type(dump["name"])

    # These are rejected by the proposed type:
    missing = dump["ids"]
    wrong_type: int = dump["name"]


if __name__ == "__main__":
    model_dump_return = eval_call_with_types(BaseModel.model_dump, User)
    print(format_helper.format_class(model_dump_return))
