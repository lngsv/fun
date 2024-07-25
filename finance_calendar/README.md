# finance calendar

```shell
py -m venv venv
source venv/bin/activate
pip install -e finance_calendar
pip install -e "finance_calendar[dev]"

fincalendar -h
fincalendar --from-date 2024-07-01 --to-date 2024-07-31 --schedule-csv finance_calendar/db/init.csv --output-csv finance_calendar/db/out.csv --static-input-csv finance_calendar/db/out.csv
fincalendar -c config.json
```
