import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import matplotlib.cm as cm
import matplotlib.colors as mcolors
import json

# Load the data from the JSON file
with open('./boxes_with_locations.json', 'r') as file:
    data = json.load(file)


class Item:
    def __init__(self, id, width, height, depth):
        self.id = id
        self.width = width
        self.height = height
        self.depth = depth
        self.orientation = (width, height, depth)

# 가능한 모든 방향을 반환하는 메서드
    def possible_orientations(self):
        orientations = [
            (self.width, self.height, self.depth),
            (self.width, self.depth, self.height),
            (self.height, self.width, self.depth),
            (self.height, self.depth, self.width),
            (self.depth, self.width, self.height),
            (self.depth, self.height, self.width)
        ]
        return orientations

# 박스의 정보를 저장하는 리스트
items = []
for key, value in data.items():
    items.append(Item(int(key), value['width'], value['height'], value['length']))

# 서브 볼륨 적재법을 구현한 클래스 
class SubVolume:
    def __init__(self, x, y, z, width, height, depth):
        # 현재 컨테이너의 남아있는 좌표와 크기를 저장한다.
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
    # 현재 남아있는 공간이 아이템을 수용할 수 있는지 확인하는 메서드
    def can_accommodate(self, item):
        item_width, item_height, item_depth = item
        return (self.width >= item_width and
                self.height >= item_height and
                self.depth >= item_depth)

# 컨테이너를 나타내는 클래스
class Container:
    def __init__(self, width, height, depth):
        # 컨테이너의 크기와 서브 볼륨을 저장한다.( 서브 볼륨은 아이템이 적재할 때마다 업데이트 된다.)
        self.width = width
        self.height = height
        self.depth = depth
        self.sub_volumes = [SubVolume(0, 0, 0, width, height, depth)]
        self.packed_items = []
    # 서브 볼륨을 업데이트하는 매서드 
    def insert_subvolume(self, new_subvolume):
        for i, subvolume in enumerate(self.sub_volumes):
            if (new_subvolume.x < subvolume.x or # x의 크기가 줄어들었거나
                (new_subvolume.x == subvolume.x and new_subvolume.y < subvolume.y) or # y의 크기가 줄어들었거나
                (new_subvolume.x == subvolume.x and new_subvolume.z < subvolume.z)): # z의 크기가 줄어들었을 때
                self.sub_volumes.insert(i, new_subvolume) # 기존의 서브 볼륨을 새로운 서브 볼륨으로 교체한다.
                return
        self.sub_volumes.append(new_subvolume) # 새로운 서브 볼륨을 추가한다.

    def create_new_subvolumes(self, subvolume, item, item_position):
        new_subvolumes = []
        item_x, item_y, item_z = item_position
        item_width, item_height, item_depth = item

       # 아이템을 수용할 수 있는 서브 볼륨을 생성한다.
        if subvolume.height > item_height:
            new_subvolumes.append(SubVolume(item_x, item_y + item_height, item_z, item_width, subvolume.height - item_height, item_depth))
        if subvolume.width > item_width:
            new_subvolumes.append(SubVolume(item_x + item_width, item_y, item_z, subvolume.width - item_width, item_height, item_depth))
        if subvolume.depth > item_depth:
            new_subvolumes.append(SubVolume(item_x, item_y, item_z + item_depth, item_width, item_height, subvolume.depth - item_depth))

        return new_subvolumes

    def pack_items(self, items):
        for item in items:
            placed = False
            for subvolume in self.sub_volumes:
                for orientation in item.possible_orientations():
                    if subvolume.can_accommodate(orientation):
                        item_position = (subvolume.x, subvolume.y, subvolume.z)
                        self.packed_items.append((item.id, item_position, orientation))
                        
                        new_subvolumes = self.create_new_subvolumes(subvolume, orientation, item_position)
                        self.sub_volumes.remove(subvolume)
                        for new_subvolume in new_subvolumes:
                            self.insert_subvolume(new_subvolume)
                        
                        placed = True
                        break
                if placed:
                    break
            if not placed:
                print(f"Item {item.id} could not be placed.")
                break
        


# Example container dimensions (width, height, depth)
container = Container(200, 200, 200)

# Pack the items into the container
container.pack_items(items)

# Print packed items details
for item in container.packed_items:
    print(f"Item {item[0]} placed at {item[1]} with orientation {item[2]}")

# Visualize the packed container
container.visualize_packing()
p