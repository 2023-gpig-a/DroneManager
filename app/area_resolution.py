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

    def displace_from_centre(self, theta: float, dist: float) -> LatLon:
        newlat: float = (math.sin(theta) * dist) + self.lat
        newlon: float = (math.cos(theta) * dist) + self.lon
        return (newlat, newlon)

    def path_method1(self, vision: float = DRONE_VISION) -> list[LatLon]:
        centre: LatLon = (self.lat, self.lon)
        coords: list[LatLon] = [centre]

        for theta in self.slices(vision):
            coords.append(self.displace_from_centre(theta, self.radius))
            coords.append(centre)

        return coords

    def path_method2(self, vision: float = DRONE_VISION) -> list[LatLon]:
        centre: LatLon = (self.lat, self.lon)
        coords: list[LatLon] = [centre]

        slices = self.slices(vision)

        for i in range(0, len(slices), 2):
            theta1 = slices[i]
            coords.append(self.displace_from_centre(theta1, self.radius))
            if i + 1 < len(slices):
                theta2 = slices[i + 1]
                coords.append(self.displace_from_centre(theta2, self.radius))
            coords.append(centre)

        return coords

    def path_method3(self, vision: float = DRONE_VISION) -> list[LatLon]:
        return []