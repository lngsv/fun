import argparse
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


# CalendarRow(date='2023-12-30', purpose='purp', price='123', balance=456, override=None)
# table = [list(map(str.capitalize, CalendarRow.model_fields.keys())), CalendarRow(date='2023-12-30', purpose='purp', price=123, balance=456, override=None).model_dump().values()]


def is_last_day_of_month(day: datetime.date):
    return day.day == calendar.monthrange(day.year, day.month)[1]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule-csv", required=True)
    # parser.add_argument("--static-input-csv", required=True)
    parser.add_argument("--from-date", type=datetime.date.fromisoformat, required=True)
    parser.add_argument("--to-date", type=datetime.date.fromisoformat, required=True)
    parser.add_argument("--initial-balance", type=int, default=0)
    parser.add_argument("--output-csv")
    return parser.parse_args()


def read_schedule(schedule_path: str) -> List[ScheduleItem]:
    schedule = []
    with open(schedule_path) as schedule_csv:
        csv_reader = csv.DictReader(schedule_csv)
        for row in csv_reader:
            schedule_row = ScheduleItem(**row)  # type: ignore[arg-type]
            schedule.append(schedule_row)

    return schedule


def to_printable_table(events: List[CalendarRow]):
    return [map(str.capitalize, CalendarRow.model_fields.keys())] + list(
        map(lambda row: row.model_dump().values(), events)
    )


def main():
    args = parse_args()
    schedule = read_schedule(args.schedule_csv)
    table: List[CalendarRow] = to_printable_table(
        [
            CalendarRow(
                date=args.from_date,
                purpose="initial balance",
                price=args.initial_balance,
                balance=args.initial_balance,
            )
        ]
    )

    # TODO parse static file. To dict?
    # Read static, generate within the provided range,
    # sort and deduplicate by (date, purpose), prioritize the overrides
    # Next stage: add validations for the inputs
    balance = args.initial_balance
    for iterator in rrule(DAILY, dtstart=args.from_date, until=args.to_date):
        date = iterator.date()
        for schedule_item in schedule:
            if schedule_item.happens_on(date):
                balance += schedule_item.price
                table.append(
                    CalendarRow(
                        date=date,
                        purpose=schedule_item.purpose,
                        price=schedule_item.price,
                        balance=balance,
                    )
                )

    if args.output_csv:
        print(f"Outputting results to {args.output_csv}")
        with open(args.output_csv, "w") as csvfile:
            writer = csv.writer(csvfile)
            writer.writerows(table)
    else:
        print(tabulate(table, headers="firstrow", tablefmt="grid"))

    return os.EX_OK


if __name__ == "__main__":
    sys.exit(main())
