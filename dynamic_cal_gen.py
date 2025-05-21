from calendar import monthcalendar, month_name
from datetime import date, datetime, timedelta

def get_week_span(start_date, classes_per_week, class_days, num_weeks):
    """
    Generate a dictionary of dates mapped to their class numbers
    
    Parameters:
    start_date: Start date for the calendar
    classes_per_week: Number of classes to be held per week
    class_days: List of integers representing days (0=Monday, 6=Sunday)
    num_weeks: Total number of weeks to generate
    """
    week_mapping = {}
    current_date = start_date
    current_week = 1
    classes_in_current_week = 0
    
    class_days = sorted(class_days)

    academic_holidays = get_academic_holidays()
    first_class_found = False
    while current_week <= num_weeks:
        if current_date not in academic_holidays:
            day_of_week = current_date.weekday()
            if day_of_week in class_days:
                if first_class_found and classes_in_current_week >= classes_per_week:
                    current_week += 1
                    classes_in_current_week = 0
                    
                week_mapping[current_date] = current_week
                classes_in_current_week += 1
                if current_week==num_weeks and classes_in_current_week==classes_per_week:
                    break
                first_class_found = True
        current_date += timedelta(days=1)
    return week_mapping, current_date

def get_academic_holidays():
    """Return a set of academic holiday dates"""
    holidays_list = [
        # 2025
        date(2025, 9, 1),    # Labor Day
        date(2025, 11, 26),  # Day Before Thanksgiving
        date(2025, 11, 27),  # Thanksgiving
        date(2025, 11, 28),  # Day after Thanksgiving
        # Winter Holiday
        date(2025, 12, 23), date(2025, 12, 24), 
        date(2025, 12, 25), date(2025, 12, 26),
        date(2025, 12, 31),  # New Year's Eve
        # 2026
        date(2026, 1, 1),    # New Year's Day
        # Spring Break
        date(2026, 4, 13), date(2026, 4, 14), date(2026, 4, 15),
        date(2026, 4, 16), date(2026, 4, 17), date(2026, 4, 18),
        date(2026, 5, 25),   # Memorial Day
        date(2026, 7, 4),   # July 4th
        # End of Summer Break
        date(2026, 8, 24), date(2026, 8, 25), date(2026, 8, 26),
        date(2026, 8, 27), date(2026, 8, 28), date(2026, 8, 29)
  
    ]
    return set(holidays_list)

def convert_days_to_indices(days):
    """Convert day names to indices (0-6 for Monday-Sunday)"""
    day_map = {
        'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3,
        'friday': 4, 'saturday': 5, 'sunday': 6
    }
    return [day_map[day.lower()] for day in days]

def generate_class_calendar(start_year, start_month, num_weeks, classes_per_week, class_days):
    start_date = date(start_year, start_month, 1)
    
    class_day_indices = convert_days_to_indices(class_days)
    week_mapping, end_date = get_week_span(start_date, classes_per_week, class_day_indices, num_weeks)
    
    academic_holidays = get_academic_holidays()
    
    current_date = start_date
    months_to_generate = []
    while current_date <= end_date:
        months_to_generate.append((current_date.year, current_date.month))
        if current_date.month == 12:
            current_date = date(current_date.year + 1, 1, 1)
        else:
            current_date = date(current_date.year, current_date.month + 1, 1)

    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            .calendar-container {
                display: flex;
                flex-wrap: wrap;
                gap: 20px;
                padding: 20px;
                font-family: Arial, sans-serif;
            }
            .month {
                width: 300px;
            }
            .month-title {
                background-color: #4a90e2;
                color: white;
                padding: 10px;
                text-align: center;
                font-weight: bold;
            }
            table {
                width: 100%;
                border-collapse: collapse;
            }
            th, td {
                border: 1px solid #ddd;
                padding: 4px;
                text-align: center;
            }
            th {
                background-color: #f2f2f2;
            }
            .highlight {
                background-color: #ffa500;
            }
            .date {
                font-size: 14px;
                margin-bottom: 2px;
            }
            .week-number {
                font-size: 10px;
                color: #ff0000;
            }
            .legends-container {
                display: flex;
                gap: 40px;
                margin: 20px;
                justify-content: flex-start;
            }
            .legend {
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 5px;
            }
            .legend-title {
                font-weight: bold;
                margin-bottom: 10px;
                color: #4a90e2;
            }
            .color-item {
                display: flex;
                align-items: center;
                margin-bottom: 8px;
            }
            .color-box {
                width: 20px;
                height: 20px;
                margin-right: 10px;
                border: 1px solid #ddd;
            }
            .holiday-list {
                columns: 2;
                column-gap: 20px;
            }
            .holiday-item {
                margin-bottom: 8px;
                break-inside: avoid;
            }
        </style>
    </head>
    <body>
    """
    
    html += """
    <div class="legends-container">
        <div class="legend">
            <div class="legend-title">Color Guide</div>
            <div class="color-item">
                <div class="color-box" style="background-color: #ffa500;"></div>
                <span>Holidays and Sundays</span>
            </div>
            <div class="color-item">
                <div class="color-box" style="background-color: white;"></div>
                <span>Regular Days</span>
            </div>
            <div class="color-item">
                <div class="color-box" style="border: none;">
                    <span style="color: #ff0000; font-size: 10px;">1</span>
                </div>
                <span>Week Numbers (in red)</span>
            </div>
        </div>
        
        <div class="legend">
            <div class="legend-title">Academic Holidays</div>
            <div class="holiday-list">
                <div class="holiday-item">• Labor Day: Sep 1, 2025</div>
                <div class="holiday-item">• Thanksgiving: Nov 26 - 28, 2025</div>
                <div class="holiday-item">• Winter Holiday: Dec 23 - 26, 2025</div>
                <div class="holiday-item">• New Year's Eve: Dec 31, 2025</div>
                <div class="holiday-item">• New Year's Day: Jan 1, 2026</div>
                <div class="holiday-item">• Spring Break: Apr 13 - 18, 2026</div>
                <div class="holiday-item">• Memorial Day: May 25, 2026</div>
                <div class="holiday-item">• July 4th : Jul 4, 2026</div>
                <div class="holiday-item">• End of Summer Break: Aug 24 - 31, 2026</div>
            </div>
        </div>
    </div>
    <div class="calendar-container">
    """
    
    for year, month in months_to_generate:
        cal = monthcalendar(year, month)
        
        html += f'<div class="month">'
        html += f'<div class="month-title">{month_name[month]} {year}</div>'
        
        html += '''
        <table>
        <tr>
            <th>Mon</th>
            <th>Tue</th>
            <th>Wed</th>
            <th>Thu</th>
            <th>Fri</th>
            <th>Sat</th>
            <th>Sun</th>
        </tr>
        '''
        
        for week in cal:
            html += '<tr>'
            for day_index, day in enumerate(week):
                if day == 0:
                    html += '<td></td>'
                else:
                    current_date = date(year, month, day)
                    is_holiday = current_date in academic_holidays
                    is_class_day = day_index in class_day_indices
                    
                    week_num = week_mapping.get(current_date, "")
                    
                    classes = []
                    if is_holiday:
                        classes.append('highlight')
                    elif is_class_day:
                        classes.append('class-day')
                    
                    class_str = f' class="{" ".join(classes)}"' if classes else ''
                    
                    html += f'''
                    <td{class_str}>
                        <div class="date">{day}</div>
                        {f'<div class="week-number">{week_num}</div>' if week_num and not is_holiday else ''}
                    </td>
                    '''
            html += '</tr>'
        
        html += '</table></div>'
    
    html += '</div></body></html>'
    
    filename = f'class_calendar_{start_year}_{start_month}_{num_weeks}weeks_proper.html'
    with open(filename, 'w') as f:
        f.write(html)
    
    return html

if __name__ == "__main__":
    # year = int(input("Specify start year: "))
    # month = int(input("Specify start month: "))
    # num_weeks = int(input("Specify number of weeks: "))
    # classes_per_week = int(input("Specify number of classes per week: "))
    # print("Enter the days for classes (separated by commas, e.g., Monday,Wednesday,Friday): ")
    # class_days = input().strip().split(',')
    #generate_class_calendar(year, month, num_weeks, classes_per_week, class_days)

    generate_class_calendar(
        start_year=2025,
        start_month=9,
        num_weeks=48,
        classes_per_week=4,
        class_days=['Tuesday', 'Wednesday', 'Thursday', 'Saturday']
    )
    
