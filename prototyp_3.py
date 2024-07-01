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

    def pack_items(self, items, method='DBL'):
        if method == 'DBL':
            self.pack_items_dbl(items)
        elif method == 'BR':
            self.pack_items_br(items)
        else:
            raise ValueError(f"Unknown packing method: {method}")

    def pack_items_dbl(self, items):
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

    def pack_items_br(self, items):
        def eval_ems(ems):
            score = 0
            valid = []
            for bs in items:
                for orientation in bs.possible_orientations():
                    bx, by, bz = orientation
                    if ems[3] - ems[0] >= bx and ems[4] - ems[1] >= by and ems[5] - ems[2] >= bz:
                        valid.append(1)
            score += (ems[3] - ems[0]) * (ems[4] - ems[1]) * (ems[5] - ems[2])
            score += len(valid)
            if len(valid) == len(items):
                score += 10
            return score

        for item in items:
            placed = False
            best_score = -1e10
            best_action = None

            for subvolume in self.sub_volumes:
                for orientation in item.possible_orientations():
                    if subvolume.can_accommodate(orientation):
                        item_position = (subvolume.x, subvolume.y, subvolume.z)
                        updated_containers = self.copy()
                        self.packed_items.append((item.id, item_position, orientation))
                        new_subvolumes = self.create_new_subvolumes(subvolume, orientation, item_position)
                        updated_containers.sub_volumes.remove(subvolume)
                        for new_subvolume in new_subvolumes:
                            updated_containers.insert_subvolume(new_subvolume)
                        score = eval_ems([subvolume.x, subvolume.y, subvolume.z, subvolume.x + orientation[0], subvolume.y + orientation[1], subvolume.z + orientation[2]])
                        if score > best_score:
                            best_score = score
                            best_action = (item.id, item_position, orientation)
                        self.packed_items.pop()

            if best_action is not None:
                item_id, item_position, orientation = best_action
                self.packed_items.append((item_id, item_position, orientation))
                self.sub_volumes = updated_containers.sub_volumes
                placed = True
                subvolume = [s for s in self.sub_volumes if s.x == item_position[0] and s.y == item_position[1] and s.z == item_position[2]][0]
                new_subvolumes = self.create_new_subvolumes(subvolume, orientation, item_position)
                self.sub_volumes.remove(subvolume)
                for new_subvolume in new_subvolumes:
                    self.insert_subvolume(new_subvolume)
            else:
                print(f"Item {item.id} could not be placed.")
                break

    def visualize_packing(self):
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')

        # Create a colormap
        colormap = cm.get_cmap('tab20', len(self.packed_items))
        norm = mcolors.Normalize(vmin=0, vmax=len(self.packed_items) - 1)

        for index, (item_id, position, orientation) in enumerate(self.packed_items):
            x, y, z = position
            dx, dy, dz = orientation

            # Draw the cuboid
            vertices = [
                [x, y, z],
                [x + dx, y, z],
                [x + dx, y + dy, z],
                [x, y + dy, z],
                [x, y, z + dz],
                [x + dx, y, z + dz],
                [x + dx, y + dy, z + dz],
                [x, y + dy, z + dz]
            ]
            faces = [
                [vertices[j] for j in [0, 1, 2, 3]],
                [vertices[j] for j in [4, 5, 6, 7]], 
                [vertices[j] for j in [0, 1, 5, 4]], 
                [vertices[j] for j in [2, 3, 7, 6]], 
                [vertices[j] for j in [1, 2, 6, 5]], 
                [vertices[j] for j in [4, 7, 3, 0]]
            ]
            
            color = colormap(norm(index))
            poly3d = Poly3DCollection(faces, facecolors=color, linewidths=1, edgecolors='r')
            poly3d.set_alpha(0.7)
            ax.add_collection3d(poly3d)

            # Label the item with its ID and location
            item_location = next((item['location'] for key, item in data.items() if int(key) == item_id), "unknown")
            ax.text(x + dx / 2, y + dy / 2, z + dz / 2, f'{item_id} ({item_location})', color='black', fontsize=8, ha='center', va='center')

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.set_xlim([0, self.width])
        ax.set_ylim([0, self.height])
        ax.set_zlim([0, self.depth])

        plt.show()

# Example container dimensions (width, height, depth)
container = Container(200, 200, 200)

# Pack the items into the container using DBL method
container.pack_items(items, method='DBL')

# Print packed items details
for item in container.packed_items:
    print(f"Item {item[0]} placed at {item[1]} with orientation {item[2]}")

# Visualize the packed container
container.visualize_packing()

# Pack the items into the container using BR method
container.pack_items(items, method='BR')

# Print packed items details
for item in container.packed_items:
    print(f"Item {item[0]} placed at {item[1]} with orientation {item[2]}")

# Visualize the packed container
container.visualize_packing()
