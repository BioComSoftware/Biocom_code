##############################################################################
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU LGPL License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# See the files gpl.txt and lgpl.txt packaged with this file.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "LGPLv3"
__license_file__= "lgpl.txt"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"

##############################################################################

from BiocomCommon.checks        import Checks
from BiocomCommon.confighandler import ConfigHandler
from BiocomCommon.loghandler    import log 

import inspect 
import re
import xml.etree.cElementTree as ET


class XMLHandler(object):
    """"""
    def __init__(self, *args, **kwargs):
        self.checks = Checks()
        self.config = ConfigHandler()        
        self.source = kwargs.pop('source', None)
        
    
    """ PROPERTIES ========================================================="""
    @property
    def source(self):
        try:
            return self._SOURCE
        except AttributeError as e:
            return None
        
    @source.setter
    def source(self, value):
        """"""
        if value is None: 
            log.debug("xmlhandler.source has been set to None.")
            self._SOURCE = None
            self._TREE    = None
            self._ROOT    = None
            return
        
        _value = str(value)

        if not self.checks.pathExists(_value):
            err = ''.join(["xmlhandler.source.setter: ", "The source path '", _value, "' appears invalid. "])
            raise ValueError(err)
        
        self._TREE = ET.parse(_value)
        self._ROOT = self._TREE.getroot()
        self._SOURCE = _value
        log.debug(''.join(["xmlhandler.source has been set to '", _value, "'."]))
                           
    @source.deleter
    def source(self):
        self._SOURCE = None
        self._TREE   = None
        self._ROOT   = None

    @property
    def tree(self):
        try:
            return self._TREE
        except AttributeError as e:
            return None
        
    @tree.setter
    def tree(self, value):
        err = ''.join(["xmlhandler.tree.setter: The 'tree' parameter cannot be manually set. Please set 'source' value instead."])
        raise NotImplementedError(err)
    
    @tree.deleter
    def tree(self):
        del source

    @property
    def root(self):
        try:
            return self._ROOT
        except AttributeError as e:
            return None
        
    @root.setter
    def root(self, value):
        err = ''.join(["xmlhandler.root.setter: The 'root' parameter cannot be manually set. Please set 'source' value instead."])
        raise NotImplementedError(err)
    
    @root.deleter
    def root(self):
        del source
    
    @property
    def elements(self):
        try:
            return self._ELEMENTS
        except (AttributeError, NameError) as e:
             self._ELEMENTS = []
             return self._ELEMENTS
             
    @elements.setter
    def elements(self, value):
        """
        value must be a string, in the format of an ElementTree findall
        statement.
        
        Currently, no string checks are performed. Screw up at your own risk.

        """
        # For now, does no check on the value string...so we assume the user
        # knows what the hell s/he's doing. 
        self._ELEMENTS = self.root.findall(value)
        
    @elements.deleter
    def elements(self):
        self._ELEMENTS = []

    @property
    def element(self):
        try: 
            return self._ELEMENT
        except (AttributeError, NameError) as e:
            self._ELEMENT = None
            return self._ELEMENT            
                
    @element.setter
    def element(self, value):
        """
        """
        err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": " ])

        def _passed_element(value):
            self._ELEMENT = value
            
        def _passed_tuple(value):
            if ( (len(value) < 2) or (len(value) > 3) ): 
                _err = ''.join([err, "Tuple must contain 2 or 3 values in the format (attrib_name, attrib_value, number_of_matched_instance). "])
                raise ValueError(_err)
            # Get found instance number _end_count
            try:                _end_count = value[2]
            except IndexError:  _end_count = 1
            # Search elements
            _count = 0
            for elem in self.dump():
                try:
                    if elem.attrib[value[0]] == value[1]:
                        # Check which numbered match this is
                        _count += 1 # Increment match
                        if _count == _end_count:
                            self._ELEMENT = elem
                            return
                # KeyError when there is no elem.attrib[value[0]] 
                except KeyError:
                    continue
            # If here, nothing got found, or the Nth (_count_end) match was not found
            self._ELEMENT = None
            return False
        
        """BEGIN"""
        # if isinstance(value, xml.etree.ElementTree.Element): # Doesnt work. I dont know why
        # Element passed in...just set
        if   str(type(value)) == "<type 'Element'>": return _passed_element(value) 
        # assumes first instance of elem.attrib[]'name'
        elif isinstance(value, str)                : return _passed_tuple( ('name', value) ) 
        # Finds (elem-attrib-name, elem-attrib-value, number of found instance)
        elif isinstance(value, tuple)              : return _passed_tuple(value)
        # Invalid input
        else:
            err = ''.join([err, "Value '", str(value), "' is not a valid object. ", "\n'value' must be a Name String, an ElementTree Element object, or a tupl containing a (attrib, value, instance) pair. "])
            raise ValueError(err)

    @element.deleter
    def element(self):
        self._ELEMENT = None
            
    """ PRIVATE METHODS ===================================================="""
        
    """ PUBLIC METHODS  ===================================================="""
    @classmethod
    def isXMLHandler(self, XML):
        # Try to load the file as xml
        if isinstance(XML, XMLHandler): 
            return XML
        
        else:
            # If source is not a valid xml file, this will error. 
            try:  
                return XMLHandler(source = XML) 
            
            except Exception as e:
                stack = inspect.stack()
                _class = stack[1][0].f_locals["self"].__class__            
                err = ''.join([_class, ".isXMLHandler:", "Parameter must be an XMLHandler object, or a full-path string to an XML file. (Value = '", str(XML), "'."])
                raise ValueError(err)

    def write(self, dest = None):
        """
        :NAME:
            write([dest = String])
            
        :PARAMETERS:
        
            dest = (OPTIONAL) The full file path to which the XML output will 
                   be written. If not supplied, the destination file will be 
                   the original source file (WARNING: THIS WILL OVERWRITE THE
                   SOURCE FILE!)
        """
        err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": " ])
        
        if dest is None: dest is self.source
        
        try:
            self.tree.write(dest, encoding='ISO-8859-1', xml_declaration=True)
        except Exception as e:
            msg = ''.join([err, "An unknown error occurred trying to export XML. (", str(e), ")."])
            log.error(msg)
            return False
        
        msg = ''.join(["Tree successfully exported to '", dest, "'. "])
        log.info(msg)
        return True

    def dump(self, _elem = None):
        """
        :NAME:
            
        :RETURNS:
            A list of cElementTree Elements.
        """
        if _elem is None:
            return self.root.getiterator()
        
        elif str(type(_elem)) == "<type 'Element'>":
            return _elem.getiterator()
        
        else:
            err = ''.join([self.__class__.__name__, ".", inspect.stack()[0][3], ": " ])
            err = ''.join([err, "Value passed in is not a valid cElement"])
            raise ValueError(err)
        
if __name__ == '__main__':
#     _xml = XMLHandler(source = '/Users/mikes/Documents/tmp/DeMIX.toppas')
#     _xml = XMLHandler(source = '/Users/mikes/Documents/tmp/FeatureFinderCentroided5.ini')
    _xml = XMLHandler(source = '/Users/mikes/Documents/tmp/Workflow.bpwf')

    _xml.element = 'bioproximity'
    print '_xml.element =', _xml.element.attrib
    
    for i in _xml.element.findall('*'): print i.attrib


#===============================================================================
#     _xml.element = _xml.element.find("*[@name='0']")
#     print '_xml.element =', _xml.element.attrib
# 
#     _xml.element = _xml.element.find("NODE[@name='parameters']")
#     print '_xml.element =', _xml.element.attrib
#===============================================================================
    # log.debug(str(xml), log_level = 10, screendump = True)
    # xml.write('/Users/mikes/Documents/tmp/TESTXMLOUTPUT.xml')
    #===========================================================================
#===============================================================================
#     import inspect
#     import time
#     from Bioproximity.common.openms_bridge import OpenMSBridge
#     OPENMS = OpenMSBridge()
#     
#     log.debug("Starting xmlhandler test...", 
#               logfile = 'syslog', 
#               screendump = True,
#               log_level = 10,              
#               )
#     xml = XMLHandler(source = "/Users/mikes/Documents/tmp/DeMix.top")
#     xml = XMLHandler(source = "/Users/mikes/Documents/tmp/DeMix.toppas")
# #     xml = XMLHandler(source = "nope")
#     print "xml.source:", xml.source
#     print "xml.tree:", xml.tree
#     print "xml.root:", xml.root
#     print "xml.elements:", xml.elements
#     print "xml.tree.getroot():", xml.tree.getroot
#     print inspect.getmembers(xml, predicate=inspect.ismethod)
# #     for i in [elem.attrib for elem in xml.root.iter()]: 
# #         print i  
#     #===========================================================================
#     # elem = xml.root.findall("NODE[@name='veices']")
#     # print 'elem=', elem    
#     #===========================================================================
#     elem = [elem.attrib['name'] for elem in xml.root.findall("NODE")]
#     print 'elem:', elem
#     time.sleep(.1)
#     exes = OPENMS.methods('installed')
#     print 'exes:', exes
#     print [i for e in elem for i in exes if e in i]        
# #     for elem in xml.root.iter():         
# #         try:
# #             if  ((elem.attrib['name'] == 'toppas_type') and (elem.attrib['value'] =="tool") ):
# #                 print; print '============' 
# #                 print elem
# #         except: pass
#===============================================================================

#===============================================================================
#     for elem in xml.root.findall("NODE[@name='0']"):
#         print '----'
#         print elem, ':', elem.attrib
# #         print "xml.root.findall(NODE[@name='vertices']).elem.attrib =", elem.attrib
# #         for i in elem: print i
#===============================================================================
        
    #===========================================================================
    # for node in xml.root:
    #     print node, node.attrib['name']
    # 
    # raw_input('Press enter...')
    #===========================================================================
    
#===============================================================================
#     for i in  xml.elements:
#         print 'i:', i
#         print "i.attrib:", i.attrib        
#         print "i.attrib['name']:", i.attrib['name']
#         print '------------------------------------'
# #     for parent in xml.tree.getiterator():
# #         for child in parent:
# #             print child.attrib['name']
#===============================================================================
     
    
        
        
    
 