# typemap-test

Demo testing repo for the PEP 827 prototypes:
- [typemap runtime (@iliyasone fork)](https://github.com/iliyasone/python-typemap.git)
- [mypy prototype](https://github.com/msullivan/mypy-typemap)

## Plan

Update the typemap prototype types so real **Pydantic** and **SQLAlchemy**
work under PEP 827. The current `typemap_proposal.py` examples in
[typemap-test](https://github.com/iliyasone/typemap-test) use stand-in classes
that mimic `BaseModel` and `Mapped`, because the type adapter doesn't yet
handle the real library classes. That's what this work is about.

The reference for what should be caught is the set of `current_gap.py` files
in the same repo. They list **8** cases of code that mypy accepts today and
shouldn't:

**Pydantic (2)**
- `BaseModel.model_dump()` returns `dict[str, Any]`, so field-level precision is lost.
- Accessing a non-existent key on the dump is allowed.

**SQLAlchemy (6)**
- `filter_by(name=123)` accepts wrong value type.
- `filter_by(does_not_exist=True)` accepts unknown column.
- `update(...).values(name=123)` accepts wrong value type.
- `update(...).values(does_not_exist=True)` accepts unknown column.
- `where(User.age == "old")` accepts wrong value type in comparison.
- `select(User).join(Server)` accepts implicit join between unrelated tables.

### Goals

- The runtime evaluator runs against the actual Pydantic and SQLAlchemy classes.
- The full type hierarchy is in place, so the transformations compose with nested generics, inheritance, and overloads.
- Everything that already type-checks in these libraries keeps type-checking.

PEP 827 acceptance becomes a path to first-class language support. The stubs
are useful regardless: we get to see how these types look in real production
code, what problems show up with the existing complicated type system, and
what design updates the PEP might need before it eventually lands, hopefully
in Python 3.16.
## Setup

Requires [uv](https://docs.astral.sh/uv/).

Since everything is under active development, the pyproject.toml
depends on unpinned github repos, and `uv.lock` is gitignored.

```bash
uv sync --upgrade
```

To try out the working typemap transformation example:
```bash
uv run mypy examples/fastapi_like.py
```

```bash
uv run python examples/fastapi_like.py
```

## Library typing gap examples

The `current_gap.py` files use real libraries and show code that mypy accepts
today even though it is suspicious or fails later. The `typemap_proposal.py`
files use small artificial APIs to show the proposed source-level shape in a
form that both mypy and the runtime evaluator can handle today.

```bash
uv run mypy examples/pydantic/current_gap.py
uv run python examples/pydantic/current_gap.py
uv run mypy examples/pydantic/typemap_proposal.py
uv run python examples/pydantic/typemap_proposal.py

uv run mypy examples/sqlalchemy/current_gap.py
uv run python examples/sqlalchemy/current_gap.py
uv run mypy examples/sqlalchemy/typemap_proposal.py
uv run python examples/sqlalchemy/typemap_proposal.py
```

`examples/sqlalchemy/current_gap.py` shows inline SQLAlchemy statements that
are typed today and inline statements that mypy accepts even though they are
suspicious or fail later.

`examples/pydantic/current_gap.py` shows inline `user.model_dump()` code where
current Pydantic returns `dict[str, Any]`, so bad key access and wrong
assignments are accepted.
