import calendar
import datetime


def get_calendar():

    # Create dict for calendar ("month": [1, 2, 3, etc])
    vertical_calendar = {}

    # Get the current year, month and month 6 months back and set "last six month" (lsm) to current year
    current_year = datetime.datetime.now().year
    current_month = datetime.datetime.now().month
    last_six_month = current_month - 6
    lsm_year = current_year

    # If 6 months prior goes into previous year
    if last_six_month < 1:
        last_six_month = last_six_month + 12
        lsm_year = current_year - 1

    # Loop over the months and print the days
    for i in range(1, 7):
        last_six_month += 1

        # Reset if month goes into new year
        if last_six_month > 12:
            last_six_month = last_six_month - 12
            lsm_year = current_year

        # Get the number of days in the month
        days_in_month = calendar.monthrange(lsm_year, last_six_month)[1]
        
        # Get the month name from 6 months back
        month_name = calendar.month_name[last_six_month]

        # Format the name for the vertical calendar dict
        month_year = month_name[:3] + " " + str(lsm_year)
   
        # Create days dict to be inside vertical_calendar dict
        days_dict = {}

        for day in range(1, days_in_month+1):
            vertical_calendar[month_year] = {day, ""}
            days_dict[day] = ""

        # Add key (first 3 lettes of month) and blank list to dict
        vertical_calendar[month_year] = days_dict

    return vertical_calendar


get_calendar()
