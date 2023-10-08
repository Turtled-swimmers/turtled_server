from datetime import date, datetime, timedelta


async def create_monthly_history(time_filter: str):
    # Create user monthly history list
    def get_dates_in_month(year: int, month: int):
        # Initialize the start date for the given month & Calculate the number of days in the month
        start_date = datetime(year, month, 1)
        next_month = start_date.replace(day=28) + timedelta(days=4)
        last_day = (next_month - timedelta(days=next_month.day)).day

        return int(last_day)

    year_filter, month_filter = (int(_filter) for _filter in time_filter.split("-"))
    date_field = {}

    first_date_of_month = date(year_filter, month_filter, 1)
    end_day_of_month = get_dates_in_month(int(year_filter), int(month_filter))
    end_date_of_month = date(year_filter, month_filter, end_day_of_month)

    current_date = first_date_of_month
    for _ in range(first_date_of_month.day, end_date_of_month.day + 1):
        date_field[current_date.strftime("%Y-%m-%d")] = False
        current_date += timedelta(days=1)

    return {calendar_date: has_event for calendar_date, has_event in date_field.items()}
