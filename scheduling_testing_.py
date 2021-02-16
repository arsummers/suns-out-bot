import schedule
import time


def schedule_tester():
  print('THIS MESSAGE IS SCHEDULED')

def schedule_weather_trigger():
  # should be used to call check_weather on a schedule, so I won't have to rely on the next day forecast. It should call check_weather at 11 AM, then call send_message right after if the weather is satisfactory

  # will need to use at(time_str) method to get this to trigger at the same time each day

  # will need to use class schedule.Job(interval, schedule-None)
  pass

schedule.every(10).seconds.do(schedule_tester)

while True:
    schedule.run_pending()
    time.sleep(1)
  

# schedule_weather_trigger()
