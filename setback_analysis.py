#pylint: disable=invalid-name, unnecessary-pass

from setback_analyzer import SetbackAnalyzer
from setbacks import SetbackDefinition, Setbacks


CURRENT_SIDE_SETBACK = 15
CURRENT_FRONT_SETBACK = 30
CURRENT_REAR_SETBACK = 25

test_setbacks = []

front_setback = SetbackDefinition(maximum=CURRENT_FRONT_SETBACK)
side_setback = SetbackDefinition(maximum=CURRENT_SIDE_SETBACK)
rear_setback = SetbackDefinition(maximum=CURRENT_REAR_SETBACK)

test_setbacks.append(Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
))

front_setback = SetbackDefinition(maximum=CURRENT_FRONT_SETBACK / 2)
side_setback = SetbackDefinition(maximum=CURRENT_SIDE_SETBACK / 2)
rear_setback = SetbackDefinition(maximum=CURRENT_REAR_SETBACK / 2)

test_setbacks.append(Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
))

front_setback = SetbackDefinition(
    maximum=25,
    lot_area_for_max=20000,
    minimum=12.5,
    lot_area_for_min=4500,
)
side_setback = SetbackDefinition(
    maximum=15,
    lot_area_for_max=20000,
    minimum=7.5,
    lot_area_for_min=4500
)
rear_setback = SetbackDefinition(
    maximum=25,
    lot_area_for_max=20000,
    minimum=12.5,
    lot_area_for_min=4500
)

test_setbacks.append(Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
))


test_setbacks.append(Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
    setback_for_closest_bounary=5,
    apply_closest_boundary_sb_only_to_sides=True,
))

test_setbacks.append(Setbacks(
    front=front_setback,
    sm_side=side_setback,
    lg_side=side_setback,
    rear=rear_setback,
    setback_for_closest_bounary=5,
    max_lot_area_for_closest_boundary=15000,
))


# analyzer = SetbackAnalyzer(test_setbacks[-1])
# print(analyzer.get_violations_summary_text())
# print(analyzer.get_violations_details_text())

analyzers = []
for setbacks in test_setbacks:
    analyzers.append(SetbackAnalyzer(setbacks))

# for i, analyzer in enumerate(analyzers):
#     if i == 3:
#         pass
#         print(analyzer.get_violations_summary_text())
#         print(analyzer.get_violations_details_text())

print(analyzers[-1].get_violations_summary_text())
print(analyzers[-1].get_violations_details_text())

pass
