from datetime import datetime, time, date
import os


def parse_work_hours(input_str):
    start_str, end_str = input_str.split('-')

    if ':' not in start_str:
        start_str += ':00'
    if ':' not in end_str:
        end_str += ':00'

    start = datetime.strptime(start_str, "%H:%M")
    end = datetime.strptime(end_str, "%H:%M")

    return start, end

def calculate_salary(start, end, base_salary, weekdays_rules, weekend_rules):
    day_of_week = start.weekday()
    rules = weekdays_rules if day_of_week < 5 else weekend_rules
    salary = 0

    for rule in rules:
        rule_start, rule_end, multiplier = rule
        overlap_start = max(start.time(), rule_start)
        overlap_end = min(end.time(), rule_end)

        if overlap_start < overlap_end:
            duration = (datetime.combine(datetime.min, overlap_end) - datetime.combine(datetime.min, overlap_start)).seconds
            salary += duration * base_salary * multiplier / 3600

    return salary


def main():
    while True:
        date_input = input("Enter the date you worked (DD/MM) or 'today': ")
        if date_input.lower() == 'today':
            work_date = datetime.now()
            break
        else:
            try:
                work_date = datetime.strptime(date_input, "%d/%m")
                break
            except ValueError:
                print("Invalid date format. Please enter the date in the format 'DD/MM' or 'today'.")

    input_str = input("Enter work hours (HH:MM-HH:MM) or 'skip' if you didn't work: ")

    if input_str.lower() != 'skip':
        start, end = parse_work_hours(input_str)
        start = work_date.replace(hour=start.hour, minute=start.minute)
        end = work_date.replace(hour=end.hour, minute=end.minute)
        # start, end = parse_work_hours(input_str)
        # start = work_date.replace(hour=start.hour, minute=start.minute)
        # end = work_date.replace(hour=end.hour, minute=end.minute)
        # start, end = parse_work_hours(input_str)

        weekdays_rules = [
            (time(6, 0), time(18, 15), 1),
            (time(18, 15), time(20, 0), 1.5),
            (time(20, 0), time(23, 30), 1.7),
        ]

        weekend_rules = [
            (time(6, 0), time(12, 0), 1),
            (time(12, 0), time(23, 0), 2),
        ]

        base_salary = 100  # Replace with your base salary in SEK
        salary = calculate_salary(start, end, base_salary, weekdays_rules, weekend_rules)

        date_str = start.strftime("%d/%m")
        result_line = f"{date_str} - {salary:.2f} SEK\n"

        with open("salary.txt", "a+") as f:
            f.write(result_line)
            f.seek(0)
            lines = f.readlines()
            # total_salary = sum(float(line.split(' - ')[1].strip().rstrip(" SEK")) for line in lines)
            total_salary = sum(float(line.split(' - ')[1].strip().rstrip(" SEK")) for line in lines if ' - ' in line and not line.startswith("Total"))
            f.write(f"Total: {total_salary:.2f} SEK\n")

        print(result_line.strip())


if __name__ == "__main__":
    main()
