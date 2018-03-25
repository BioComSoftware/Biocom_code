
# Twisted imports
from twisted.protocols.ftp import FTPClient, FTPFileListProtocol
from twisted.internet.protocol import Protocol, ClientCreator
from twisted.python import usage
from twisted.internet import reactor

# Standard library imports
from inspect import getmembers
from inspect import stack
from logger import check_logger

import string
import sys

try:
    from cStringIO import StringIO
except ImportError:
    from StringIO import StringIO

class BufferingProtocol(Protocol):
    # Code licensed from Twisted Matrix Laboratories.
    # See LICENSE for details.
    """Simple utility class that holds all data written to it in a buffer."""
    def __init__(self):
        self.buffer = StringIO()

    def dataReceived(self, data):
        self.buffer.write(data)

class FTPclient(object):
    def __init__(self, host, port, directory, 
                 username, password, 
                 log, error, 
                 debug = 0, passive = 0):
        try:
            self.log = check_logger(log)
        except Exception, e:
            self.log = create_logger(app_name = "FTPclient", 
                                     log_level = 40, 
                                     screen = False)
        self.log.debug("Starting FTPclient __init__ ...")
        self.host = host
        self.log.debug('host: ' + str(host))
        self.port = port
        self.log.debug('port: ' + str(port))
        self.directory = directory
        self.log.debug('directory: ' + str(directory))
        self.username = username
        self.log.debug('username: ' + str(username))  
        self.password = password
        self.log.debug('password: ' + str(password))
        self.error = error
        self.log.debug('error: ' + str(error))
        self.debug = debug
        self.log.debug('debug: ' + str(debug))
        self.passive = passive 
        self.log.debug('passive: ' + str(passive))

    def success(self, response):
        self.log.debug("".join(['Success!  Got response: ', 
                                str(response), '\n' ]))

    def fail(self, error):
        self.log.debug("".join(['Error:', str(error), '\n' ]))
    
    def showFiles(self, result, fileListProtocol):
        print 'Processed file listing:'
        for file in fileListProtocol.files:
            print '    %s: %d bytes, %s' \
                  % (file['filename'], file['size'], file['date'])
        print 'Total: %d files' % (len(fileListProtocol.files))
    
    def showBuffer(self, result, bufferProtocol):
        print 'Got data:'
        print bufferProtocol.buffer.getvalue()

    def run(self):
        # Create the client
        FTPClient.debug = self.debug
        self.creator = ClientCreator(reactor, 
                                     FTPClient, 
                                     self.username,
                                     self.password, 
                                     passive=self.passive
                                )

        self.creator.connectTCP(
            self.host, 
            self.port
            ).addCallback(self.connectionMade).addErrback(self.connectionFailed)
#             ).addCallback(self.connectionMade).addErrback(self.connectionFailed)

        reactor.run()
                
    def connectionFailed(self, f):
        print "Connection Failed:", f
        reactor.stop()

    def showcwd(self):
        pass
    
    def connectionMade(self, ftpClient):
        self.ftpClient = ftpClient
        
    def showfiles(self):
        # Get the current working directory
        self.ftpClient.pwd().addCallbacks(self.success, self.fail)
    
        # Get a detailed listing of the current directory
        fileList = FTPFileListProtocol()
        d = self.ftpClient.list('.', fileList)
        d.addCallbacks(self.showFiles, self.fail, callbackArgs=(fileList,))
    
        # Change to the parent directory
        self.ftpClient.cdup().addCallbacks(self.success, self.fail)
        
        # Create a buffer
        proto = BufferingProtocol()
    
        # Get short listing of current directory, and quit when done
        d = self.ftpClient.nlst('.', proto)
        d.addCallbacks(self.showBuffer, self.fail, callbackArgs=(proto,))
#         d.addCallback(lambda result: reactor.stop())

#         # Get the current working directory
#         ftpClient.pwd().addCallbacks(self.success, self.fail)
#     
#         # Get a detailed listing of the current directory
#         fileList = FTPFileListProtocol()
#         d = ftpClient.list('.', fileList)
#         d.addCallbacks(self.showFiles, self.fail, callbackArgs=(fileList,))
#     
#         # Change to the parent directory
#         ftpClient.cdup().addCallbacks(self.success, self.fail)
#         
#         # Create a buffer
#         proto = BufferingProtocol()
#     
#         # Get short listing of current directory, and quit when done
#         d = ftpClient.nlst('.', proto)
#         d.addCallbacks(self.showBuffer, self.fail, callbackArgs=(proto,))
# #         d.addCallback(lambda result: reactor.stop())


# this only runs if the module was *not* imported
if __name__ == '__main__':
    from logger import create_logger
    import errorhandler
 
    log = create_logger('SECscraper', 
                         log_level = 10) 

#     error = errorhandler.error(None)    

    o = FTPclient(
                  host = "ftp.sec.gov", 
                  port = 21, 
                  directory = '/edgar/daily-index/2009', 
                  username = 'anonymous', 
                  password = '', 
                  log = log, 
                error = None
                  )
    o.run()
    o.showfiles()
