import unittest
import math
from app.area_resolution import TargetCircle
from app.types import LatLon


class TestCircleRouting(unittest.TestCase):
    """Base class to test the different routing methods.

    Each class that inherits from this should test one routing method, and override `routing_method`.
    """

    routing_method = None

    def assert_latlon_lists_equal(
        self,
        left: list[LatLon],
        right: list[LatLon],
        rel_tol=0.001,
    ):
        """Assert that two lists of latitudes and longitudes are equal within a margin of error."""
        self.assertEqual(len(left), len(right))
        for l, r in zip(left, right):
            self.assertTrue(math.isclose(l[0], r[0], rel_tol=rel_tol))
            self.assertTrue(math.isclose(l[1], r[1], rel_tol=rel_tol))

    def assert_path_expected(
        self,
        circle: TargetCircle,
        vision: float,
        expected: list[LatLon],
    ):
        """Call the routing method with the given circle and vision, and assert that it returns `expected`."""
        path = self.__class__.routing_method(circle, vision)
        self.assert_latlon_lists_equal(path, expected)


class TestCircleRoutingMethod1(TestCircleRouting):
    routing_method = TargetCircle.path_method1

    def test1(self):
        centre = (10.0, 10.0)
        circle = TargetCircle(lat=centre[0], lon=centre[1], radius=20.0)
        self.assert_path_expected(
            circle=circle,
            vision=5.0,
            expected=[
                centre,
                (10.0, 30.0),
                centre,
                (18.94427190999916, 27.88854381999832),
                centre,
                (26.0, 22.0),
                centre,
                (29.677398201998148, 13.577708763999667),
                centre,
                (29.200000000000003, 4.400000000000002),
                centre,
                (24.668605932398624, -3.5952933031987158),
                centre,
                (17.040000000000006, -8.719999999999999),
                centre,
                (7.9249289168802, -9.892060727838128),
                centre,
                (-0.7519999999999971, -6.864000000000001),
                centre,
                (-7.158691232142381, -0.27517957020704387),
                centre,
                (-9.9424, 8.48319999999999),
                centre,
                (-8.515358395451063, 17.56184524358968),
                centre,
                (-3.1788800000000084, 25.043839999999992),
                centre,
                (4.940261157601107, 29.34939386251466),
                centre,
            ],
        )

    def test2(self):
        pass
