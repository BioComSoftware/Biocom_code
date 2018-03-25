

from twisted.internet.protocol import Protocol, ClientCreator

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

class LineTextBuffer(object):
    def __init__(self):
        self.linelist = []
 
    def write(self, data):
        lines = StringIO(data)
        for line in lines.readlines():
            self.linelist.append(line)
    
    def readline(self):
        return self.linelist.pop(0)
    
    def readlines(self):
        loop = True
        while loop:
            try:
                line = self.linelist.pop(0)
                yield line
        
            except IndexError, e:
                loop =False

    def clear(self):
        self.linelist = []