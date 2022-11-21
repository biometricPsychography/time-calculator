def add_time(start, duration, day_of_week=None):
    days_of_week_list = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    start = start.strip()
    duration = duration.strip()
    start = start.upper()
    duration = duration.upper()

    if day_of_week :
        day_of_week = day_of_week.lower()


    days_of_week_num_dict = {
        'monday': 0,
        'tuesday': 1,
        'wednesday': 2,
        'thursday': 3,
        'friday': 4,
        'saturday': 5,
        'sunday': 6
    }

    if day_of_week :
        day_of_week_num = days_of_week_num_dict[day_of_week]



    if len(start) == 7 :
        start_hour = int(start[0])
        start_min = int(start[2:4])
        start_am_pm_indicator = start[5:7]
    elif len(start) == 8 :
        start_hour = int(start[0:2])
        start_min = int(start[3:5])
        start_am_pm_indicator = start[6:8]

    if start_am_pm_indicator == 'AM' :
        #tfht will indicate 24 hour time or 'military time' for brevity's sake
        tfht_start_hour = start_hour
    elif start_am_pm_indicator == 'PM' :
        if start_hour != 12 :
            tfht_start_hour = start_hour + 12
        elif start_hour == 12 :
            tfht_start_hour = 12

    dur_list = duration.split(':')
    dur_hour = int(dur_list[0])
    dur_min = int(dur_list[1])

    # handle sum of minutes being one hour or greater
    min_sum = start_min + dur_min
    final_min_value = min_sum % 60
    if min_sum > 59 :
        # note: int truncates towards zero
        hour_supplement = int(min_sum / 60)
    else :
        hour_supplement = 0

    sum_dict = {
        'hour': tfht_start_hour + dur_hour + hour_supplement,
        'min': final_min_value
    }

    # Calculating for final_day_dict 
    number_of_days_passed = int(sum_dict['hour'] / 24)
    tfht_hour_of_end_day = sum_dict['hour'] % 24

    if tfht_hour_of_end_day == 0 :
        twelveht_hour_of_end_day = 12
        end_am_pm_indicator = 'AM'
    elif tfht_hour_of_end_day < 12 :
        # twelveht indicates twelve hour time
        twelveht_hour_of_end_day = tfht_hour_of_end_day
        end_am_pm_indicator = 'AM'
    elif tfht_hour_of_end_day == 12 :
        twelveht_hour_of_end_day = tfht_hour_of_end_day
        end_am_pm_indicator = 'PM'
    else :
        twelveht_hour_of_end_day = tfht_hour_of_end_day - 12
        end_am_pm_indicator = 'PM'


    if number_of_days_passed == 0 : 
        day_count_string = ''
    elif number_of_days_passed == 1 :
        day_count_string = ' (next day)'
    else :
        day_count_string = f' ({number_of_days_passed} days later)'

    if day_of_week and number_of_days_passed != 0 :
        potential_index = (days_of_week_num_dict[day_of_week] + number_of_days_passed % 7)
        if potential_index == 7 :
            potential_index = 0
        end_day = days_of_week_list[potential_index]
    elif day_of_week :
        end_day = days_of_week_list[days_of_week_num_dict[day_of_week]]
    else :
        end_day = ''

    if sum_dict['min'] < 10 :
        padded_min = '0' + str(sum_dict['min'])
    else : 
        padded_min = str(sum_dict['min'])

    final_day_dict = {
        'hour': twelveht_hour_of_end_day,
        'min': sum_dict['min'],
        'padded_min': padded_min,
        'am_pm': end_am_pm_indicator,
        'day': end_day,
        'day_count_string': '' + day_count_string
    }

    if final_day_dict['day'] == '' :
        final_string = (f'{final_day_dict["hour"]}:{final_day_dict["padded_min"]} '
        f'{final_day_dict["am_pm"]}{day_count_string}')
    else :
        final_string = (f'{final_day_dict["hour"]}:{final_day_dict["padded_min"]} '
        f'{final_day_dict["am_pm"]}, {final_day_dict["day"]}{day_count_string}')
    
    print(final_day_dict)
    print(final_string)
    return final_string

# add_time('3:00 PM', '24:09', 'Friday')
# add_time('12:00 PM', '3:09')

# 'Expected calling "add_time()" 
# with "11:59 PM", "24:05" to return "12:04 AM (2 days later)"')

add_time("11:59 PM", "24:05")