from typing import TYPE_CHECKING

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str


if TYPE_CHECKING:
    user = User(id=1, name="Ada")

    # Current Pydantic: model_dump() returns dict[str, Any].
    dump = user.model_dump()
    reveal_type(dump)
    reveal_type(dump["id"])

    # Not rejected today, because both expressions are Any.
    missing = dump["ids"]
    wrong_type: int = dump["name"]


if __name__ == "__main__":
    user = User(id=1, name="Ada")
    dump = user.model_dump()

    print(f"model_dump(): {dump!r}")
    print(f"name has runtime type: {type(dump['name']).__name__}")

    try:
        dump["ids"]
    except KeyError as exc:
        print(f"missing key at runtime: {exc!r}")
