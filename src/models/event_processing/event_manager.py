from typing import Any, List, Tuple
from pydantic import BaseModel
from src.models.event_processing.colony_moon import ColonyMoon
from src.models.event_processing.device import Device
from src.models.event_processing.device_status import DeviceStatus
from src.models.event_processing.galaxy_two import GalaxyTwo
from src.models.event_processing.orbit_one import OrbitOne
from src.models.event_processing.service_type import ServiceType
from src.models.event_processing.vac_mars import VacMars
from src.models.event_processing.unkn import Unkn
from datetime import datetime
import random
from pathlib import Path
import sched
import time

class EventManager(BaseModel):
    target_path: str
    frequency_seconds: int
    range_of_files: Tuple[int, int]

    def __random_device(self, mission_class) -> Device:
        '''
        Description here
        
        Parameters:
        -----------
        
        Returns:
        --------
        
        '''
        
        if mission_class is Unkn:
            return Device(
                device_type = 'unknown', 
                device_status = DeviceStatus.UNKNOWN, 
                device_age = 'unknown',
                device_description = 'unknown'
            )
        else:
            return Device(
                device_status = random.choice([
                    DeviceStatus.EXCELLENT, 
                    DeviceStatus.FAULTY, 
                    DeviceStatus.GOOD, 
                    DeviceStatus.KILLED, 
                    DeviceStatus.WARNING, 
                    DeviceStatus.UNKNOWN
                ]),
                device_type = 'd',
                device_description = 'any description',
                device_age = random.randint(2, 20)
            )
        
    def __generate_files(self) -> None:
        '''
        description here
        
        Parameters:
        -----------

        Returns:
        --------
            None
        '''

        min_files, max_files = self.range_of_files
        
        number_of_files: int = random.randint(min_files, max_files)
        
        mission_classes: List = random.choices([ColonyMoon, OrbitOne, GalaxyTwo, VacMars, Unkn], k = number_of_files)
        
        # Create "devices" directory if it does not exist
        device_path = Path(self.target_path)
        device_path.mkdir(exist_ok = True) 
             
        for i, mission_class in enumerate(mission_classes, 1):

            # Params for each mission class whose keys correspond to the class
            mission_params = {
                ColonyMoon: {
                    'date': datetime.now(), 
                    'budget': 2,
                    'size': 5
                },
                OrbitOne: {
                    'date' : datetime.now(), 
                    'budget' : 2,
                    'satellite_name' : 'OpenAI',
                    'service_type' : ServiceType.UPDATE
                },
                GalaxyTwo: {
                    'date': datetime.now(), 
                    'budget': 2,
                    'distance_ly': 15,
                    'galaxy_name': 'Orion'
                },
                VacMars: {
                    'date': datetime.now(), 
                    'budget': 2,
                    'number_of_passengers': 3,
                    'ticket_price': 15
                },
                Unkn: {
                    'date': datetime.now(),
                    'budget': 'unknown'
                }
            }

            # Create an instance based on one of the dictionary keys.
            mission_instance = mission_class(**mission_params[mission_class], device = self.__random_device(mission_class))
                
            name: Path = device_path.joinpath(f'{str(mission_instance)}-{i}.log')

            mission_instance.generate_event(name)

    def __call__(self) -> Any:
        self.__generate_files()