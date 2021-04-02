# this is the older function scheduler that works when it runs locally, but prevents the flask app from starting up while it's running. preserved here so that I can get back to it if other options fail even more.



  def schedule_weather_trigger(self):
        """
        Set to run in the background. Sleeps for a day, calls send_weather_message, which checks the weather and sends a message. 

        Trying to rewrite with APScheduler
        """

        #left in for testing that deployed version will loop
        schedule.every(10).seconds.do(self.send_weather_message) 

        #schedule.every().day.at("11:59").do(self.send_weather_message) #commented out for testing
        while True:
            schedule.run_pending()
            #time.sleep(86399) #sleeps for a day minus a second, then runs. Cuts down on unnecessary up time
            time.sleep(1) # for testing
