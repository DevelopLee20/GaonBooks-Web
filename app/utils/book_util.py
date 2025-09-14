import re


class BookUtil:
    @classmethod
    def clean_integer_fields(cls, v) -> int:
        if isinstance(v, str):
            # Extracts only digits from the string.
            digits = re.sub(r"\D", "", v)
            if digits:
                try:
                    return int(digits)
                except Exception:
                    return 0
        return 0
