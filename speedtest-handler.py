import speedtest
import json
from pymongo import MongoClient
from urllib import request


def run_speedtest():
  servers = []
  s = speedtest.Speedtest()
  s.get_servers(servers)
  s.get_best_server()
  s.download()
  s.upload(pre_allocate=False)
  s.results.share()

  return s.results.dict()

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

def write_to_database(formatted_speed_results):
  client = MongoClient('localhost', 27017)
  db = client['speedtest']
  collection = db['2018_speedtests']
  posts = db.posts
  post_id = posts.insert_one(formatted_speed_results).inserted_id
  print(post_id)


if __name__ == '__main__':
  formatted_speed_results = process_speedtest_data( run_speedtest() ) 
  write_to_database(formatted_speed_results)
""" def test_process_data():
  test_answer = {'upload': 103.76, 'download': 100.74, 'ping': 13, 'timestamp': '2018-09-13T17:00:11.626171Z'}
  with open('./results.json') as f:
    data = json.load(f)
  print (str(process_speedtest_data(data)) + '\n' + str(test_answer))
  assert set(process_speedtest_data(data)) == set(test_answer) """