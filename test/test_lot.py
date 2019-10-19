#pylint: disable=attribute-defined-outside-init, wrong-import-position
import unittest
import sys
sys.path.append('/Users/sani/Documents/PlanComm/Glens/glens_setback_analysis')
from lot import Lot

class TestLog(unittest.TestCase):

    def setUp(self):
        self.lot1_4 = Lot(
            front_sb=1,
            sm_side_sb=2,
            lg_side_sb=3,
            rear_sb=4,
        )

        self.lot4_1 = Lot(
            front_sb=4,
            sm_side_sb=3,
            lg_side_sb=2,
            rear_sb=1,
        )

        self.lotfoo = Lot(
            front_sb='foo',
            sm_side_sb=2,
            lg_side_sb=3,
            rear_sb='foo',
        )

    def test_sorted_sb_object(self):
        sorted_obj = self.lot1_4.get_sorted_setbacks_object()
        self.assertEqual(sorted_obj[0][Lot.SB_TYPE], Lot.FRONT_SB)
        self.assertEqual(self.lot1_4.get_closest_boundary(), Lot.FRONT_SB)

        sorted_obj = self.lot4_1.get_sorted_setbacks_object()
        self.assertEqual(sorted_obj[0][Lot.SB_TYPE], Lot.REAR_SB)
        self.assertEqual(self.lot4_1.get_closest_boundary(), Lot.REAR_SB)

        sorted_obj = self.lotfoo.get_sorted_setbacks_object()
        self.assertEqual(sorted_obj[0][Lot.SB_TYPE], Lot.SM_SIDE_SB)
        self.assertEqual(self.lotfoo.get_closest_boundary(), Lot.SM_SIDE_SB)


if __name__ == '__main__':
    unittest.main()
