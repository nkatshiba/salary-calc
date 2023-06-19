# from datetime import datetime, time, date
import datetime
import os

def parse_work_date(input_str: str) -> datetime.date:
    return datetime.datetime.strptime(input_str, "%d%m").date()

def parse_work_hours(input_str: str) -> tuple[datetime.time, datetime.time]:
    start_str, end_str = input_str.split('-')
    start = datetime.datetime.strptime(start_str, "%H%M").time()
    end = datetime.datetime.strptime(end_str, "%H%M").time()
    return start, end

def main():
    input_date_str = input("Enter the date you worked (DDMM) or 'today': ")
    work_date = parse_work_date(input_date_str) if input_date_str.lower() != 'today' else datetime.date.today()

    input_str = input("Enter work hours (HHMM-HHMM) or 'skip' if you didn't work: ")
    if input_str.lower() != 'skip':
        start, end = parse_work_hours(input_str)
        start = datetime.datetime.combine(work_date, start)
        end = datetime.datetime.combine(work_date, end)

        # ... (rest of your code for calculating salary and writing to the file)

    with open("salary.txt", "r") as f:
        lines = f.readlines()

    total_salary = sum(float(line.split(' - ')[1].strip().rstrip(" SEK")) for line in lines if ' - ' in line and not line.startswith("Total"))

    for line in lines:
        print(line.strip())

    print(f"\nTotal accumulated salary: {total_salary:.2f} SEK")

if __name__ == "__main__":
    main()
