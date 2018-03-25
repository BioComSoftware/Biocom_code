
# from csv import DictWriter

from lib import *
from pandas import *
from win32com.shell import shellcon, shell

import csv
import inspect
import os
import sys
import time

class CSVFileWriter(object):
    def __init__(self, 
                 calling_obj,
                 filename = None):
        # Check the validity of the filename and path
        # If none, then create based on date
        
        if filename is None:
            filename = "".join(["agmarknet.", 
                                time.strftime("%Y%m%d%H%M%S."), 
            # Extension MUST be xls for xls file, or pandas writer engine fails
                                "xls"])
            
            # Default to current users desktop
            if sys.platform.startswith('win'):
                userhome = shell.SHGetFolderPath(0, 
                                                 shellcon.CSIDL_PROFILE, 
                                                 None, 
                                                 0)
                userhome = userhome.encode(sys.stdout.encoding)
#                 userhome = os.path.expanduser('~')
                desktop = "".join([userhome, '\\Desktop\\'])
                filename = "".join([desktop, filename])
            # If not windows, drop top local dir via linux format
            else:
                filename = "".join(["./", filename])
                
        # If pathname was passed, verify it at least has a directory indicator    
        encoding = sys.stdout.encoding
        filename.encode(sys.stdout.encoding)
        if sys.platform.startswith('win'):
            if "\\" not in str(filename):
                filename = "".join([".\\", str(filename)])
        else:
            if "/" not in str(filename):
                filename = "".join(["./", str(filename)])
            
        calling_obj.log.debug("".join(["Checking filename and path: ",filename]))
        if not checkpath.directoryexists(filename):
            e = ("InvalidFilePath: '" + str(filename) + "'" + ". ") 
            self.lasterr = calling_obj.error.handle(e,inspect.getmembers(self),inspect.stack())
            sys.exit(1) # This can be replaced with handling method

        self.filename = filename
        self._DataFrame = {}
        
#         self.writer = csv.writer(
#                                  open(self.filename, 'wb'),
# #                                  delimiter=',', 
# #                                  quoting=csv.QUOTE_MINIMAL
#                                  )

    def add_row(self, 
                _row, # Must be list of strings
                sheetname,
                 ):
        try:
            _row.append("DELETEME")
            _row.pop(len(_row)-1)
        except Exception, e:
            e = "'row' passed to csvfilewriter.add_row is not a list."
            raise TypeError(e)

        try:
            if sheetname not in self._DataFrame.keys():
                self._DataFrame[sheetname] = []
            self._DataFrame[sheetname].append(_row)
        except IndexError, e:
            e = "Invalid 'sheetname' passed to csvfilewriter.add_row."
            raise TypeError(e)
            
    def write(self):
        with ExcelWriter(self.filename) as writer:
            for key in self._DataFrame.keys():
                df = DataFrame(self._DataFrame[key])
                df.to_excel(writer, sheet_name=key, index=False)

    def close(self):
        self.writer.close()
        
    