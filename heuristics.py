from given_data import container_size, data
import random
import json

class Item:
    def __init__(self, id, width, length, height, weight, location):
        self.id = id
        self.width = width
        self.length = length
        self.height = height
        self.weight = weight
        self.location = location

    def possible_orientations(self):
        return [
            (self.width, self.length, self.height),
            (self.width, self.height, self.length),
            (self.length, self.width, self.height),
            (self.length, self.height, self.width),
            (self.height, self.width, self.length),
            (self.height, self.length, self.width)
        ]

# Convert data to a list of Item objects
items = [Item(int(key), value['width'], value['length'], value['height'], value['weight'], value['location'])
         for key, value in data.items()]

class PackingAlgorithm:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.best_packed_items = []
        self.best_utilization = 0

    def pack_items_with_permutations(self, items, num_iterations=1000):
        for _ in range(num_iterations):
            random.shuffle(items)
            packed_items = self.pack_items(items)
            utilization = self.calculate_capacity_utilization(packed_items)
            
            if utilization > self.best_utilization:
                self.best_packed_items = packed_items
                self.best_utilization = utilization

    def pack_items(self, items):
        packed_items = []
        current_x, current_y, current_z = 0, self.length, 0
        load_order = 0
        
        for item in items:
            placed = False
            for orientation in item.possible_orientations():
                if self.can_place_item(current_x, current_y, current_z, orientation):
                    load_order += 1
                    packed_items.append({
                        "id": item.id,
                        "position": (current_x, current_y - orientation[1], current_z),
                        "orientation": orientation,
                        "location": item.location,
                        "load_order": load_order,
                        "weight": item.weight
                    })
                    placed = True
                    
                    # Update current_x for the next item
                    current_x += orientation[0]
                    
                    # If we've reached the end of the row
                    if current_x + orientation[0] > self.width:
                        current_x = 0
                        current_z += orientation[2]
                        
                        # If we've reached the top of the container
                        if current_z + orientation[2] > self.height:
                            current_z = 0
                            current_y -= orientation[1]
                    
                    break
            
            if not placed:
                print(f"Unable to place item {item.id}")
        
        return packed_items

    def can_place_item(self, x, y, z, orientation):
        return (x + orientation[0] <= self.width and
                y - orientation[1] >= 0 and
                z + orientation[2] <= self.height)

    def calculate_capacity_utilization(self, packed_items):
        total_container_volume = self.width * self.length * self.height
        packed_volume = sum(item["orientation"][0] * item["orientation"][1] * item["orientation"][2] 
                            for item in packed_items)
        return packed_volume / total_container_volume

def main():
    container = PackingAlgorithm(container_size[0], container_size[1], container_size[2])
    container.pack_items_with_permutations(items)

    print("Best Packed Items:")
    for packed_item in container.best_packed_items:
        print(f"Item ID: {packed_item['id']}, Position: {packed_item['position']}, "
              f"Orientation: {packed_item['orientation']}, Location: {packed_item['location']}, "
              f"Load Order: {packed_item['load_order']}, Weight: {packed_item['weight']}")
 
    # Save packed items to a JSON file
    with open('packed_items.json', 'w') as f:
        json.dump(container.best_packed_items, f, indent=4)

    # Print the best capacity utilization
    print(f"Best Capacity Utilization: {container.best_utilization:.2%}")

if __name__ == "__main__":
    main()