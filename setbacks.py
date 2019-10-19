#pylint: disable=line-too-long
from lot import Lot


class SetbackDefinition:

    def __init__(
            self,
            maximum=None,
            lot_area_for_max=None, #if none then applies to all areas
            minimum=None, #if none then same as max
            lot_area_for_min=None,
    ):
        self.max = maximum
        self.lot_area_for_max = lot_area_for_max
        self.min = minimum
        self.lot_area_for_min = lot_area_for_min

    def get_setback_for_lot_area(self, lot_area):
        if self.lot_area_for_max is None:
            setback = self.max
        elif not isinstance(lot_area, int):
            setback = self.max
        elif lot_area >= self.lot_area_for_max:
            setback = self.max
        elif lot_area <= self.lot_area_for_min:
            setback = self.min
        else:
            setback = self.get_slope() * (lot_area - self.lot_area_for_min) + self.min
        return setback

    # m in y = mx + b
    def get_slope(self):
        slope = 0
        if self.lot_area_for_max is not None:
            slope = (1.0 * self.max - self.min) / (self.lot_area_for_max - self.lot_area_for_min)
        return slope

    def get_formula(self):
        if self.lot_area_for_max is None:
            formula = f'setback = {self.max}'
        else:
            formula = f'setback = {round(self.get_slope(), 6)} x (lot_area - {self.lot_area_for_min}) + {self.min} ' +\
            f'with maximum setback of {self.max} ' + \
            f'and minimum setback of {self.min}'
        return formula


class Setbacks:
    def __init__(
            self,
            front: SetbackDefinition = None,
            sm_side: SetbackDefinition = None,
            lg_side: SetbackDefinition = None,
            rear: SetbackDefinition = None,
            setback_for_closest_bounary=None, # allows a special setback to be set for the closest boundary which overrides the defined setback.
            apply_closest_boundary_sb_only_to_sides=False,
            max_lot_area_for_closest_boundary=None,
    ):
        self.front = front
        self.sm_side = sm_side
        self.lg_side = lg_side
        self.rear = rear
        self.setback_for_closest_bounary = setback_for_closest_bounary
        self.apply_closest_boundary_sb_only_to_sides = apply_closest_boundary_sb_only_to_sides
        self.max_lot_area_for_closest_boundary = max_lot_area_for_closest_boundary

    def get_front_setback_for_lot(self, lot: Lot):
        return self.get_setback_for_lot(self.front, Lot.FRONT_SB, lot)

    def get_front_formula(self):
        return self.front.get_formula() + self.get_closest_boundary_formula()

    def get_sm_side_setback_for_lot(self, lot: Lot):
        return self.get_setback_for_lot(self.sm_side, Lot.SM_SIDE_SB, lot)

    def get_sm_side_formula(self):
        if isinstance(self.setback_for_closest_bounary, int) and self.apply_closest_boundary_sb_only_to_sides:
            return f'setback = {self.setback_for_closest_bounary}'
        else:
            return self.sm_side.get_formula() + self.get_closest_boundary_formula()

    def get_lg_side_setback_for_lot(self, lot: Lot):
        return self.get_setback_for_lot(self.lg_side, Lot.LG_SIDE_SB, lot)

    def get_lg_side_formula(self):
        return self.lg_side.get_formula() + self.get_closest_boundary_formula()

    def get_rear_setback_for_lot(self, lot: Lot):
        return self.get_setback_for_lot(self.rear, Lot.REAR_SB, lot)

    def get_rear_formula(self):
        return self.rear.get_formula() + self.get_closest_boundary_formula()

    def get_closest_boundary_formula(self):
        txt = ''
        if isinstance(self.setback_for_closest_bounary, int) and not self.apply_closest_boundary_sb_only_to_sides:
            txt += f'\n   or setback is {self.setback_for_closest_bounary}ft if residence is closest to this boundary.\n'
            if isinstance(self.max_lot_area_for_closest_boundary, int):
                txt += f'   and lot area <= {self.max_lot_area_for_closest_boundary} sqft'
        else:
            txt += ''
        return txt

    def get_setback_for_lot(
            self,
            setback_definition: SetbackDefinition,
            boundary,
            lot: Lot,
    ):
        calculated_setback = setback_definition.get_setback_for_lot_area(lot.lot_area)

        if self.setback_for_closest_bounary and \
            (not isinstance(self.max_lot_area_for_closest_boundary, int) or lot.lot_area <= self.max_lot_area_for_closest_boundary):
            if self.apply_closest_boundary_sb_only_to_sides:
                if boundary is Lot.SM_SIDE_SB:
                    return min(calculated_setback, self.setback_for_closest_bounary)
                else:
                    return calculated_setback
            else:
                if lot.get_closest_boundary() is boundary:
                    return min(calculated_setback, self.setback_for_closest_bounary)
                else:
                    return calculated_setback
        else:
            return calculated_setback

class SetbackViolation:

    def __init__(
            self,
            lot: Lot,
            setbacks: Setbacks,
    ):
        self.lot = lot
        self.setbacks = setbacks

    def has_violation(self, actual_distance, get_setback_method):
        if not isinstance(actual_distance, int):
            return 1
        if actual_distance < get_setback_method(self.lot):
            return 1
        return 0

    def has_front_violation(self):
        return self.has_violation(self.lot.front_sb, self.setbacks.get_front_setback_for_lot)

    def has_sm_side_violation(self):
        return self.has_violation(self.lot.sm_side_sb, self.setbacks.get_sm_side_setback_for_lot)

    def has_lg_side_violation(self):
        return self.has_violation(self.lot.lg_side_sb, self.setbacks.get_lg_side_setback_for_lot)

    def has_rear_violation(self):
        return self.has_violation(self.lot.rear_sb, self.setbacks.get_rear_setback_for_lot)

    def num_violations(self):
        return self.has_front_violation() + self.has_sm_side_violation() + self.has_lg_side_violation() + self.has_rear_violation()

    def has_violations(self):
        return self.num_violations()

    def get_violations_text(self):
        if self.num_violations() == 0:
            text = 'no violations'
        else:
            text = f'{self.num_violations()} violations: '
            if self.has_front_violation():
                text += f'front: setback={self.setbacks.get_front_setback_for_lot(self.lot):0.0f} actual={self.lot.front_sb} '
            if self.has_sm_side_violation():
                text += f'sm_side: setback={self.setbacks.get_sm_side_setback_for_lot(self.lot):0.0f} actual={self.lot.sm_side_sb} '
            if self.has_lg_side_violation():
                text += f'lg_side: setback={self.setbacks.get_lg_side_setback_for_lot(self.lot):0.0f} actual={self.lot.lg_side_sb} '
            if self.has_rear_violation():
                text += f'rear: setback={self.setbacks.get_rear_setback_for_lot(self.lot):0.0f} actual={self.lot.rear_sb} '
        return text
