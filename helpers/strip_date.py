from datetime import datetime, timezone


def strip_date(date: str, format: str) -> datetime:
    """Create a datetime object from a string date"""
    format = format.upper()

    year_idx = format.find("Y")
    year_count = format.count("Y")
    month_idx = format.find("M")
    month_count = format.count("M")
    day_idx = format.find("D")
    day_count = format.count("D")

    year = int(date[year_idx: year_idx + year_count])
    month = int(date[month_idx: month_idx + month_count])
    day = int(date[day_idx: day_idx + day_count])

    return datetime(year, month, day, tzinfo=timezone.utc)
