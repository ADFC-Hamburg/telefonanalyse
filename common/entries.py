"""Provides a class for phone call list entries."""

from common import strings

from typing import NamedTuple
from datetime import date, time


class PhoneCall(NamedTuple):
    id: int
    duration: int
    date: date
    time: time
    topic: str


COMMA_SEPERATED_ORDER = ','.join((strings.COLUMN.ID,strings.COLUMN.DATE,
                                  strings.COLUMN.TIME,strings.COLUMN.TOPIC,
                                  strings.COLUMN.DURATION))

def comma_seperated(entry:PhoneCall) -> str:
    """Converts a PhoneCall object into a comma seperated string."""
    id = str(entry.id)
    duration = str(entry.duration)
    date = entry.date.strftime('%d.%m.%Y')
    time = entry.time.strftime('%H:%M')
    topic = f'"{entry.topic}"'
    return f'{id},{date},{time},{topic},{duration}'

