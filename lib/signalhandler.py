import signal

def set_signal_handler(self):
    self.log.debug("Parsing signal handlers...")
    for i in [x for x in dir(signal) if x.startswith("SIG")]:
      try:
        signum = getattr(signal,i)
        signal.signal(signum,self._signal_handler)
      except Exception, e:
        self.log.debug("Skipping " + str(i) + " in set_signal_handler")