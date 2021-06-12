from typing import Any

from functools import singledispatch


@singledispatch
def parse(args: Any):
    raise NotImplemented(f"{type(args)} is not implement yet!")


@parse.register
def _(arg: str = '') -> list:
    print(arg)


@parse.register
def _(args: list = []) -> list:
    print(args)

