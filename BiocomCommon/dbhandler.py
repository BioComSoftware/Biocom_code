##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
from test.test_support import args_from_interpreter_flags
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.4.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from common.checks                      import *
from common.errorhandler.trywrappers    import raisetry
from common.errorhandler.trywrappers    import handlertry
from common.errorhandler.messages       import MESSAGE as MSG
from confighandler                      import ConfigHandler
from inspect                            import getmembers
from inspect                            import stack
from common.loghandler                  import log

import abc
import MySQLdb
import pymssql
import re
import sys
import time

class DBHandlerAbstract(object): # ABSTRACT CLASS ------------------------------
    """
    """
    __metaclass__ = abc.ABCMeta
    
    @abc.abstractmethod
    def close(self):
        """
        :NAME:
            
        :DESCRIPTION:
            
        :ARGUMENTS:

        :RETURNS:
            
        :USAGE:
        """
        pass


class DBHandler(object): # FACTORY ---------------------------------------------
    """
    This is a factory class that will call and return a subclass.

    It is NOT an abstract class.

    The objects classes that are instantiated by this factory will be 
    subclasses of DBHandler  
    """
    @staticmethod
    def handler(service, *args, **kwargs):
        # Microsoft SQL (mssql)
        if      re.match("^(\s*)ms(\s*)sql.*$", str(service.lower())):
            return DBHandler_MSSQL(*args, **kwargs)
        
        # MySQL
        elif    re.match("^(\s*)my(\s*)sql.*$", str(service.lower())):
            return DBHandler_MYSQL(*args, **kwargs)

        else:
            log.error(MSG.DBHandlerNotProvided())
            raise TypeError('DBHandler service not provided.')


# =============================================================================
# EDIT HANDLER DEFAULTS FOR ALL DBHandlerAbstract CLASSES HERE 
class DBHandler_defaults(object):
    def __init__(self):
        self.db_host    = '10.208.183.196'
        self.db_name    = 'DENTRIXTEST'
        self.db_port    = 1433
# =============================================================================

    
class DBHandler_MYSQL(DBHandlerAbstract): # FUNCTIONAL CLASS ------------------
    def __init__(self):
        raise NotImplementedError
      
        
class DBHandler_MSSQL(DBHandlerAbstract): # FUNCTIONAL CLASS ------------------
    def __init__(self, *args, **kwargs):

        self.config     = ConfigHandler()     
        self.args       = args
        self.kwargs     = kwargs
        self.default    = DBHandler_defaults()
        
        self._check_host()
        self._check_db_name()
        self._check_db_port()

        # Sets database parameters from dbvars.cfg
#         self._set_db_vars()
#         
#         # Check for overriding vars passed into __init__
#         if host     is not None: self.dbvars['host'] = str(host)
#         if database is not None: self.dbvars['database'] = str(database)
#         if port     is not None: self.dbvars['port'] = str(port) 
#         if user     is not None: self.dbvars['user'] = str(user) 
#         if password is not None: self.dbvars['password'] = str(password) 
#         
#         # Actually create the DB connection and cursor
#         self._set_db()
# 
#         self.values = {}

        log.debug("DBHandler set successfully.")
            
    def _check_host(self):
        try:
            # Errors if it doesnt exist
            self.config.db_host
            # Overrides self.config.db_host if it was passed in
            self.config.db_host = self.kwargs.pop("db_host", self.config.db_host) 

        except AttributeError as e:
            log.error(MSG.DBHostNotConfigured())
            self.config.db_host = self.default.db_host
    
        if (      
            (checkIP(self.config.db_host) is False) and 
            (checkServername(self.config.db_host) is False) 
            ):
            log.error(MSG.DBHostImproperlyConfigured())
            raise AttributeError("Invalid database host name '" + str(self.config.db_host) + "'")

        log.debug('DBHandler.db_host: ' + str(self.config.db_host))
    
    def _check_db_name(self):
        try:
            # Errors if it doesnt exist
            self.config.db_name
            # Overrides self.config.db_host if it was passed in
            self.config.db_name = self.kwargs.pop("db_name", self.config.db_name) 

        except AttributeError as e:
            log.error(MSG.DBNameNotConfigured())
            self.config.db_name = self.default.db_name
    
        if (checkString(self.config.db_name) is False):
            log.error(MSG.DBNameImproperlyConfigured())
            raise AttributeError("Invalid database name '" + str(self.config.db_name) + "'")

        log.debug('DBHandler.db_name: ' + str(self.config.db_name))

    def _check_db_port(self):
        try:
            # Errors if it doesnt exist
            self.config.db_port
            # Overrides self.config.db_host if it was passed in
            self.config.db_port = self.kwargs.pop("db_port", self.config.db_port) 

        except AttributeError as e:
            log.error(MSG.DBPortNotConfigured())
            self.config.db_port = self.default.db_port
    
        if (checkInt(self.config.db_port) is False):
            log.error(MSG.DBPortImproperlyConfigured())
            raise AttributeError("Invalid database port '" + str(self.config.db_port) + "'")

        log.debug('DBHandler.db_port: ' + str(self.config.db_port))

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

    def _set_all_defaults(self):
        self.default_db_host = '10.208.183.196'

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

    def close(self):
        log.info('DBHandler closed.')
                                   
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
    class test(object):
        from confighandler import ConfigHandler
        
        def __init__(self):
            app_name   = 'dbhandler_test'
            logfile    = 'system'
            log_level  = 10
            screendump = True
        
#             log.info('Starting DentrixReporting logger...',
#                      app_name = app_name,
#                      logfile    = logfile,
#                      log_level  = log_level,
#                      screendump = screendump
#                      )        
            
    
            self.config = ConfigHandler(self,
                                        app_name   = app_name,
                                        logfile    = logfile,
                                        log_level  = log_level,
                                        screendump = screendump,
                                        config_file = "/Users/mikes/Documents/Eclipseworkspace/Telemend/Telemend-Dentrix-Reporting/conf/DentrixReporting.conf"
                                        )
            
            DBO = DBHandler.handler('mssql')
            print 'DBO = ', DBO   

    o = test()
