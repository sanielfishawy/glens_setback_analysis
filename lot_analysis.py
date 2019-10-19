#pylint: disable=invalid-name, unnecessary-pass

# from lot import Lot
from setbacks import Setbacks, SetbackDefinition
from setback_analyzer import SetbackAnalyzer

CURRENT_SIDE_SETBACK = 15
CURRENT_FRONT_SETBACK = 30
CURRENT_REAR_SETBACK = 25


front_setback = SetbackDefinition(maximum=CURRENT_FRONT_SETBACK)
side_setback = SetbackDefinition(maximum=CURRENT_SIDE_SETBACK)
rear_setback = SetbackDefinition(maximum=CURRENT_REAR_SETBACK)

setbacks = (Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
))

sba = SetbackAnalyzer(setbacks=setbacks)

lots_with_zero_setback = []
for lot in sba.lots:
    if lot.get_distance_to_closest_boundary() == 0:
        lots_with_zero_setback.append(lot)

pass