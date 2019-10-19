#pylint: disable=invalid-name, unnecessary-pass

import csv
from lot import Lot

class GlensCSVImporter:

    SETBACKS_CSV = 'setbacks.csv'

    STREET = 'Street'
    ST_NUMBER = 'No'
    APN = 'APN'
    LOT_AREA = 'Lot Area'
    RES_SIZE = 'ResSize'
    YR_BUILT = 'YrBlt'
    YR_RENO = 'Reno/New:'
    FRONT_SB = 'Front'
    SM_SIDE_SB = 'Side_Sm'
    LG_SIDE_SB = 'Side_Lg'
    REAR_SB = 'Rear'

    def __init__(self):
        self.lots = []


    def import_csv(self):
        csvi = GlensCSVImporter
        with open(GlensCSVImporter.SETBACKS_CSV) as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                lot = Lot(
                    street=row[csvi.STREET],
                    st_number=row[csvi.ST_NUMBER],
                    apn=row[csvi.APN],
                    lot_area=row[csvi.LOT_AREA],
                    res_size=row[csvi.RES_SIZE],
                    yr_built=row[csvi.YR_BUILT],
                    yr_reno=row[csvi.YR_RENO],
                    front_sb=row[csvi.FRONT_SB],
                    sm_side_sb=row[csvi.SM_SIDE_SB],
                    lg_side_sb=row[csvi.LG_SIDE_SB],
                    rear_sb=row[csvi.REAR_SB],
                )
                self.lots.append(lot)
        self.lots.sort(key=self.get_lot_area_for_sort)

    def get_lots(self):
        return self.lots

    def get_lot_area_for_sort(self, lot: Lot):
        return lot.lot_area
        if isinstance(lot.lot_area, int):
            return lot.lot_area
        return 25000

if __name__ == "__main__":
    csvimp = GlensCSVImporter()
    csvimp.import_csv()
    pass