# pylint: disable=C0413
# pylint: disable=no-value-for-parameter,line-too-long
import sys
import unittest
sys.path.insert(0, '/Users/sani/Documents/PlanComm/Glens/glens_setback_analysis')

from setbacks import SetbackDefinition #pylint: disable

class TestSetbackAnalyzer(unittest.TestCase):

    def setUp(self):
        self.setback_no_slope = SetbackDefinition(maximum=1)
        self.setback_with_slope = SetbackDefinition(
            maximum=100,
            lot_area_for_max=1000,
            minimum=50,
            lot_area_for_min=200,
        )

    def test_setback_with_no_slope(self):
        self.assertEqual(self.setback_no_slope.max, 1)
        self.assertEqual(self.setback_no_slope.get_setback_for_lot_area(None), self.setback_no_slope.max)

    def test_setback_with_slope(self):
        self.assertEqual(self.setback_with_slope.get_setback_for_lot_area(600), 75)
        self.assertEqual(self.setback_with_slope.get_setback_for_lot_area(1000), 100)
        self.assertEqual(self.setback_with_slope.get_setback_for_lot_area(1001), 100)
        self.assertEqual(self.setback_with_slope.get_setback_for_lot_area(200), 50)
        self.assertEqual(self.setback_with_slope.get_setback_for_lot_area(100), 50)

    def test_formula(self):
        print(self.setback_with_slope.get_formula())
        print(self.setback_no_slope.get_formula())

if __name__ == '__main__':
    unittest.main()