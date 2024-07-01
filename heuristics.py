from given_data import container_size, data
import random
import json

# Item class to represent each box
class Item:
    def __init__(self, id, width, length, height, weight, location):
        self.id = id
        self.width = width
        self.length = length
        self.height = height
        self.weight = weight
        self.orientation = (width, length, height)
        self.location = location

    def possible_orientations(self):
        orientations = [
            (self.width, self.length, self.height),
            (self.width, self.height, self.length),
            (self.length, self.width, self.height),
            (self.length, self.height, self.width),
            (self.height, self.width, self.length),
            (self.height, self.length, self.width)
        ]
        return orientations

# Convert data to a list of Item objects
items = []
for key, value in data.items():
    items.append(Item(int(key), value['width'], value['length'], value['height'], value['weight'], value['location']))

# SubVolume class to represent available spaces in the container
class SubVolume:
    def __init__(self, x, y, z, width, length, height):
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.length = length
        self.height = height

    def can_accommodate(self, item):
        item_width, item_length, item_height = item
        return (self.width >= item_width and
                self.length >= item_length and
                self.height >= item_height)

# Container class to represent the container and manage packing
class Container:
    def __init__(self, width, length, height):
        self.width = width
        self.length = length
        self.height = height
        self.sub_volumes = [SubVolume(0, 0, 0, width, length, height)]
        self.packed_items = []

    def insert_subvolume(self, new_subvolume):
        self.sub_volumes.append(new_subvolume)

    def create_new_subvolumes(self, subvolume, item, item_position):
        new_subvolumes = []
        item_x, item_y, item_z = item_position
        item_width, item_length, item_height = item

        if subvolume.width > item_width:
            new_subvolumes.append(SubVolume(item_x + item_width, item_y, item_z,
                                            subvolume.width - item_width, item_length, item_height))
        if subvolume.length > item_length:
            new_subvolumes.append(SubVolume(item_x, item_y + item_length, item_z,
                                            item_width, subvolume.length - item_length, item_height))
        if subvolume.height > item_height:
            new_subvolumes.append(SubVolume(item_x, item_y, item_z + item_height,
                                            item_width, item_length, subvolume.height - item_height))

        if subvolume.width > item_width and subvolume.length > item_length:
            new_subvolumes.append(SubVolume(item_x + item_width, item_y + item_length, item_z,
                                            subvolume.width - item_width, subvolume.length - item_length, item_height))

        if subvolume.width > item_width and subvolume.height > item_height:
            new_subvolumes.append(SubVolume(item_x + item_width, item_y, item_z + item_height,
                                            subvolume.width - item_width, item_length, subvolume.height - item_height))

        if subvolume.length > item_length and subvolume.height > item_height:
            new_subvolumes.append(SubVolume(item_x, item_y + item_length, item_z + item_height,
                                            item_width, subvolume.length - item_length, subvolume.height - item_height))

        if subvolume.width > item_width and subvolume.length > item_length and subvolume.height > item_height:
            new_subvolumes.append(SubVolume(item_x + item_width, item_y + item_length, item_z + item_height,
                                            subvolume.width - item_width, subvolume.length - item_length, subvolume.height - item_height))

        return new_subvolumes

    def is_supported(self, item_position, item_orientation):
        item_x, item_y, item_z = item_position
        item_width, item_length, item_height = item_orientation

        if item_z == 0:
            return True  # Item is on the floor

        # Check if there is a supporting box below
        for packed_item in self.packed_items:
            _, packed_position, packed_orientation, _, _, _ = packed_item
            packed_x, packed_y, packed_z = packed_position
            packed_width, packed_length, packed_height = packed_orientation

            if (packed_x <= item_x < packed_x + packed_width or packed_x < item_x + item_width <= packed_x + packed_width) and \
               (packed_y <= item_y < packed_y + packed_length or packed_y < item_y + item_length <= packed_y + packed_length) and \
               (packed_z + packed_height == item_z):
                return True

        return False

    def pack_items(self, items, method='DBL'):
        if method == 'DBL':
            self.pack_items_dbl(items)
        else:
            raise ValueError(f"Unknown packing method: {method}")

    def pack_items_dbl(self, items):
        best_packing = []
        best_packing_count = 0
        iterations = 1000  # Number of iterations to attempt

        for _ in range(iterations):
            self.reset()
            random_items = random.sample(items, len(items))  # Randomly shuffle items
            load_order = 0  # Initialize load order counter
            for item in random_items:
                placed = False
                random_orientations = random.sample(item.possible_orientations(), len(item.possible_orientations()))  # Randomly shuffle orientations
                for subvolume in self.sub_volumes:
                    for orientation in random_orientations:
                        if subvolume.can_accommodate(orientation):
                            item_position = (subvolume.x, subvolume.y, subvolume.z)
                            if self.is_supported(item_position, orientation):
                                load_order += 1  # Increment load order
                                self.packed_items.append((item.id, item_position, orientation, item.location, load_order, item.weight))
                                new_subvolumes = self.create_new_subvolumes(subvolume, orientation, item_position)
                                self.sub_volumes.remove(subvolume)
                                for new_subvolume in new_subvolumes:
                                    self.insert_subvolume(new_subvolume)
                                placed = True
                                break
                    if placed:
                        break
                if not placed:
                    print(f"Item {item.id} could not be placed in this iteration.")
                    break
            if len(self.packed_items) > best_packing_count:
                best_packing = list(self.packed_items)
                best_packing_count = len(self.packed_items)

        self.packed_items = best_packing

    def reset(self):
        self.sub_volumes = [SubVolume(0, 0, 0, self.width, self.length, self.height)]
        self.packed_items = []  
        return 

def main():
    container = Container(container_size[0], container_size[1], container_size[2])
    container.pack_items(items, method='DBL')

    print("Packed Items:")
    for packed_item in container.packed_items:
        print(f"Item ID: {packed_item[0]}, Position: {packed_item[1]}, Orientation: {packed_item[2]}, Location: {packed_item[3]}, Load Order: {packed_item[4]}, Weight: {packed_item[5]}")

    # Save packed items to a JSON file
    packed_items_data = [
        {"id": packed_item[0], "position": packed_item[1], "orientation": packed_item[2], "location": packed_item[3], "load_order": packed_item[4], "weight": packed_item[5], "dimensions": (packed_item[2][0], packed_item[2][1], packed_item[2][2])}
        for packed_item in container.packed_items
    ]
    with open('packed_items.json', 'w') as f:
        json.dump(packed_items_data, f, indent=4)

if __name__ == "__main__":
    main()
