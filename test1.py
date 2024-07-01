from ortools.linear_solver import pywraplp
import pybullet as p
import pybullet_data
import time

def create_data_model():
    data = {}
    weights = [48, 30, 19, 36, 36, 27, 42, 42, 36, 24, 30]
    widths = [10, 20, 30, 20, 20, 15, 25, 25, 20, 10, 20]
    lengths = [5, 10, 15, 10, 10, 8, 12, 12, 10, 5, 10]
    heights = [3, 6, 9, 6, 6, 4, 7, 7, 6, 3, 6]
    
    # Define the container dimensions
    data['container'] = {'width': 100, 'length': 100, 'height': 100}
    
    # Define the items as a list of dictionaries
    data['items'] = [
        {'id': i, 'weight': weights[i], 'width': widths[i], 'length': lengths[i], 'height': heights[i]}
        for i in range(len(weights))
    ]
    
    return data

def pack_items(data):
    solver = pywraplp.Solver.CreateSolver("SCIP")
    if not solver:
        return None

    # Variables
    x = {}
    y = solver.IntVar(0, 1, 'y')
    
    for item in data['items']:
        x[item['id']] = solver.IntVar(0, 1, 'x[%i]' % item['id'])

    # Constraints
    solver.Add(sum(x[item['id']] * item['weight'] for item in data['items']) <= y * data['container']['width'])

    for item in data['items']:
        solver.Add(x[item['id']] <= y)
    
    # Objective
    solver.Minimize(y)

    status = solver.Solve()

    if status == pywraplp.Solver.OPTIMAL:
        packed_items = [item for item in data['items'] if x[item['id']].solution_value() > 0]
        return packed_items
    else:
        return None

def setup_pybullet():
    physicsClient = p.connect(p.GUI)  # Use GUI instead of DIRECT for visualization
    p.setAdditionalSearchPath(pybullet_data.getDataPath())
    p.setGravity(0, 0, -9.81)
    p.loadURDF("plane.urdf")
    return physicsClient

def create_pybullet_box(item, base_position):
    half_extents = [item['width'] / 2, item['length'] / 2, item['height'] / 2]
    collision_shape_id = p.createCollisionShape(p.GEOM_BOX, halfExtents=half_extents)
    body_id = p.createMultiBody(baseMass=0, baseCollisionShapeIndex=collision_shape_id, basePosition=base_position)
    return body_id

def visualize_packing(packed_items):
    setup_pybullet()
    x_offset = 0
    y_offset = 0
    z_offset = 0
    for i, item in enumerate(packed_items):
        pos = [x_offset + item['width'] / 2, y_offset + item['length'] / 2, z_offset + item['height'] / 2]
        create_pybullet_box(item, pos)
        x_offset += item['width']  # Stack items horizontally
        if x_offset >= 100:  # Move to the next row if the current row is full
            x_offset = 0
            y_offset += item['length']
        if y_offset >= 100:  # Move to the next layer if the current layer is full
            y_offset = 0
            z_offset += item['height']
        p.setRealTimeSimulation(1)
        for _ in range(240):  # Add a delay to visualize the sequence
            p.stepSimulation()
            time.sleep(1./240.)
    while True:
        p.stepSimulation()
        time.sleep(1./240.)

def main():
    data = create_data_model()
    packed_items = pack_items(data)
    if packed_items is None:
        print("No feasible packing solution found.")
        return

    print("Packing solution is collision-free.")
    for item in packed_items:
        print(f"Packed item {item['id']} at initial position.")
    
    visualize_packing(packed_items)

if __name__ == "__main__":
    main()
