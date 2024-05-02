from typing import Tuple
from pydantic import BaseModel
import math

from .types import LatLon

# TODO: replace with good number
DRONE_VISION = 1.0


class TargetArea(BaseModel):
    """An area to be divided into a search sequence for a drone."""

    def search_area(self, vision: float) -> list[LatLon]:
        """Get a sequence of points to fully cover the search area."""
        return []


class TargetCircle(TargetArea):
    """Circle centred around a lat/lon with a radius.

    Has methods for routing drones to cover it, given a particular (circular) vision radius.
    """

    lat: float
    lon: float
    radius: float

    def slice_angles(self, vision: float) -> list[float]:
        """Get a sequence of radius angles that divide the circle into arcs.

        An angle will be used such that `vision` is the length of the curved side of the arc(s).
        """

        inc_angle = math.atan2(vision * 2, self.radius)
        # TODO: does this want to be floor or ceil?
        num_slices = int(math.ceil(2 * math.pi / inc_angle))
        return [inc_angle * i for i in range(num_slices)]

    def displace_from_centre(self, theta: float, dist: float) -> LatLon:
        """Get a point given a bearing and distance from the centre."""

        newlat: float = (math.sin(theta) * dist) + self.lat
        newlon: float = (math.cos(theta) * dist) + self.lon
        return (newlat, newlon)

    def centre(self) -> LatLon:
        """Convenience method to get the centre of the circle."""
        return (self.lat, self.lon)

    def path_method1(self, vision: float = DRONE_VISION) -> list[LatLon]:
        """Generate a radial point sequence."""

        coords: list[LatLon] = [self.centre()]

        for theta in self.slice_angles(vision):
            coords.append(self.displace_from_centre(theta, self.radius))
            coords.append(self.centre())

        return coords

    def path_method2(self, vision: float = DRONE_VISION) -> list[LatLon]:
        """Generate a radial point sequence, with lower overall distance."""

        coords: list[LatLon] = [self.centre()]
        slices = self.slice_angles(vision)

        for i in range(0, len(slices), 2):
            theta1 = slices[i]
            coords.append(self.displace_from_centre(theta1, self.radius))
            if i + 1 < len(slices):
                theta2 = slices[i + 1]
                coords.append(self.displace_from_centre(theta2, self.radius))
            coords.append(self.centre())

        return coords

    def path_method3(self, vision: float = DRONE_VISION) -> list[LatLon]:
        """Generate a squared zig-zag across the circle."""
        # TODO
        return []

    def search_area(self, vision: float = DRONE_VISION) -> list[LatLon]:
        # TODO: switch to method 3
        return self.path_method2(vision)
