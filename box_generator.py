import random
import json

# Define the list of locations
locations = ['po1', 'po2', 'po3', 'po4', 'po5']

# Your data (already existing in your context)
boxes = {
    1: {"spec_id": 5, "width": 41, "length": 31, "height": 28, "volume": 35588, "weight": 8.71},
    2: {"spec_id": 2, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 6.04},
    3: {"spec_id": 3, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 2.93},
    4: {"spec_id": 5, "width": 41, "length": 31, "height": 28, "volume": 35588, "weight": 8.39},
    5: {"spec_id": 3, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 2.55},
    6: {"spec_id": 3, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 9.32},
    7: {"spec_id": 1, "width": 22, "length": 19, "height": 9, "volume": 3762, "weight": 8.69},
    8: {"spec_id": 6, "width": 48, "length": 38, "height": 34, "volume": 62016, "weight": 9.32},
    9: {"spec_id": 4, "width": 34, "length": 25, "height": 21, "volume": 17850, "weight": 2.41},
    10: {"spec_id": 2, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 4.48},
    11: {"spec_id": 6, "width": 48, "length": 38, "height": 34, "volume": 62016, "weight": 3.19},
    12: {"spec_id": 4, "width": 34, "length": 25, "height": 21, "volume": 17850, "weight": 3.26},
    13: {"spec_id": 4, "width": 34, "length": 25, "height": 21, "volume": 17850, "weight": 9.23},
    14: {"spec_id": 5, "width": 41, "length": 31, "height": 28, "volume": 35588, "weight": 4.91},
    15: {"spec_id": 2, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 3.32},
    16: {"spec_id": 7, "width": 54, "length": 39, "height": 34, "volume": 71604, "weight": 7.29},
    17: {"spec_id": 3, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 1.73},
    18: {"spec_id": 2, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 2.8},
    19: {"spec_id": 5, "width": 41, "length": 31, "height": 28, "volume": 35588, "weight": 7.38},
    20: {"spec_id": 1, "width": 22, "length": 19, "height": 9, "volume": 3762, "weight": 1.87},
    21: {"spec_id": 4, "width": 34, "length": 25, "height": 21, "volume": 17850, "weight": 6.48},
    22: {"spec_id": 6, "width": 48, "length": 38, "height": 34, "volume": 62016, "weight": 3.69},
    23: {"spec_id": 6, "width": 48, "length": 38, "height": 34, "volume": 62016, "weight": 8.19},
    24: {"spec_id": 1, "width": 22, "length": 19, "height": 9, "volume": 3762, "weight": 9.68},
    25: {"spec_id": 2, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 1.69},
    26: {"spec_id": 7, "width": 54, "length": 39, "height": 34, "volume": 71604, "weight": 1.65},
    27: {"spec_id": 6, "width": 48, "length": 38, "height": 34, "volume": 62016, "weight": 1.79},
    28: {"spec_id": 5, "width": 41, "length": 31, "height": 28, "volume": 35588, "weight": 7.04},
    29: {"spec_id": 4, "width": 34, "length": 25, "height": 21, "volume": 17850, "weight": 3.83},
    30: {"spec_id": 3, "width": 27, "length": 18, "height": 15, "volume": 7290, "weight": 5.48}
}

# Assign random locations to each box
for box_id, box_info in boxes.items():
    box_info['location'] = random.choice(locations)

# Save the updated boxes data to a JSON file
with open('boxes_with_locations.json', 'w') as json_file:
    json.dump(boxes, json_file, indent=4)

print("Data has been saved to boxes_with_locations.json")
