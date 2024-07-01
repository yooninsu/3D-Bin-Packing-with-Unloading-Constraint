import json
import numpy as np

# Load packed items from the JSON file
with open('packed_items.json', 'r') as f:
    packed_items = json.load(f)

# Sort items by load order in descending order (reverse of loading order)
packed_items.sort(key=lambda x: x['load_order'], reverse=True)

# Define the position of the container opening
container_opening_position = np.array([0, 0, 0])

# Function to calculate the Euclidean distance
def calculate_distance(position1, position2):
    return np.linalg.norm(position1 - position2)

# Calculate the unloading cost
total_unloading_cost = 0
for item in packed_items:
    # Get the position of the item
    item_position = np.array(item['position'])
    # Calculate the distance from the item's position to the container opening
    distance = calculate_distance(item_position, container_opening_position)
    # Add the distance to the total unloading cost
    total_unloading_cost += distance

print(f"Total Unloading Cost: {total_unloading_cost}")
