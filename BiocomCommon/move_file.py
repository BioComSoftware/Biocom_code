##############################################################################
# Removal of the "__license__" line or content from  "__license__", or removal 
# of "__author__" in this or any constituent # component or file constitutes a 
# violation of the licensing and copyright agreement. 
__author__      = "Mike Rightmire"
__copyright__   = "BioCom Software"
__license__     = "Telemend"
__license_file__= "Clause1.PERPETUAL_AND_UNLIMITED_LICENSING_TO_THE_CLIENT.py"
__version__     = "0.9.0.0"
__maintainer__  = "Mike Rightmire"
__email__       = "Mike.Rightmire@BiocomSoftware.com"
__status__      = "Development"
##############################################################################

from datetime import datetime
from BiocomCommon.loghandler import log

import os
import shutil
""""""
# === PRIVATE FUNCTIONS ======================================================
def _move_file(src, dst):
    """"""
    try:
        result = shutil.move(src, dst)
        return True

    except Exception as e:
        return e

def _rename_file(src, dst):
    """"""
    try:
        shutil.move(src, dst)
        return True

    except Exception as e:
        return e

def _check_dir_exists(dst_dir):
    """"""
    try:
        os.stat(dst_dir)
        return True

    except Exception as e:
        msg = ''.join(["The directory '", str(dst_dir),
                       "' does not exist. ", "Creating."])
        log.debug(msg)

        try:
            os.mkdir(dst_dir)
        except Exception as e:
            return e

        return True

    return False

""""""
# === PUBLIC FUNCTIONS ======================================================
def move_file(src_dir, dst_dir, filename):
    """"""
    # ============================================
    # Check if directory exists. If not, create it
    if not _check_dir_exists(dst_dir):
        err = "Cannot use or create directory '" + str(dst_dir) + "'."
        raise IOError(err) # Fatal

    # ==================================================================
    # Rename in place first, to prevent file being picked up redundantly
    newfilename = filename +"." + str(datetime.now().microsecond)
    src  = src_dir + "/" + filename
    dst  = src_dir + "/" + newfilename
    result = _rename_file(src, dst)
    if result is not True: # Must specifically check for True
        err = ''.join(["Cannot rename '", src, "'. (", str(result), ")."])
        raise IOError(err) # Fatal

    #=========================================================
    # If the renaming works, then move to the .error directory
    src = dst # To grab time-dependent name change
    dst = dst_dir + "/" + newfilename # Safety slash

    msg = ''.join(["common.move_util: Moving file '", src, "' to '", dst, "'. "])
    log.debug(msg)

    result = _move_file(src, dst)
    if result is not True: # Must specifically check for True
        err = ''.join(["Cannot move '", str(src), "' to '", str(dst),"'."])
        raise IOError(err)
