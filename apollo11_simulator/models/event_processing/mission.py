import hashlib
import uuid
from datetime import datetime

import yaml
from pydantic import BaseModel, ConfigDict, computed_field

from apollo11_simulator.models.event_processing.device import Device
from apollo11_simulator.models.event_processing.service_type import ServiceType
from apollo11_simulator.utils import Utils


class Mission(BaseModel):
    date: datetime
    budget: float | str
    device: Device

    @computed_field
    @property
    def mission(self) -> str:
        '''
                To return the name of the class

                Parameters:
                -----------

                Returns:
                --------
                    str
                '''
        return self.__class__.__name__

    @computed_field
    @property
    def hash(self) -> str:
        '''
                Overrides hash property in order to disable hash generation

                Parameters:
                -----------

                Returns:
                --------
                    str
                '''
        hash = hashlib.sha256()
        hash.update(Utils.transform_date(self.date).encode())
        hash.update(self.mission.encode())
        hash.update(self.device.device_type.encode())
        hash.update(self.device.device_status.encode())
        return hash.hexdigest()

    def __str__(self) -> str:
        return 'APL'

    def generate_event(self, name: str) -> None:
        '''
                To create a file with a name received to parameter

                Parameters:
                name

                Returns:
                --------
                    None
                '''
        with open(name, 'w+') as file:
            yaml.dump(self.model_dump(), file)


class ColonyMoon(Mission):
    size: int

    def __str__(self) -> str:
        return f'{super().__str__()}CLMN'


class GalaxyTwo(Mission):
    galaxy_name: str

    def __str__(self) -> str:
        return f'{super().__str__()}GALXONE'


class OrbitOne(Mission):
    model_config = ConfigDict(use_enum_values=True)
    satellite_name: str
    service_type: ServiceType

    def __str__(self) -> str:
        return f'{super().__str__()}ORBONE'


class Unkn(Mission):

    @property
    def mission(self) -> str:
        return super().mission.upper()

    def __str__(self) -> str:
        return f'{super().__str__()}UNKN'

    @property
    def hash(self):
        '''
        Overrides hash property in order to disable hash generation

        Parameters:
        -----------

        Returns:
        --------
            None
        '''

        return None

    @computed_field
    @property
    def process_id(self) -> str:
        return str(uuid.uuid4())


class VacMars(Mission):
    number_of_passengers: int
    ticket_price: float

    @computed_field
    @property
    def total_sales(self) -> float:
        '''
        To return the number of passenger and ticket price

        Parameters:
        -----------

        Returns:
        --------
        float
        '''
        return self.number_of_passengers * self.ticket_price

    def __str__(self) -> str:
        return f'{super().__str__()}TMRS'
