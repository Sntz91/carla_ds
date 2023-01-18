import json
import carla

# TODO Abstract class (Vehicle, Camera same)
class Vehicle:
    def __init__(self, direction):
        self.vehicle = False
        self.direction = direction
    
    def spawn(self, location, world, bp):
        self.vehicle = world.spawn_actor(bp, location)
    
    def move(self):
        location = self.vehicle.get_location()
        location.y += self.direction
        self.vehicle.set_location(location)

    def destroy(self):
        val = self.vehicle.destroy()
        return val

# TODO Abstract class (Vehicles, Cameras same)
class Vehicles:
    def __init__(self):
        self.vehicles = []

    @staticmethod
    def _read_vehicle_json(filename: str) -> dict:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data["vehicles"]
    
    @staticmethod
    def _read_vehicle_dict(v_dict: dict) -> tuple(str, str, carla.Location, int):
        v_name = "todo"
        v_type = v_dict["type"]
        spawn_location = v_dict["spawn_location"]
        v_spawn_location = carla.Transform(
            carla.Location(
                x=v_dict["x"],
                y=v_dict["y"],
                z=v_dict["z"]
            ),
            carla.Rotation(
                pitch=0,
                yaw=spawn_location["yaw"],
                roll=0
            )
        )
        v_direction = v_dict["direction"]

        return v_name, v_type, v_spawn_location, v_direction



    def initialize_vehicles(self, 
        bp_lib: carla.BlueprintLibrary, 
        world: carla.World, 
        filename:str='carla/data/vehicles.json'
    ) -> None:
        file = open(filename, 'r')
        data = json.load(file)
        vehicles = self._read_vehicle_json(filename)
        for vehicle in vehicles:
            #v_name = "todo" # TODO
            v_name, v_type, v_spawn_location, v_direction = \
                self._read_vehicle_dict(vehicle)

            v_bp = bp_lib.find(v_type)
            new_v = Vehicle(v_direction)
            new_v.spawn(v_spawn_location, world, v_bp)

            self.add_vehicle(new_v)

    def add_vehicle(self, vehicle: Vehicle):
        self.vehicles.append(vehicle)

    def destroy_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.destroy()
        self.vehicles = []

    def move_vehicles(self):
        for vehicle in self.vehicles:
            vehicle.move()