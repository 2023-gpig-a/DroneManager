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


class TestCircleRoutingMethod2(TestCircleRouting):
    routing_method = TargetCircle.path_method2

    def test1(self):
        circle = TargetCircle(lat=0.01, lon=100.0, radius=2000.0)
        self.assert_path_expected(
            circle=circle,
            vision=100.0,
            expected=[
                (0.01, 100.0),
                (0.01, 2100.0),
                (199.01743804199782, 2090.0743804199783),
                (0.01, 100.0),
                (396.049603960396, 2060.39603960396),
                (589.1508314312608, 2011.2595534726524),
                (0.01, 100.0),
                (776.4044711302813, 1943.1526320948929),
                (955.9519146648305, 1856.7512788630434),
                (0.01, 100.0),
                (1126.0110424138188, 1752.9130807404827),
                (1284.8939121690996, 1632.6686961796504),
                (0.01, 100.0),
                (1431.0235130077, 1497.211625198331),
                (1562.9494181023158, 1347.8863631525085),
                (0.01, 100.0),
                (1679.3621811062271, 1186.1750557869382),
                (1779.1063332195981, 1013.6827880203174),
                (0.01, 100.0),
                (1861.19185193322, 832.1216524829933),
                (1924.8039876153125, 643.2937559368262),
                (0.01, 100.0),
                (1969.3113504064222, 449.0733322490293),
                (1994.2721771549748, 251.38813945979763),
                (0.01, 100.0),
                (1999.4387161902614, 52.20032558936072),
                (1984.759686411272, -146.5130468968273),
                (0.01, 100.0),
                (1950.380786283397, -342.7796246580053),
                (1896.6432476908851, -534.6513403070427),
                (0.01, 100.0),
                (1824.0804489989723, -720.223748186242),
                (1733.412620943136, -897.6549271704451),
                (0.01, 100.0),
                (1625.5396978928063, -1065.1837628754197),
                (1501.532385445164, -1221.147427809275),
                (0.01, 100.0),
                (1362.621533008707, -1363.9978859655712),
                (1210.1859168602552, -1492.3172580398168),
                (0.01, 100.0),
                (1045.738554936144, -1604.8318947600565),
                (870.9116891917715, -1700.4250186450195),
                (0.01, 100.0),
                (687.4405845888832, -1778.1478087125588),
                (497.14630551569275, -1837.228818115766),
                (0.01, 100.0),
                (301.917640594537, -1877.081631230901),
                (103.69235528453706, -1897.310684195789),
                (0.01, 100.0),
                (-95.56204164117698, -1897.715191126237),
                (-293.8678268390747, -1878.2911370403353),
                (0.01, 100.0),
                (-489.2566925247651, -1839.2313177096428),
                (-679.7892831472784, -1780.9234260417),
                (0.01, 100.0),
                (-863.5744446945013, -1703.946203987716),
                (-1038.7879955684612, -1609.063698170126),
                (0.01, 100.0),
                (-1203.6908327179196, -1497.2176762464742),
                (-1356.6461933136654, -1369.518279281913),
                (0.01, 100.0),
                (-1496.1359006336984, -1227.2330029113123),
                (-1620.775432907833, -1071.774116659763),
                (0.01, 100.0),
                (-1729.327665554083, -904.6846462925339),
                (-1820.7151504066405, -727.6230583283163),
                (0.01, 100.0),
                (-1894.0308100564841, -542.3467987314779),
                (-1948.5469411566708, -350.6948491719859),
                (0.01, 100.0),
                (-1983.7224373289255, -154.56947399293577),
                (-1999.208159979704, 44.0826609416527),
                (0.01, 100.0),
                (-1994.850403717053, 243.2898101116614),
                (-1970.692421971858, 441.07471913680826),
                (0.01, 100.0),
                (-1926.973997680743, 635.4742502514404),
                (-1864.1290632918588, 824.558867663181),
                (0.01, 100.0),
                (-1782.7813937164822, 1006.4517893911639),
                (-1683.7384149765392, 1179.3476154900202),
                (0.01, 100.0),
                (-1567.9831900010743, 1341.5302477629189),
                (-1436.6646611175943, 1491.389923099433),
                (0.01, 100.0),
                (-1291.0862460876044, 1627.4391913717864),
                (-1132.6929008777531, 1748.3276792989684),
                (0.01, 100.0),
                (-963.0567775766038, 1852.8554937382078),
                (-783.8616198110719, 1939.9851313678505),
                (0.01, 100.0),
                (-596.8860505477198, 2008.85177655064),
                (-403.9859181578136, 2058.7718851647387),
                (0.01, 100.0),
                (-207.0758759723896, 2089.2499692026513),
                (-8.11037816166985, 2099.9835147966874),
                (0.01, 100.0),
            ],
        )
