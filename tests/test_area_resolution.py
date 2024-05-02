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
        circle = TargetCircle(lat=-10.0, lon=2.0, radius=1.0)
        self.assert_path_expected(
            circle=circle,
            vision=0.1,
            expected=[
                (-10.0, 2.0),
                (-10.0, 3.0),
                (-10.0, 2.0),
                (-9.803883864861817, 2.98058067569092),
                (-10.0, 2.0),
                (-9.615384615384615, 2.923076923076923),
                (-10.0, 2.0),
                (-9.44182330768363, 2.8297221102000094),
                (-10.0, 2.0),
                (-9.289940828402367, 2.7041420118343193),
                (-10.0, 2.0),
                (-9.165636087784886, 2.5512139892937125),
                (-10.0, 2.0),
                (-9.073736913973601, 2.376877560309513),
                (-10.0, 2.0),
                (-9.017812546688466, 2.1879037161883828),
                (-10.0, 2.0),
                (-9.000035012779664, 1.9916319456601659),
                (-10.0, 2.0),
                (-9.021094767639976, 1.795685179054071),
                (-10.0, 2.0),
                (-9.080173878850395, 1.6076737239861778),
                (-10.0, 2.0),
                (-9.17497779356995, 1.4348996912960565),
                (-10.0, 2.0),
                (-9.30182445586722, 1.284073390929701),
                (-10.0, 2.0),
                (-9.455787312796856, 1.1610527125694174),
                (-10.0, 2.0),
                (-9.630886655058317, 1.0706156131148088),
                (-10.0, 2.0),
                (-9.820321860824244, 1.0162745472936376),
                (-10.0, 2.0),
                (-10.016735522701982, 1.0001400486668688),
                (-10.0, 2.0),
                (-10.212499199494058, 1.022838759357298),
                (-10.0, 2.0),
                (-10.400009694545343, 1.0834890921163338),
                (-10.0, 2.0),
                (-10.571984353626323, 1.1797354699813738),
                (-10.0, 2.0),
                (-10.721743913381726, 1.3078398137017475),
                (-10.0, 2.0),
                (-10.843471914893001, 1.4628267236852388),
                (-10.0, 2.0),
                (-10.932440607082459, 1.6386767177945845),
                (-10.0, 2.0),
                (-10.985194566176139, 1.828560019899067),
                (-10.0, 2.0),
                (-10.999684899693584, 2.025101819149793),
                (-10.0, 2.0),
                (-10.97534882266295, 2.220668697666884),
                (-10.0, 2.0),
                (-10.913131515428772, 2.4076651021742648),
                (-10.0, 2.0),
                (-10.81544941412469, 2.5788283450244123),
                (-10.0, 2.0),
                (-10.686096359559535, 2.7275106771719257),
                (-10.0, 2.0),
                (-10.530096249567247, 2.8479374777628),
                (-10.0, 2.0),
                (-10.353507917604214, 2.9354315326046754),
                (-10.0, 2.0),
                (-10.163189815845612, 2.986594690845372),
                (-10.0, 2.0),
            ],
        )
