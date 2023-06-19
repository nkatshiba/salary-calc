import datetime

# Base salary
s = float(152.5)

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

# Get today's date
today = datetime.datetime.now().strftime("%d%m")

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

    # Display salary and time slots salary
    print(f"Your salary for today is: {salary:.2f} SEK")
    print("Time slots salary:")
    for slot_salary in time_slots_salary:
        print(slot_salary)

    # Save salary to file
    with open(f"{today}_salary.txt", "a") as f:
        f.write(f"{today}: {salary:.2f} SEK\n")

    # Calculate and display grand total salary
    grand_total_salary = 0
    with open(f"{today}_salary.txt", "r") as f:
        for line in f:
            grand_total_salary += float(line.split(": ")[1].split(" ")[0])
    print(f"\nGrand total salary: {grand_total_salary:.2f} SEK")
