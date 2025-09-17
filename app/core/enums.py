from enum import Enum


class MODE(str, Enum):
    prod = "prod"
    dev = "dev"


class STORE_SPOT(str, Enum):
    sch = "sch"
    sunmoon = "sunmoon"
    nasaret = "nasaret"
    kongju = "kongju"
    mokwon = "mokwon"
