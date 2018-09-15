
from platform   import system as system_name  # Returns the system/OS name
from subprocess import call   as system_call  # Execute a shell command
def ping(host='8.8.8.8'):
    """
    Returns True if host (str) responds to a ping request.
    Remember that a host may not respond to a ping (ICMP) request even if the host name is valid.
    """

    # Ping command count option as function of OS
    param = '-n' if system_name().lower()=='windows' else '-c'

    # Building the command. Ex: "ping -c 1 google.com"
    command = ['ping', param, '1', host]

    # Pinging
    return system_call(command) == 0

import speedtest
def run_speedtest():
  servers = []
  s = speedtest.Speedtest()
  s.get_servers(servers)
  s.get_best_server()
  s.download()
  s.upload(pre_allocate=False)
  s.results.share()

  return s.results.dict()

from urllib import request
def process_speedtest_data(speed_results):
  # Formatting for the db entry
  entry = {}
  entry['upload'] = round((speed_results['upload'] / 1000000), 2)
  entry['download'] = round((speed_results['download'] / 1000000), 2)
  entry['ping'] = int(round(speed_results['ping'], 0))
  entry['_id'] = speed_results['timestamp']
  
  # Saves the image to the file directory
  request.urlretrieve(speed_results['share'], "./images/" + speed_results['timestamp'] + ".png")
  
  # returns formatted entry
  return entry

from pymongo import MongoClient
from datetime import datetime
def write_to_database(formatted_speed_results):
  client = MongoClient("mongodb://localhost:27017/")
  db = client["speedtest"]
  collection = db["2018_speedtests"]
  post_id = collection.insert_one(formatted_speed_results)
  print (post_id)


if __name__ == '__main__':
  if (ping()):
    print("Passed generic connection test.\nStarting SpeedTest")
    
    #Run the speed test and process the output
    test_results = process_speedtest_data(run_speedtest())
    print("Writing to database")
    
    # Output results to database
    write_to_database(test_results)
    print("Finished")
  
  else:
    # Else write not connected to internet
    write_to_database(
      {'upload': 0, 'download': 0, 'ping': 0, '_id': str(datetime.utcnow()) + "Z"}
    )
  
""" def test_process_data():
  test_answer = {'upload': 103.76, 'download': 100.74, 'ping': 13, 'timestamp': '2018-09-13T17:00:11.626171Z'}
  with open('./results.json') as f:
    data = json.load(f)
  print (str(process_speedtest_data(data)) + '\n' + str(test_answer))
  assert set(process_speedtest_data(data)) == set(test_answer) """