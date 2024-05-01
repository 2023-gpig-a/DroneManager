from typing import Tuple
from pydantic import BaseModel
import math

from .types import LatLon

# TODO: replace with good number
DRONE_VISION = 1.0


class TargetCircle(BaseModel):
    lat: float
    lon: float
    radius: float

    def slices(self, vision: float) -> list[float]:
        slice_angle = math.atan2(vision * 2, self.radius)
        # TODO: does this want to be floor or ceil?
        num_slices = int(math.ceil(2 * math.pi / slice_angle))
        return [slice_angle * i for i in range(num_slices)]

    def path_method1(self, vision: float = DRONE_VISION) -> list[LatLon]:
        centre: LatLon = (self.lat, self.lon)
        coords: list[LatLon] = []
        for theta in self.slices(vision):
            newlat: float = (math.sin(theta) * self.radius) + self.lat
            newlon: float = (math.cos(theta) * self.radius) + self.lon
            coords.push((newlat, newlon))
            coords.push(centre)
        return coords

    def path_method2(self, vision: float = DRONE_VISION) -> list[LatLon]:
        pass

    def path_method3(self, vision: float = DRONE_VISION) -> list[LatLon]:
        pass
