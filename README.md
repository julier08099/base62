# base62

Encode non-negative integers as short, URL-safe base62 strings and decode them back.

```python
from base62 import encode, decode

encode(100000)   # -> 'q0U'
decode('q0U')     # -> 100000
```

## Why

Short-URL and ID-obfuscation services need compact identifiers that survive
being pasted into URLs, typed by humans, and stored in fixed-width columns.
Base62 (0-9A-Za-z) is denser than base16 and avoids the URL-unsafe characters
of base64 (+, /, =). The trade-off vs. base64 is two extra characters per
identifier on average and no standard padding scheme — acceptable for IDs
that are already short.

## Edge cases

- `encode(0)` returns `"0"`, not `""`. An empty identifier is almost always
  a bug at the call site, so zero is given an explicit representation.
- Only non-negative integers are accepted. Negative inputs raise `ValueError`;
  there is no leading-sign convention.
- `bool` is rejected by `encode` even though it subclasses `int`, because
  silently encoding `True` as `"1"` is a common source of bugs.
- `decode("")` raises `ValueError`; there is no valid zero-length encoding.

## Exports

- `encode(n: int) -> str`
- `decode(s: str) -> int`
- `CHARSET` — the 62-character alphabet string, in case callers want to
  build their own formatting on top.

## Running the tests

```
PYTHONPATH=src python -m unittest discover -s tests
```
