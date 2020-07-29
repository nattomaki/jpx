from datetime import datetime

__all__ = ["date2iso"]


def date2iso(value):
    fmt = {4: "%y%m", 6: "%y%m%d", 7: "%Y-%m", 8: "%Y%m%d", 10: "%Y-%m-%d"}
    x = datetime.strptime(value, fmt.get(len(value)))
    return x.isoformat()
