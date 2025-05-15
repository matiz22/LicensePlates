import re

_PATTERNS = [
    # Powiaty dwuliterowe
    r'^[A-Z]{2}(?!0{5})\d{5}$',               # I zasób: 2 litery + 5 cyfr (00001-99999)
    r'^[A-Z]{2}(?!0{4})\d{4}[A-Z]$',          # II zasób: 2 litery + 4 cyfry (0001-9999) + 1 litera
    r'^[A-Z]{2}(?!0{3})\d{3}[A-Z]{2}$',       # III zasób: 2 litery + 3 cyfry (001-999) + 2 litery
    r'^[A-Z]{2}[1-9][A-Z](?!0{3})\d{3}$',     # IV zasób: 2 litery + 1 cyfra (!=0) + 1 litera + 3 cyfry (001-999)
    r'^[A-Z]{2}[1-9][A-Z]{2}(?!0{2})\d{2}$',  # V zasób: 2 litery + 1 cyfra (!=0) + 2 litery + 2 cyfry (01-99)

    # Powiaty trzyliterowe
    r'^[A-Z]{3}[A-Z](?!0{3})\d{3}$',          # I zasób: 3 litery + 1 litera + 3 cyfry (001-999)
    r'^[A-Z]{3}(?!0{2})\d{2}[A-Z]{2}$',       # II zasób: 3 litery + 2 cyfry (01-99) + 2 litery
    r'^[A-Z]{3}[1-9][A-Z](?!0{2})\d{2}$',     # III zasób: 3 litery + 1 cyfra (!=0) + 1 litera + 2 cyfry (01-99)
    r'^[A-Z]{3}(?!0{2})\d{2}[A-Z][1-9]$',     # IV zasób: 3 litery + 2 cyfry (01-99) + 1 litera + 1 cyfra (!=0)
    r'^[A-Z]{3}[1-9][A-Z]{2}[1-9]$',          # V zasób: 3 litery + 1 cyfra (!=0) + 2 litery + 1 cyfra (!=0)
    r'^[A-Z]{3}[A-Z]{2}(?!0{2})\d{2}$',       # VI zasób: 3 litery + 2 litery + 2 cyfry (01-99)
    r'^[A-Z]{3}(?!0{5})\d{5}$',               # VII zasób: 3 litery + 5 cyfr (00001-99999)
    r'^[A-Z]{3}(?!0{4})\d{4}[A-Z]$',          # VIII zasób: 3 litery + 4 cyfry (0001-9999) + 1 litera
    r'^[A-Z]{3}(?!0{3})\d{3}[A-Z]{2}$',       # IX zasób: 3 litery + 3 cyfry (001-999) + 2 litery
    r'^[A-Z]{3}[A-Z](?!0{2})\d{2}[A-Z]$',     # X zasób: 3 litery + 1 litera + 2 cyfry (01-99) + 1 litera
    r'^[A-Z]{3}[A-Z][1-9][A-Z]{2}$',          # XI zasób: 3 litery + 1 litera + 1 cyfra (!=0) + 2 litery

    # Tablice zmniejszone
    r'^[A-Z](?!0{3})\d{3}$',                  # I zasób: 1 litera + 3 cyfry (001-999)
    r'^[A-Z](?!0{2})\d{2}[A-Z]$',             # II zasób: 1 litera + 2 cyfry (01-99) + 1 litera
    r'^[A-Z][1-9][A-Z][1-9]$',                 # III zasób: 1 litera + 1 cyfra (!=0) + 1 litera + 1 cyfra (!=0)
    r'^[A-Z]{2}(?!0{2})\d{2}$',               # IV zasób: 1 litera + 1 litera + 2 cyfry (01-99)
    r'^[A-Z][1-9][A-Z]{2}$',                   # V zasób: 1 litera + 1 cyfra (!=0) + 2 litery
    r'^[A-Z]{3}[1-9]$',                        # VI zasób: 1 litera + 2 litery + 1 cyfra (!=0)
    r'^[A-Z]{2}[1-9][A-Z]$',                   # VII zasób: 1 litera + 1 litera + 1 cyfra (!=0) + 1 litera
]

_COMPILED_PATTERNS = [re.compile(p) for p in _PATTERNS]

def validate_registration(plate: str) -> bool:
    """
    Sprawdza, czy podany tekst (bez spacji) jest prawidłowym wzorem numeru rejestracyjnego
    zgodnie z tablicami standardowymi powiatów (2- i 3-literowych) oraz tablicami zmniejszonymi.

    :param plate: tekst rejestracji, bez spacji
    :return: True jeśli pasuje do dowolnego wzorca, False w przeciwnym razie
    """
    plate = plate.upper()

    for regex in _COMPILED_PATTERNS:
        if regex.match(plate):
            return True
    return False
