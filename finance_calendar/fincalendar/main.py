import calendar
import csv
import datetime
import os
import sys
from enum import StrEnum
from typing import List, Literal, Optional

from dateutil.rrule import DAILY, rrule
from pydantic import BaseModel, model_validator
from tabulate import tabulate
from typing_extensions import Self

from .parameters import get_parameters

INITIAL_BALANCE_PURPOSE = "initial balance"


class EventType(StrEnum):
    LAST_WORKDAY_UNTIL = "last_workday_until"
    MONTHLY = "monthly"
    BIMONTHLY = "bimonthly"


class ScheduleItem(BaseModel):
    event_type: EventType
    day: int
    purpose: str
    price: int
    bimonthly_odd: bool | Literal[""]  # empty string is None from csv reader

    @model_validator(mode="after")
    def _check_bimonthly_odd(self) -> Self:
        if self.event_type == EventType.BIMONTHLY:
            assert isinstance(
                self.bimonthly_odd, bool
            ), "bimonthly_odd expected in the csv for bimonthly event"
        return self

    def _is_today(self, dt: datetime.date) -> bool:
        return dt.day == self.day or is_last_day_of_month(dt) and dt.day < self.day

    def _is_yesterday(self, dt: datetime.date) -> bool:
        next_day = dt + datetime.timedelta(days=1)
        return next_day.day == self.day

    def happens_on(self, dt: datetime.date) -> bool:
        # print(self.purpose, self.day, self.event_type)
        if self.event_type == EventType.MONTHLY:
            return self._is_today(dt)

        if self.event_type == EventType.BIMONTHLY:
            if dt.month % 2 == int(self.bimonthly_odd):
                return self._is_today(dt)
            return False

        if self.event_type == EventType.LAST_WORKDAY_UNTIL:
            if dt.weekday() >= 5:
                return False

            if self._is_today(dt):
                return True

            if dt.weekday() == 4 and (
                self._is_today(dt + datetime.timedelta(days=1))
                or self._is_today(dt + datetime.timedelta(days=2))
            ):
                return True

            return False

        assert False, "unexpected event type"


class CalendarRow(BaseModel):
    date: datetime.date
    purpose: str
    price: int
    balance: int
    override: Optional[int] = None


def is_last_day_of_month(day: datetime.date):
    return day.day == calendar.monthrange(day.year, day.month)[1]


def read_schedule(schedule_path: str) -> List[ScheduleItem]:
    schedule = []
    with open(schedule_path) as schedule_csv:
        csv_reader = csv.DictReader(schedule_csv)
        for row in csv_reader:
            schedule_row = ScheduleItem(**row)  # type: ignore[arg-type]
            schedule.append(schedule_row)

    return schedule


def read_static(static_path: Optional[str]) -> List[CalendarRow]:
    if not static_path:
        return []
    static = []
    with open(static_path) as static_csv:
        csv_reader = csv.DictReader(static_csv)
        for row in csv_reader:
            row = {k.lower(): (None if v == "" else v) for k, v in row.items()}
            static_row = CalendarRow(**row)  # type: ignore[arg-type]
            static.append(static_row)

    return static


def to_printable_table(events: List[CalendarRow]):
    return [map(str.capitalize, CalendarRow.model_fields.keys())] + list(
        map(lambda row: row.model_dump().values(), events)
    )


def main():
    parameters = get_parameters()

    schedule = read_schedule(parameters.schedule_csv)
    static = read_static(parameters.static_input_csv)

    table: List[CalendarRow] = static + [
        CalendarRow(
            date=parameters.from_date,
            purpose=INITIAL_BALANCE_PURPOSE,
            price=parameters.initial_balance,
            balance=parameters.initial_balance,
        )
    ]

    # Next stage: add validations for the inputs

    for iterator in rrule(
        DAILY, dtstart=parameters.from_date, until=parameters.to_date
    ):
        date = iterator.date()
        for schedule_item in schedule:
            if schedule_item.happens_on(date):
                table.append(
                    CalendarRow(
                        date=date,
                        purpose=schedule_item.purpose,
                        price=schedule_item.price,
                        balance=0,
                    )
                )

    # TODO we might have different overrides or prices for the same date and purpose
    table.sort(key=lambda row: row.date)
    assert table[0].purpose == INITIAL_BALANCE_PURPOSE
    current_date, added_purposes = table[0].date, {table[0].purpose}
    filtered_table = [table[0]]
    balance = table[0].balance
    for row in table[1:]:
        if row.purpose == INITIAL_BALANCE_PURPOSE:
            continue

        if row.date == current_date:
            if row.purpose in added_purposes:
                continue
            added_purposes.add(row.purpose)
        else:
            current_date = row.date
            added_purposes = {row.purpose}

        balance += row.price
        row.balance = balance

        if row.override is not None:
            balance = row.override

        filtered_table.append(row)

    printable_table = to_printable_table(filtered_table)

    if parameters.output_csv:
        print(f"Outputting results to {parameters.output_csv}")
        with open(parameters.output_csv, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(printable_table)
    else:
        print(tabulate(printable_table, headers="firstrow", tablefmt="grid"))

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
