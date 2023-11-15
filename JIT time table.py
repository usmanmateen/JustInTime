import random

job_roles = {
    'Stamper': ['Shift A', 'Shift B'],
    'Floor Manager': ['Shift C', 'Shift D'],
    'Product Engineer': ['Shift E', 'Shift F'],
    'Production Operative': ['Shift A', 'Shift C', 'Shift E'],
}

def generate_shift_schedule(job_roles, num_days):
    shift_schedule = {}
    shifts = ['Shift A', 'Shift B', 'Shift C', 'Shift D', 'Shift E', 'Shift F']
    
    for day in range(1, num_days + 1):
        shift_schedule[day] = {}
        for role, patterns in job_roles.items():
            pattern = random.choice(patterns)
            shift_schedule[day][role] = random.choice(shifts)
    
    return shift_schedule


num_days = 7
schedule = generate_shift_schedule(job_roles, num_days)


for day, roles in schedule.items():
    print(f"Day {day}:")
    for role, shift in roles.items():
        print(f"{role}: {shift}")
    print()
