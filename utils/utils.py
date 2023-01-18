import os
import json
import time

def create_dataset(vehicles, cameras, max_iter=50, filename='carla/out/World_Position_Estimation/position/positions.txt'):
    if os.path.exists(filename):
        os.remove(filename)
    i = 0
    pos_list = []
    pos_dict = {}
    
    while i <= max_iter:
        pos_dict[str(i)] = {}
        for vehicle in vehicles:
            location = vehicle.vehicle.get_location()
            vehicle.move()
            pos_dict[str(i)][str(vehicle.vehicle.id)] = ([
                vehicle.vehicle.get_location().x,
                vehicle.vehicle.get_location().y,
                vehicle.vehicle.get_location().z
            ])
            
        time.sleep(1.0)
        
        for camera in cameras:
            camera.write_image(i)
            
        i+=1
        print("%.1f of %.1f" %(i, max_iter))      
        
    with open(filename, 'w') as file:
        file.write(json.dumps(pos_dict))