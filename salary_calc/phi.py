from datetime import datetime, timedelta


def parse_time(time_str):
    start, end = time_str.split("-")
    start_time = datetime.strptime(start, "%H%M")
    end_time = datetime.strptime(end, "%H%M")
    return start_time, end_time


def calculate_salary(start_time, end_time, base_salary, day_of_week):
    salary = 0
    current_time = start_time
    
    while current_time < end_time:
        if day_of_week in range(0, 5):  # Monday-Friday
            if current_time.time() < datetime.strptime("18:15", "%H:%M").time():
                salary += base_salary
            elif current_time.time() < datetime.strptime("20:00", "%H:%M").time():
                salary += 1.5 * base_salary
            else:
                salary += 1.7 * base_salary
        elif day_of_week == 5:  # Saturday
            if current_time.time() < datetime.strptime("12:00", "%H:%M").time():
                salary += base_salary
            else:
                salary += 2 * base_salary
        else:  # Sunday
            salary += 2 * base_salary

        current_time += timedelta(minutes=1)
    
    return salary

def save_to_file(date, daily_salary, total_salary):
    with open("salary.txt", "a") as f:
        f.write(f"{date}: {daily_salary:.2f} SEK\n")
        f.write("\n")
        f.write(f"Total Salary: {total_salary:.2f} SEK\n")


def main():
    date = datetime.now().strftime("%d%m")
    input_str = input("Enter working hours in format '1005-1900' or 'skip': ")
    
    if input_str.lower() != "skip":
        start_time, end_time = parse_time(input_str)
        day_of_week = datetime.now().weekday()
        
        base_salary = 152  # You can set your base salary here
        daily_salary = calculate_salary(start_time, end_time, base_salary, day_of_week)
        
        print(f"Total salary for {date}: {daily_salary:.2f} SEK")
        
        # Read previous total salary from the file
        try:
            with open("salary.txt", "r") as f:
                lines = f.readlines()
                previous_total = float(lines[-1].split()[-2])
        except (FileNotFoundError, IndexError, ValueError):
            previous_total = 0
        
        total_salary = previous_total + daily_salary
        save_to_file(date, daily_salary, total_salary)
    else:
        print("Skipped for today.")

if __name__ == "__main__":
    main()
