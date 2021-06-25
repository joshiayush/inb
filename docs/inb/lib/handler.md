# `CommandHandler()`

Function `CommandHandler()` is going to take in the `argparse.Namespace` and will decide what command is executed and what functions
with what parameters are need to be invoked.

**Prototype:**

```python3
def CommandHandler(namespace: argparse.Namespace) -> None:
```

In order to make `CommandHandler()` design more understandable, flexible, and maintainable we are going to strictly make use of **SOLID**'s [_Open-closed_][_openclosed_principle] concept.

<!-- Definitions -->

[_openclosed_principle]: https://en.wikipedia.org/wiki/Open%E2%80%93closed_principle
