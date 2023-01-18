import carla
from utils.vehicle import Vehicles
from utils.camera import Cameras
from utils.utils import create_dataset

def main():
    client = carla.Client('localhost', 2000) 
    world = client.get_world()
    bp_lib = world.get_blueprint_library() 

    try:
        vehicles = Vehicles()
        vehicles.initialize_vehicles(bp_lib, world)

        cameras = Cameras()
        cameras.initialize_cameras(bp_lib, world)

        create_dataset(vehicles.vehicles, cameras.cameras, max_iter=10)

    except Exception as e:
        print("sheesh.", e)

    finally:
        vehicles.destroy_vehicles()
        cameras.destroy_cameras()


if __name__=='__main__':
    main()