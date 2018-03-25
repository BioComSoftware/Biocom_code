##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.3.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from checklist import checklist
from inspect import getmembers
from inspect import stack
from logger import check_logger
from logger import create_logger
# from functions import *

import custom_errors
import ConfigParser
import MySQLdb
import re
import sys
import time

class db(object):
    def __init__(self, 
                 host = None, 
                 database = None, 
                 port = 3306, 
                 user = None, 
                 password = None, 
                 log = None,
                 ):
        
#         try:
            # Check if logger passed, else create new one
            self.log = check_logger(log, self)
            # Set error handler
            self.error = custom_errors.error(self)
            # Sets database parameters from dbvars.cfg
            self._set_db_vars()
            
            # Check for overriding vars passed into __init__
            if host     is not None: self.dbvars['host'] = str(host)
            if database is not None: self.dbvars['database'] = str(database)
            if port     is not None: self.dbvars['port'] = str(port) 
            if user     is not None: self.dbvars['user'] = str(user) 
            if password is not None: self.dbvars['password'] = str(password) 
            
            # Actually create the DB connection and cursor
            self._set_db()

            self.values = {}

            self.log.info("Done.")
            

    
#         except Exception, e:
#             self.lasterr = error(self, e, getmembers(self), stack()

    def _checklistlengths(self, columns, values):
        if ((checklist(columns)) and (checklist(values))):
            if (len(columns) != len(values)):
                e = "".join(["'dbhandler.checklistlengths': The number of items ", 
                             "in 'columns' and 'values' ", 
                             "do not appear to match. ", 
                             "If you need to insert a blank value, use ''.", 
                             "Skipping."])
                self.log.error(e)
                self.log.error("".join(["columns: (",str(len(columns)),")",
                                        str(columns)]))
                self.log.error("".join(["values: (",str(len(values)),")",
                                        str(columns)]))                
                return False
            else: return True
        else:
            e = "".join(["'dbhandler.checklistlengths': The parameters ", 
                         "'columns' and 'values' ", 
                         "do not appear to be lists. ", 
                         "Each of these must be passed ", 
                         "as a list of strings."])
            self.log.error(e)
            self.log.error("".join(["columns: (",
                                    str(len(columns)),
                                    ")",
                                    str(columns)]))
            self.log.error("".join(["values: (",
                                    str(len(values)),
                                    ")",
                                    str(values)]))            
            return False                

    def _set_db(self):
        self.log.info("Starting MySQL database connection ...")
        self.log.debug("Creating connection...")
        
        self.conn=MySQLdb.connect(host    = self.dbvars['host'],
                                  db      = self.dbvars['database'],
                                  port    = int(self.dbvars['port']),
                                  user    = self.dbvars['user'],
                                  passwd  = self.dbvars['password']
                                )
        
        self.log.debug("Done.")

        self.log.debug("Verifying connection...")
        if not self._verify_connection():
            e = ('Fatal: DBStartFailure')
            raise Exception(e)
        self.log.debug("Done.")

        self.log.debug("Creating cursor...")
        self.cursor = self.conn.cursor()
        self.log.debug("Done.")

        self.tables = []
        self.cursor.execute("""show tables;""")
        for row in self.cursor:
            self.tables.append(row[0]) 
        self.log.debug("Done.")
        
    def _set_db_vars(self, filename = "../etc/dbvars.cfg"):
        """
        _set_db_vars([filename])
        
        DESCRIPTION:
            Uses ConfigParser to set the column names for each table into
            variable self.columns[<table>]
            
            filename can be set for non-default configuration file name
            default = dbvars.cfg
            
        dbvars.cfg format 
            [tablename]
            column = 'ColumnsName1'
            column = 'ColumnsName2'
        
        NOTE: _set_db_vars should only be run ONCE in __init__
        """

        self.log.debug("Loading DB variables...")
        try:
            self.columns    = {}
            self.dbvars     = {} 
            
            config = ConfigParser.ConfigParser()
            self.log.debug("".join(["Reading: ", str(filename)]))
            config.read(filename)
    
            for section in config.sections():
                # Check for specific section, otherwise assume table
                if (section == 'database'): 
                    options = config.options(section)
                    for option in options:
                        self.dbvars[option]= str(config.get(section, option))
                    continue 
                
                try:
                    # Check if key "section" (for table) already exists
                    if self.columns[section]:
                        e = "".join([
                                "Table '", section, "' has already been set.",  
                                "Redundant section in configuration file.", 
                                "Skipping. Please check dbvars.cfg"
                                ])
                        self.log.error(e)
                        
                # "Table" key doesn't exist, create it as a list
                except (AttributeError, KeyError, IndexError):
                    self.columns[section] = []
    
                # Start loading list with the sections values
                options = config.options(section)
                for option in options:
                    self.columns[section].append(str(config.get(section, option)))

            return True

        except Exception, e:
            raise
            self.log.debug("".join(['dbhandler._set_db_varsDone: ', e]))
            return False

    def _cleanMysqlInsertString(self, _list, _quotes = False):
        """
        Takes a list of strings, and formats then into a single string
        which meets format for a MySQL insert statement
        """
        if checklist(_list): # If is a list
            result = "(" # Start result to be returned

            for _item in _list:

                # Strip carrage returns from _item
                _item = str(_item)
                _item = "".join(c for c in _item if c not in "\n\r")

                # If a number, strip spaces
                try:
                    if ((int(_item)) or (float(_item))):
                        _item = "".join(c for c in _item if not re.match("\s", c))
                except ValueError: # Fails if _item has string chars
                    pass
                 
                # String escape 
                _item = _item.encode("string_escape")

                # Add quotes if needed                
                if _quotes: 
                    _item = _item.center(len(_item)+2, "'")

                # Add item to the final return
                result = "".join([result, _item, ","])

            result = result[0:(len(result)-1)] # Remove last comma
            result = "".join([result, ")"]) # Add last paren

            return result
            
        # Raise error if _list is not a list
        else:
            e = "".join(["'dbhandler._cleanMysqlInsertString' ", 
                         "parameter is not a list."])
            raise TypeError(e)
        
    def _verify_connection(self):
#         try:
            self.log.debug("".join(['Checking DB connection to database: ', 
                                    str(self.dbvars['database'])]))
            self.conn.query("""show tables;""")
            test = self.conn.use_result()
            test = test.fetch_row()
            self.log.debug("Query result: " + str(test))
            return True
    
#         except Exception, e:
#             e = "".join(['DBPassThroughException:', str(e)])
#             self.lasterr = error(self, e, getmembers(self), stack())
#             return False
                            
    def writeRowsBuffer(self, table):
        """
        writeRowsBuffer(table)
        
        DESCRIPTION:
            Forms and writes an SQL statement to place data into "table"
            
            The columns for the table are stored in non-volatile parameter
            self.columns[<table>]. This is loaded at __init__
            
            The values for the row are stored in dynamic variable 
            self.values[<table>]. These are created dynamically as script runs
            by the method loadRowsBuffer(table, values)..
        """
        try:
            # Assemble write query
            # Check params
            _columns = self._cleanMysqlInsertString(self.columns[table])
            _values = ""
            
            try:
                if len(self.values[table]) < 1: 
                    self.log.info("self.values buffer is empty.")
                    return #End method execution 
                
            except (AttributeError, KeyError, ValueError):
                self.log.info("self.values buffer is empty.")
                return #End method execution 

            # Parse the values and add them to an SQL statement string                            
            for _valuelist in self.values[table]:
                _valuestring  = self._cleanMysqlInsertString(
                                        _valuelist, _quotes  = True)
                _values = "".join([_values,",", _valuestring])
                
            _values = _values[1:] # Pop leading comma off
                
            _sql = "".join(["INSERT INTO ", str(table), " ", 
                             _columns, " ", "VALUES ", _values, 
                             ';'])
            self.log.debug("Attempting insert with:")
            self.log.debug(_sql)

            # Only turn on for deep debugging
            # self.log.debug(_sql)

            try:
                with self.conn:
                    cur = self.conn.cursor()
                    cur.execute(_sql)
                    self.log.debug("Successful.")
                return True

            except Exception, e:
                self.log.debug("".join(["Failed with", str(e)]))

                if (("duplicate" in str(e).lower()) and overwrite):
                    self.log.error("".join(["Duplicate entry(s) found. ", 
                            "Overwrite is disabled in this script. ", 
                            "Continuing without writing."]))
#                     self.log.debug("Overwrite true, attempting update...")
#                     where1 = str(columns[0])
#                     where2 = str(values[0])  
#                     if self.updateRow(
#                         columns, values, table,
#                         where = "".join([where1,"=",where2]),  
#                         prikey = where1
#                         ):
#                         self.log.debug("Successful.")
#                         return True
#                     else:
#                         self.log.debug("Failed.")
                    return False
                else: 
                    # A method for hanlding duplicate overwrites 
                    # needs to be created
                    raise
            
        except Exception, e:
            e = "".join(["PassThroughException: Failed attempting to modify ", 
                         "database row: ", 
                         str(e)])
            self.lasterr = self.error.handle(e, getmembers(self), stack())    
        
    def loadRowsBuffer(self, table = None, values = None):
        """
        loadRowsBuffer(table, values)
        
        DESCRIPTION:
            Creates a list of lists "self.values[table]" as a buffer.
            
            Each list within self.values[table] is a row of data saved for 
            "table".
            
            When 'table' is sent to self.writeRowsBuffer(table), each list 
            found within self.values[table] is written as a row to 'table'.
        """
        #### ENABLE BELOW FOR CODING DEBUG ###
        # Check that keys for table have been set
#         try:
#             self.log.debug("".join(["Attempting loadRowsBuffer with '", 
#                                     str(table), "with:"]))
#             self.log.debug("".join(["Values: (", 
#                                     str(len(values)), ")", str(values)]))
#             
#         except (AttributeError, KeyError):
#             e = "".join(["FatalScriptError: dbahndler.write: ",
#                          "Table '", str(table), "' is not in self.columns.", 
#                          "Variables for dbahndler.columns['", 
#                          str(table), "' may not have been set." ])
#             self.lasterr = self.error.handle(e,inspect.getmembers(self),inspect.stack())
        #### ENABLE ABOVE BELOW FOR CODING DEBUG ###

        # Check that values passed is a list that contains at least one element
        try:
            if not checklist(values): raise TypeError
            values[0] # Errors if list is empty
        except (AttributeError, TypeError, IndexError):
            e = "".join(["FatalScriptError: dbahndler.write: ",
                         "Variable 'values' passed does not appear to be a ",
                         "valid list type or is of zero length. ."
                         ])
        
        try:
            # Check if key "table" already exists
            self.values[table]
        # "Table" key doesn't exist, create it as a list
        except (AttributeError, KeyError, IndexError):
            self.values[table] = []
        
        # Ensure the columns and values are lists of same length
        # NOTE: Checking PASSED values not self.values[table]
        if  self._checklistlengths(self.columns[table], values):
            # If no error, append self.values[table]
            # NOTE: This creates a list of list, don't uuse 
            # self.values[table] = values
            # self.values[table] will end up as a list of lists, with 
            # each list being a row to be added
            self.values[table].append(values)
        else:
            self.log.error("".join(["The length of the value list ", 
                                    "does not appear to match the columns. ", 
                                    "Skipping this value set."]))
            self.log.error("".join([str(values)]))        

        
if __name__ == "__main__":
    d = db(
           log = None,           
           )