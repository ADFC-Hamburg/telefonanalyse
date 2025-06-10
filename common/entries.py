"""Provides a class for phone call list entries."""

from typing import NamedTuple
from datetime import date, time


class PhoneCall(NamedTuple):
    id: int
    duration: int
    date: date
    time: time
    topic: str


COMMA_SEPERATED_ORDER = 'ID,Datum,Uhrzeit,Thema,Dauer'

def comma_seperated(entry:PhoneCall) -> str:
    """Converts a PhoneCall object into a comma seperated string."""
    id = str(entry.id)
    duration = str(entry.duration)
    date = entry.date.strftime('%d.%m.%Y')
    time = entry.time.strftime('%H:%M')
    topic = f'"{entry.topic}"'
    return f'{id},{date},{time},{topic},{duration}'

