import os
import random

def generate_role_schedule(role_name, role_tasks):

    days_of_week = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

   
    weekly_schedule = {}
    for day in days_of_week:
        # random task to each day
        weekly_schedule[day] = random.choice(role_tasks[role_name])

    # create a style 
    schedule_table = f"+------------+{'-' * 54}+\n"
    schedule_table += f"| {role_name.upper():^13} | {'Task':^54} |\n"
    schedule_table += f"+------------+{'-' * 54}+\n"

    #table with tasks for each day
    for day, task in weekly_schedule.items():
        schedule_table += f"| {day:<10} | {task:<54} |\n"

    schedule_table += f"+------------+{'-' * 54}+"


    folder_name = 'uploads'
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    file_path = os.path.join(folder_name, f"{role_name.replace(' ', '_').lower()}_weekly_schedule.txt")
    with open(file_path, 'w') as file:
        file.write(schedule_table)

    print(f"{role_name} weekly schedule saved to '{file_path}'")

def job_allocation():

    tasks = {
        "Stamper": [
            "8 am - 4 pm (Stamping duties)",
            "7 am - 5 pm (Stamping oversight)",
            "9 am - 3 pm (Stamping quality checks)"
        ],
        "Floor Manager": [
            "7 am - 5 pm (Floor oversight)",
            "7 am - 4 pm (Floor oversight, meetings)",
            "8 am - 6 pm (Floor planning)"
        ],
        "Product Operative": [
            "8 am - 4 pm (Production tasks)",
            "8 am - 5 pm (Inventory management)",
            "9 am - 4 pm (Product testing)"
        ],
        "Product Engineer": [
            "9 am - 5 pm (Design tasks)",
            "9 am - 6 pm (Research and development)",
            "10 am - 4 pm (Prototyping)"
        ],
        "Marketing Director": [
            "9 am - 5 pm (Campaign planning)",
            "10 am - 4 pm (Market research)",
            "11 am - 6 pm (Ad strategy development)"
        ]
    }

    for role, task_list in tasks.items():
        generate_role_schedule(role, tasks)


job_allocation()
