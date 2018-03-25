import argparse
import inspect
import re

class testproperties(object):

    @property
    def blib_library_file(self):
        try:
            return self.BLIB_LIBRARY_FILE
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'blib_library_file' is not yet set." ])
            raise ValueError(err)

    @blib_library_file.setter
    def blib_library_file(self, value):
        self.BLIB_LIBRARY_FILE = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.BLIB_LIBRARY_FILE = False

    @blib_library_file.deleter
    def blib_library_file(self):
        del self.BLIB_LIBRARY_FILE

    @property
    def clear_precursor(self):
        try:
            return self.CLEAR_PRECURSOR
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'clear_precursor' is not yet set." ])
            raise ValueError(err)

    @clear_precursor.setter
    def clear_precursor(self, value):
        self.CLEAR_PRECURSOR = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.CLEAR_PRECURSOR = False

    @clear_precursor.deleter
    def clear_precursor(self):
        del self.CLEAR_PRECURSOR

    @property
    def top_peaks_for_search(self):
        try:
            return self.TOP_PEAKS_FOR_SEARCH
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'top_peaks_for_search' is not yet set." ])
            raise ValueError(err)

    @top_peaks_for_search.setter
    def top_peaks_for_search(self, value):
        self.TOP_PEAKS_FOR_SEARCH = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.TOP_PEAKS_FOR_SEARCH = False

    @top_peaks_for_search.deleter
    def top_peaks_for_search(self):
        del self.TOP_PEAKS_FOR_SEARCH

    @property
    def mz_window(self):
        try:
            return self.MZ_WINDOW
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'mz_window' is not yet set." ])
            raise ValueError(err)

    @mz_window.setter
    def mz_window(self, value):
        self.MZ_WINDOW = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.MZ_WINDOW = False

    @mz_window.deleter
    def mz_window(self):
        del self.MZ_WINDOW

    @property
    def min_peaks(self):
        try:
            return self.MIN_PEAKS
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'min_peaks' is not yet set." ])
            raise ValueError(err)

    @min_peaks.setter
    def min_peaks(self, value):
        self.MIN_PEAKS = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.MIN_PEAKS = False

    @min_peaks.deleter
    def min_peaks(self):
        del self.MIN_PEAKS

    @property
    def low_charge(self):
        try:
            return self.LOW_CHARGE
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'low_charge' is not yet set." ])
            raise ValueError(err)

    @low_charge.setter
    def low_charge(self, value):
        self.LOW_CHARGE = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.LOW_CHARGE = False

    @low_charge.deleter
    def low_charge(self):
        del self.LOW_CHARGE

    @property
    def high_charge(self):
        try:
            return self.HIGH_CHARGE
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'high_charge' is not yet set." ])
            raise ValueError(err)

    @high_charge.setter
    def high_charge(self, value):
        self.HIGH_CHARGE = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.HIGH_CHARGE = False

    @high_charge.deleter
    def high_charge(self):
        del self.HIGH_CHARGE

    @property
    def report_matches(self):
        try:
            return self.REPORT_MATCHES
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'report_matches' is not yet set." ])
            raise ValueError(err)

    @report_matches.setter
    def report_matches(self, value):
        self.REPORT_MATCHES = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.REPORT_MATCHES = False

    @report_matches.deleter
    def report_matches(self):
        del self.REPORT_MATCHES

    @property
    def psm_result_file(self):
        try:
            return self.PSM_RESULT_FILE
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'psm_result_file' is not yet set." ])
            raise ValueError(err)

    @psm_result_file.setter
    def psm_result_file(self, value):
        self.PSM_RESULT_FILE = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.PSM_RESULT_FILE = False

    @psm_result_file.deleter
    def psm_result_file(self):
        del self.PSM_RESULT_FILE

    @property
    def report_file(self):
        try:
            return self.REPORT_FILE
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'report_file' is not yet set." ])
            raise ValueError(err)

    @report_file.setter
    def report_file(self, value):
        self.REPORT_FILE = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.REPORT_FILE = False

    @report_file.deleter
    def report_file(self):
        del self.REPORT_FILE

    @property
    def preserve_order(self):
        try:
            return self.PRESERVE_ORDER
        except (NameError, AttributeError) as e:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": 'preserve_order' is not yet set." ])
            raise ValueError(err)

    @preserve_order.setter
    def preserve_order(self, value):
        self.PRESERVE_ORDER = value
        if re.match('^\s*OPTIONAL\s*$', value):
            self.PRESERVE_ORDER = False

    @preserve_order.deleter
    def preserve_order(self):
        del self.PRESERVE_ORDER

if __name__ == '__main__':
    o = testproperties()
    _description = ''.join(["Put the description lines here. "]) 
    # Argument parser 
 
    #=== REMEMBER !! =========================================================== 
    # If you change the defaults here, be sure to change the defaults in the  
    # __init__ and in the set() method...since these are only called at the  
    # command line 
    #=========================================================================== 
    parser = argparse.ArgumentParser(description=_description) 
 
    parser.add_argument("--blib_library_file", action="store", dest="blib_library_file", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--clear_precursor", action="store", dest="clear_precursor", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--top_peaks_for_search", action="store", dest="top_peaks_for_search", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--mz_window", action="store", dest="mz_window", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--min_peaks", action="store", dest="min_peaks", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--low_charge", action="store", dest="low_charge", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--high_charge", action="store", dest="high_charge", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--report_matches", action="store", dest="report_matches", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--psm_result_file", action="store", dest="psm_result_file", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--report_file", action="store", dest="report_file", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
    parser.add_argument("--preserve_order", action="store", dest="preserve_order", 
                        required=True, 
                        help=''.join(["Put the variable help here. "]) ) 
 
