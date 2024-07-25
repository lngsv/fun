import argparse
import datetime
import json
from typing import Optional

from pydantic import BaseModel


class Parameters(BaseModel):
    schedule_csv: str
    static_input_csv: Optional[str]
    from_date: datetime.date
    to_date: datetime.date
    initial_balance: int
    output_csv: Optional[str]


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--schedule-csv")
    parser.add_argument("--static-input-csv")
    parser.add_argument("--from-date", type=datetime.date.fromisoformat)
    parser.add_argument("--to-date", type=datetime.date.fromisoformat)
    parser.add_argument("--initial-balance", type=int, default=0)
    parser.add_argument("-o", "--output-csv")
    parser.add_argument(
        "-c",
        "--config",
        help="JSON file with the parameters, has higher priority that command line arguments",
    )
    return parser.parse_args()


def get_parameters() -> Parameters:
    args = parse_args()

    config = {}
    if args.config:
        with open(args.config) as config_file:
            config = json.load(config_file)

    return Parameters(
        schedule_csv=config.get("schedule_csv", args.schedule_csv),
        static_input_csv=config.get("static_input_csv", args.static_input_csv),
        from_date=config.get("from_date", args.from_date),
        to_date=config.get("to_date", args.to_date),
        initial_balance=config.get("initial_balance", args.initial_balance),
        output_csv=config.get("output_csv", args.output_csv),
    )
