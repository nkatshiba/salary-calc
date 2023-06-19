import datetime
import os

# Base salary
s = float(152.5)
# s = float(input("What is your base salary (s) in SEK? "))

# Overtime scheme
overtime_scheme = {
    "Monday": [
        {"start": "06:00", "end": "18:15", "multiplier": 1},
        {"start": "18:15", "end": "20:00", "multiplier": 1.5},
        {"start": "20:00", "end": "23:30", "multiplier": 1.7},
    ],
    "Tuesday": [
        {"start": "06:00", "end": "18:15", "multiplier": 1},
        {"start": "18:15", "end": "20:00", "multiplier": 1.5},
        {"start": "20:00", "end": "23:30", "multiplier": 1.7},
    ],
    "Wednesday": [
        {"start": "06:00", "end": "18:15", "multiplier": 1},
        {"start": "18:15", "end": "20:00", "multiplier": 1.5},
        {"start": "20:00", "end": "23:30", "multiplier": 1.7},
    ],
    "Thursday": [
        {"start": "06:00", "end": "18:15", "multiplier": 1},
        {"start": "18:15", "end": "20:00", "multiplier": 1.5},
        {"start": "20:00", "end": "23:30", "multiplier": 1.7},
    ],
    "Friday": [
        {"start": "06:00", "end": "18:15", "multiplier": 1},
        {"start": "18:15", "end": "20:00", "multiplier": 1.5},
        {"start": "20:00", "end": "23:30", "multiplier": 1.7},
    ],
    "Saturday": [
        {"start": "06:00", "end": "12:00", "multiplier": 1},
        {"start": "12:00", "end": "23:00", "multiplier": 2},
    ],
    "Sunday": [
        {"start": "06:00", "end": "23:00", "multiplier": 2},
    ],
}

# Prompt user for date
date_input = input("Enter the date of the hours you are about to log (format: 1906), or type 'today' if you want to log hours for today: ")
if date_input.lower() == "today":
    today = datetime.datetime.now().strftime("%d%m")
else:
    today = datetime.datetime.strptime(date_input, "%d%m").strftime("%d%m")

# Prompt user for working hours
working_hours = input("Enter your working hours for today (format: 1005-1900), or type 'skip' if you haven't worked today: ")

if working_hours.lower() == "skip":
    print("You have not worked today.")
else:
    # Calculate salary
    start_time = datetime.datetime.strptime(working_hours[:4], "%H%M").time()
    end_time = datetime.datetime.strptime(working_hours[5:], "%H%M").time()
    day_of_week = datetime.datetime.today().strftime("%A")
    salary = 0
    time_slots_salary = []
    for slot in overtime_scheme[day_of_week]:
        slot_start_time = datetime.datetime.strptime(slot["start"], "%H:%M").time()
        slot_end_time = datetime.datetime.strptime(slot["end"], "%H:%M").time()
        if start_time <= slot_start_time and end_time >= slot_end_time:
            duration = datetime.datetime.combine(datetime.date.today(), slot_end_time) - datetime.datetime.combine(datetime.date.today(), slot_start_time)
            salary += duration.seconds / 3600 * s * slot["multiplier"]
            time_slots_salary.append(f"{slot['start']}-{slot['end']}: {duration.seconds / 3600 * s * slot['multiplier']:.2f} SEK")
        elif start_time >= slot_start_time and end_time <= slot_end_time:
            duration = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), start_time)
            salary += duration.seconds / 3600 * s * slot["multiplier"]
            time_slots_salary.append(f"{working_hours}: {duration.seconds / 3600 * s * slot['multiplier']:.2f} SEK")
        elif start_time >= slot_start_time and start_time <= slot_end_time:
            duration = datetime.datetime.combine(datetime.date.today(), slot_end_time) - datetime.datetime.combine(datetime.date.today(), start_time)
            salary += duration.seconds / 3600 * s * slot["multiplier"]
            time_slots_salary.append(f"{working_hours[:4]}-{slot['end']}: {duration.seconds / 3600 * s * slot['multiplier']:.2f} SEK")
        elif end_time >= slot_start_time and end_time <= slot_end_time:
            duration = datetime.datetime.combine(datetime.date.today(), end_time) - datetime.datetime.combine(datetime.date.today(), slot_start_time)
            salary += duration.seconds / 3600 * s * slot["multiplier"]
            time_slots_salary.append(f"{slot['start']}-{working_hours[5:]}: {duration.seconds / 3600 * s * slot['multiplier']:.2f} SEK")

# ... (all the code above remains unchanged)

# Display salary and time slots salary
    print(f"Your salary for {today[:2]}/{today[2:]} is: {salary:.2f} SEK")
    print("Time slots salary:")
    for slot_salary in time_slots_salary:
        print(slot_salary)

# Calculate grand total salary
    salary_data_lines = []  # Store the salary data lines

# Create the file "salaries.txt" if it doesn't exist
    if not os.path.exists("salaries.txt"):
        with open("salaries.txt", "w") as f:
            f.write("| Date  | Working hours  | Salary      |\n")
            f.write("|-------|----------------|-------------|\n")

    grand_total_salary = 0  # Initialize grand_total_salary to 0

    with open("salaries.txt", "r") as f:
        lines = f.readlines()
        for line in lines:
            if "|" in line and "Date" not in line and "Grand total salary" not in line and "-------" not in line:
                salary_data_lines.append(line)
                try:
                    salary_value = line.split("|")[2].strip()
                    grand_total_salary += float(salary_value.split(" ")[0])
                except (ValueError, IndexError):
                    # Skip the line if it cannot be converted to a float or has an incorrect index
                    pass
            elif "Grand total salary" in line:
                grand_total_salary = float(line.split(":")[1].strip().split(" ")[0])

    grand_total_salary += salary  # Add the current day's salary to the grand total

# Save salary to file
    with open("salaries.txt", "w") as f:
        # Write the header and separators
        f.write("| Date  | Working hours  | Salary      |\n")
        f.write("|-------|----------------|-------------|\n")

        # Write the previous salary data lines (excluding the previous grand total salary line)
        for line in salary_data_lines:
            f.write(line)

        # Write the new salary entry
        f.write(f"| {today[:2]}/{today[2:]} | {working_hours} | {salary:.2f} SEK |\n")

        # Write the grand total salary
        f.write("|-------|----------------|-------------|\n")
        f.write(f"| Grand total salary: {grand_total_salary:.2f} SEK |\n")
