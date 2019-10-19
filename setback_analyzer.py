#pylint: disable=invalid-name, unnecessary-pass, line-too-long

from setbacks import Setbacks, SetbackViolation
from import_data import GlensCSVImporter
from colorama import Fore, Style

class SetbackAnalyzer:

    MIN_DISTANCE_TO_BOUND_FOR_UNSAVABLE_LOT = 5

    def __init__(self, setbacks: Setbacks):
        self.csvi = GlensCSVImporter()
        self.csvi.import_csv()
        self.lots = self.csvi.get_lots()
        self.setbacks = setbacks

        self.violations = []
        for lot in self.lots:
            self.violations.append(SetbackViolation(lot, self.setbacks))

        self.true_violations = []
        for violation in self.violations:
            if violation.has_violations():
                self.true_violations.append(violation)

        self.unsavable_lots = []
        for lot in self.lots:
            if lot.get_distance_to_closest_boundary() < SetbackAnalyzer.MIN_DISTANCE_TO_BOUND_FOR_UNSAVABLE_LOT:
                self.unsavable_lots.append(lot)

        self.savable_violations = []
        for violation in self.true_violations:
            if violation.lot.get_distance_to_closest_boundary() >= SetbackAnalyzer.MIN_DISTANCE_TO_BOUND_FOR_UNSAVABLE_LOT:
                self.savable_violations.append(violation)

    def get_num_violations(self):
        return len(self.true_violations)

    def get_num_lots(self):
        return len(self.lots)

    def get_num_unsavable_lots(self):
        return len(self.unsavable_lots)

    def get_fraction_violations(self):
        return 1.0 * self.get_num_violations() / self.get_num_lots()

    def get_fraction_savable_violations_of_savable_lots(self):
        return 1.0 * self.get_num_savable_violations() / self.get_num_savable_lots()

    def get_num_savable_lots(self):
        return self.get_num_lots() - self.get_num_unsavable_lots()

    def get_fraction_savable_lots(self):
        return 1.0 * self.get_num_savable_lots() / self.get_num_lots()

    def get_fraction_unsavable_lots(self):
        return 1.0 * self.get_num_unsavable_lots() / self.get_num_lots()

    def get_num_savable_violations(self):
        return len(self.savable_violations)

    def get_violations_summary_text(self):
        txt = f'\n\nSetback Rules:\n'
        txt += f'   Front:  {self.setbacks.get_front_formula()}\n'
        txt += f'   SmSide: {self.setbacks.get_sm_side_formula()}\n'
        txt += f'   LgSide: {self.setbacks.get_lg_side_formula()}\n'
        txt += f'   Rear:   {self.setbacks.get_rear_formula()}\n'
        txt += '\n'
        txt += f'Effect of rules:\n'
        txt += f'   {self.get_num_lots()} total lots\n'
        txt += f'   {self.get_num_unsavable_lots()} ({self.get_fraction_unsavable_lots():.0%}) unconformable lots. (min distance < {SetbackAnalyzer.MIN_DISTANCE_TO_BOUND_FOR_UNSAVABLE_LOT}ft)\n'
        txt += f'   {self.get_num_savable_lots()} ({self.get_fraction_savable_lots():.0%}) conformable lots. (min distance >= {SetbackAnalyzer.MIN_DISTANCE_TO_BOUND_FOR_UNSAVABLE_LOT}ft)\n\n'

        conforming = self.get_num_lots() - self.get_num_violations()
        txt += f'   {conforming} conforming lots / {self.get_num_lots()} total lots ({1 - self.get_fraction_violations():.0%})\n'
        txt += f'   {self.get_num_violations()} non-conforming lots / {self.get_num_lots()} total lots ({self.get_fraction_violations():.0%})\n\n'

        fraction_violations_of_savable = self.get_fraction_savable_violations_of_savable_lots()
        txt += f'   {self.get_num_savable_lots() - self.get_num_savable_violations()} conforming / {self.get_num_savable_lots()} conformable lots. ({1-fraction_violations_of_savable:.0%})\n'
        txt += f'   {self.get_num_savable_violations()} non-conforming lots / {self.get_num_savable_lots()} conformable lots. ({fraction_violations_of_savable:.0%})\n'
        return txt

    def get_violations_details_text(self):
        txt = '\n\n'
        for violation in self.true_violations:
            if violation.lot.get_distance_to_closest_boundary() < 5:
                txt += Fore.RED
            txt += f'{str(violation.lot.st_number):6} {violation.lot.street:10} [{violation.lot.apn}]'
            txt += f' {violation.lot.lot_area:6,}sqft : {violation.get_violations_text()}\n'
            txt += Style.RESET_ALL

        txt += '\n\n'
        return txt
