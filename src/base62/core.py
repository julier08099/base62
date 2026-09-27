"""Base62 encoding for non-negative integers.

The alphabet is 0-9A-Za-z, giving 62 symbols. This is the conventional
ordering used by short-URL services and database ID obfuscators; it sorts
lexicographically by digit value, which makes encoded strings comparable
only within the same length (a property this library does not rely on but
does not break).

Only non-negative integers are supported. Negative integers have no useful
representation here — the goal is short URL-safe identifiers, not arbitrary
signed transport — and attempting to encode one raises ValueError rather
than silently producing a leading '-' that callers would have to strip.
"""

CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"


def encode(n: int) -> str:
    """Encode a non-negative integer as a base62 string.

    Zero encodes as "0", not the empty string, so round-tripping zero is
    stable and the output is never empty (an empty identifier is almost
    always a bug at the call site).

    Raises ValueError if n is negative or not an int.
    """
    if not isinstance(n, int) or isinstance(n, bool):
        raise ValueError("encode() requires an int")
    if n < 0:
        raise ValueError("encode() requires a non-negative integer")
    if n == 0:
        return "0"
    digits = []
    while n:
        n, r = divmod(n, 62)
        digits.append(CHARSET[r])
    return "".join(reversed(digits))


def decode(s: str) -> int:
    """Decode a base62 string back to the original integer.

    Raises ValueError on an empty string or any character outside CHARSET.
    The lookup is a prebuilt dict so per-character decode is O(1) rather
    than O(62) per call; the table is small and built once at import.
    """
    if not isinstance(s, str):
        raise ValueError("decode() requires a str")
    if not s:
        raise ValueError("decode() received an empty string")
    _lookup = _CHARSET_INDEX
    total = 0
    for ch in s:
        v = _lookup.get(ch)
        if v is None:
            raise ValueError(f"invalid base62 character: {ch!r}")
        total = total * 62 + v
    return total


_CHARSET_INDEX = {c: i for i, c in enumerate(CHARSET)}
