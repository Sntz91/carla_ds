import json
import os
import carla
import numpy as np
import cv2 
import glob

class Camera:
    def __init__(self, name: str, image_size_w: int, image_size_h: int) -> None:
        self.name = name
        self.directory = f"carla/out/World_Position_Estimation/{self.name}"
        self.data = self.get_initial_data_dict(image_size_h, image_size_w)
        self.create_dir(self.directory)

    @staticmethod 
    def create_dir(directory: str) -> None:
        if not os.path.exists(directory):
            os.mkdir(directory)
        else:
            print('Directory already exists. \
                Will be deleted ok? (y for confirmation)')
            confirmation = (input() == 'y')
            assert confirmation, "Not confirmed."
            filelist = glob.glob(os.path.join(directory, "*"))
            for f in filelist:
                os.remove(f)

    @staticmethod 
    def get_initial_data_dict(image_h: int, image_w: int) -> dict:
        data = {'image': np.zeros((image_h, image_w, 4))}
        return data
    
    def spawn(self, 
        spawn_location: carla.Location, 
        world: carla.World, 
        bp: carla.ActorBlueprint
    ) -> None:
        self.camera = world.spawn_actor(bp, spawn_location)
        self.camera.listen(lambda image: Cameras.camera_callback(image, self.data, self.name))
    
    def destroy(self) -> bool:
        val = self.camera.destroy()
        return val
        
    def open_window(self) -> None:
        cv2.namedWindow(self.name, cv2.WINDOW_AUTOSIZE)
        cv2.imshow(self.name, self.data['image'])
        cv2.waitKey(1)
        while True:
            cv2.imshow(self.name, self.data['image'])
            if cv2.waitKey(1) == ord('q'):
                break
        cv2.destroyAllWindows()
        
    def write_image(self, i: int) -> None:
        filename = f"{self.directory}/{i:03d}.jpg"
        cv2.imwrite(filename, self.data['image'])
    

class Cameras:
    def __init__(self) -> None:
        self.cameras = []

    def add_camera(self, camera: Camera) -> None:
        self.cameras.append(camera)

    @staticmethod
    def _read_camera_json(filename: str) -> dict:
        with open(filename, 'r') as file:
            data = json.load(file)
        return data["cameras"]
        
    def initialize_cameras(self, 
        bp_lib: carla.BlueprintLibrary, 
        world: carla.World, 
        filename: str='carla/data/cameras.json'
    ) -> None:
        cameras_to_initialize = self.read_camera_json(filename)
        for camera in cameras_to_initialize:
            c_name, c_type, c_spawn_location = self._read_camera_dict(camera)

            # TODO auslagern?
            c_bp = bp_lib.find(c_type)
            c_bp.set_attribute('image_size_x', '1920')
            c_bp.set_attribute('image_size_y', '1080')
            c_bp.set_attribute('fov', '87')
            c_bp.set_attribute('sensor_tick', '1.0')

            new_c = Camera(c_name, 1920, 1080)
            new_c.spawn(c_spawn_location, world, c_bp)

            self.add_camera(new_c)

    def destroy_cameras(self) -> None:
        for camera in self.cameras:
            camera.destroy()
        self.cameras = []

    def open_window(self, cam_id: int) -> None:
        self.cameras[cam_id].open_window()

    @staticmethod
    def _read_camera_dict(c_dict: dict) -> tuple(str, str, carla.Location):
        c_name = c_dict["name"]
        c_type = c_dict["type"]
        spawn_location = c_dict["spawn_location"]
        c_spawn_location = \
            Cameras._transform_dict_to_carla_location(spawn_location)
        return c_name, c_type, c_spawn_location

    @staticmethod 
    def _transform_dict_to_carla_location(l_dict: dict) -> carla.Location:
        location = carla.Transform(
            carla.Location(
                x=l_dict["x"],
                y=l_dict["y"],
                z=l_dict["z"]
            ),
            carla.Rotation(
                pitch=l_dict["pitch"],
                yaw=l_dict["yaw"],
                roll=l_dict["roll"]
            )
        )
        return location

    @staticmethod
    def camera_callback(image, data_dict, camera_name) -> None:
        data_dict["Camera_Name"] = camera_name
        data_dict['image'] = np.reshape(
            np.copy(image.raw_data), 
            (image.height, image.width, 4)
        )