from pydantic import BaseModel
import math

from .types import LatLon


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

        # calculate arc angle
        inc_angle = math.atan2(vision * 2, self.radius)
        # minimum number of arcs with this angle to cover the whole circle
        num_slices = int(math.ceil(2 * math.pi / inc_angle))
        return [inc_angle * i for i in range(num_slices)]

    def displace_from_centre(self, theta: float, dist: float) -> LatLon:
        """Get a point given a bearing and distance from the centre."""

        newlat: float = (math.sin(theta) * dist) + self.lat
        newlon: float = (math.cos(theta) * dist) + self.lon
        return newlat, newlon

    def centre(self) -> LatLon:
        """Convenience method to get the centre of the circle."""
        return self.lat, self.lon

    def path_method1(self, vision: float) -> list[LatLon]:
        """Generate a radial point sequence."""

        coords: list[LatLon] = [self.centre()]

        for theta in self.slice_angles(vision):
            # go to the outside of the next arc, then back in again
            coords.append(self.displace_from_centre(theta, self.radius))
            coords.append(self.centre())

        return coords

    def path_method2(self, vision: float) -> list[LatLon]:
        """Generate a radial point sequence, with lower overall distance."""

        coords: list[LatLon] = [self.centre()]
        slices = self.slice_angles(vision)

        for i in range(0, len(slices), 2):
            # go to the outside of the next arc
            theta1 = slices[i]
            coords.append(self.displace_from_centre(theta1, self.radius))
            # if we're not about to cross our first arc again (ie. this is not the last arc),
            # move *along* the circumference one arc
            if i + 1 < len(slices):
                theta2 = slices[i + 1]
                coords.append(self.displace_from_centre(theta2, self.radius))
            # then back to the centre :)
            coords.append(self.centre())

        return coords

    def path_method3(self, vision: float) -> list[LatLon]:
        """Generate a zig-zag across the circle."""

        # start at the very "bottom" of the circle
        start_lat = self.lat - self.radius
        coords = [(start_lat, self.lon)]

        # generate a sequence of latitudes that we're gonna cross the circle at
        num_lines = int(math.ceil((self.radius * 2) / vision))
        print(self.radius, vision, num_lines)
        latitude_lines: list[float] = [
            start_lat + (vision * i)
            # skip the first one since it's our start point
            for i in range(1, num_lines)
        ]

        # use pythagoras to calculate the longitude difference between
        # the centre of the circle and the point(s) at the intersection of
        # the circle and a given latitude line
        def get_abs_hor_displacement(latitude: float) -> float:
            vert_from_centre = math.fabs(self.lat - latitude)

            # pythagoras
            diff_squares = math.fabs((self.radius**2) - (vert_from_centre**2))
            return math.sqrt(diff_squares)

        for line in latitude_lines:
            hor_from_centre1 = get_abs_hor_displacement(line)
            coords.append((line, self.lon + hor_from_centre1))
            coords.append((line, self.lon - hor_from_centre1))

        return coords

    def search_area(self, vision: float) -> list[LatLon]:
        return self.path_method3(vision)
