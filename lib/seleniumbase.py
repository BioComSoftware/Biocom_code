class SeleniumBase(object):
    def __init__(self,
                 driver = 'Firefox',
                 driver_path = "C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
                 cookie_url = None,   
                 log_level = 10, 
                 logfile = None
                 ):
        try:
            # Run cleanup at script end
            atexit.register(self._cleanup)
    
            # Run cleanup at any kill signal
            set_signal_handler(self)
            
            # Load the browser driver
            load_selenium_driver(self, driver, driver_path)
            
            # Try to get cookies
            self.cookie_url = cookie_url
            if self.cookie_url is not None:
                try:
                    self.driver.get(self.cookie_url)
                    if os.path.isfile('.sessioncookies.pkl'):
                        cookies = pickle.load(open(".sessioncookies.pkl", "rb"))
                        for cookie in cookies:
                            self.driver.add_cookie(cookie)
                except Exception, e:
                    self.lasterr = self.error.handle(e,inspect.getmembers(self),inspect.stack())

        except Exception, e:
            self.lasterr = self.error.handle(e,inspect.getmembers(self),inspect.stack())
            sys.exit(1)        

    def _cleanup_selenium(self):
        """
        _cleanup()
            Cleans up the files and closes the driver. 
        """
        try:
            self.driver .get(self.cookie_url)
            self.log.info("Saving session cookies...")
            pickle.dump(self.driver.get_cookies() , open(".sessioncookies.pkl","wb"))            
            self.log.info("Done.")
            
            self.log.info("Closing WebDriver...")
            self.driver.close()
            self.log.debug("'driver.stop_client()' on WebDriver...")
            self.driver.stop_client()
            self.log.debug("'driver.quit()' on WebDriver...")
            self.driver.quit()
            self.log.info("Done.")

        except Exception, e:
            self.lasterr = self.error.handle(e,inspect.getmembers(self),inspect.stack())
