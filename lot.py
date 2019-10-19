class Lot:

    SB_TYPE = 'sb_type'
    SB = 'sb'

    FRONT_SB = 'front'
    SM_SIDE_SB = 'sm_side_sb'
    LG_SIDE_SB = 'lg_side_sb'
    REAR_SB = 'rear_sb'

    def __init__(
            self,
            street=None,
            st_number=None,
            apn=None,
            lot_area=None,
            res_size=None,
            yr_built=None,
            yr_reno=None,
            front_sb=None,
            sm_side_sb=None,
            lg_side_sb=None,
            rear_sb=None,
    ):
        self.street = street
        self.st_number = self.s_to_i(st_number)
        self.apn = self.s_to_i(apn)
        self.lot_area = self.s_to_i(lot_area)
        self.res_size = self.s_to_i(res_size)
        self.yr_built = self.s_to_i(yr_built)
        self.yr_reno = self.s_to_i(yr_reno)
        self.front_sb = self.s_to_i(front_sb)
        self.sm_side_sb = self.s_to_i(sm_side_sb)
        self.lg_side_sb = self.s_to_i(lg_side_sb)
        self.rear_sb = self.s_to_i(rear_sb)

    def s_to_i(self, string):
        try:
            result = int(string.replace(',', ''))
        except (ValueError, AttributeError):
            result = string
            # print(f'Could not get integer from: {string}')
        return result

    def get_sorted_setbacks_object(self):
        a = []
        if isinstance(self.front_sb, int):
            a.append({Lot.SB_TYPE: Lot.FRONT_SB, Lot.SB: self.front_sb})
        if isinstance(self.sm_side_sb, int):
            a.append({Lot.SB_TYPE: Lot.SM_SIDE_SB, Lot.SB: self.sm_side_sb})
        if isinstance(self.lg_side_sb, int):
            a.append({Lot.SB_TYPE: Lot.LG_SIDE_SB, Lot.SB: self.lg_side_sb})
        if isinstance(self.rear_sb, int):
            a.append({Lot.SB_TYPE: Lot.REAR_SB, Lot.SB: self.rear_sb})
        a.sort(key=self.get_sb_for_sort)
        return a

    def get_sb_for_sort(self, setbacks_object):
        return setbacks_object[Lot.SB]

    def get_closest_boundary(self):
        return self.get_sorted_setbacks_object()[0][Lot.SB_TYPE]

    def get_distance_to_closest_boundary(self):
        return self.get_sorted_setbacks_object()[0][Lot.SB]

