import time
import random

# lists of connected machines 
connected_machines = {
    'Machine1': {'status': 'idle', 'instruction': None},
    'Machine2': {'status': 'idle', 'instruction': None},
    'Machine3': {'status': 'idle', 'instruction': None},
    'Machine4': {'status': 'idle', 'instruction': None},
}

# Function to send instructions to connected machines
def send_instruction(machine_id, instruction):
    if machine_id in connected_machines:
        connected_machines[machine_id]['instruction'] = instruction
        print(f"Instruction '{instruction}' sent to {machine_id}")
    else:
        print(f"Error: Machine {machine_id} not found.")

# Function to simulate machine processing
def process_machines():
    for machine_id, machine_info in connected_machines.items():
        if machine_info['status'] == 'processing':
            print(f"Machine {machine_id} is processing: {machine_info['instruction']}")
            # Simulate processing time
            time.sleep(random.uniform(1, 3))
            machine_info['status'] = 'idle'
            machine_info['instruction'] = None
            print(f"Machine {machine_id} has finished processing.")

# Example: Sending instructions to machines
send_instruction('Machine1', 'Cutting Operation')
send_instruction('Machine2', 'Assembling Operation')
send_instruction('Machine3', 'Painting Operation')
send_instruction('Machine4', 'Compiling Operation')

# Simulate machines processing
process_machines()

