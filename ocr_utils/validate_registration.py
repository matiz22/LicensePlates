import re

_PATTERNS = [
    r'^[A-Z]{2}(?!0{5})\d{5}$',
    r'^[A-Z]{2}(?!0{4})\d{4}[A-Z]$',
    r'^[A-Z]{2}(?!0{3})\d{3}[A-Z]{2}$',
    r'^[A-Z]{2}[1-9][A-Z](?!0{3})\d{3}$',
    r'^[A-Z]{2}[1-9][A-Z]{2}(?!0{2})\d{2}$',
    r'^[A-Z]{3}[A-Z](?!0{3})\d{3}$',
    r'^[A-Z]{3}(?!0{2})\d{2}[A-Z]{2}$',
    r'^[A-Z]{3}[1-9][A-Z](?!0{2})\d{2}$',
    r'^[A-Z]{3}(?!0{2})\d{2}[A-Z][1-9]$',
    r'^[A-Z]{3}[1-9][A-Z]{2}[1-9]$',
    r'^[A-Z]{3}[A-Z]{2}(?!0{2})\d{2}$',
    r'^[A-Z]{3}(?!0{5})\d{5}$',
    r'^[A-Z]{3}(?!0{4})\d{4}[A-Z]$',
    r'^[A-Z]{3}(?!0{3})\d{3}[A-Z]{2}$',
    r'^[A-Z]{3}[A-Z](?!0{2})\d{2}[A-Z]$',
    r'^[A-Z]{3}[A-Z][1-9][A-Z]{2}$',
    r'^[A-Z](?!0{3})\d{3}$',
    r'^[A-Z](?!0{2})\d{2}[A-Z]$',
    r'^[A-Z][1-9][A-Z][1-9]$',
    r'^[A-Z]{2}(?!0{2})\d{2}$',
    r'^[A-Z][1-9][A-Z]{2}$',
    r'^[A-Z]{3}[1-9]$',
    r'^[A-Z]{2}[1-9][A-Z]$',
]

_COMPILED_PATTERNS = [re.compile(p) for p in _PATTERNS]

def validate_registration(plate: str) -> bool:
    plate = plate.upper()

    for regex in _COMPILED_PATTERNS:
        if regex.match(plate):
            return True
    return False
