"""
ReproTracker 
============

A module to update and store information about github traffic and views etc.
"""

import os
import time
import json
import requests

user = "ChristophKirst"

repos = ["ClearMap", "RepoTracker"]

infos = {'traffic/views' : 'timestamps',
         'traffic/clones' : 'timestamps',
         'traffic/popular/referrers' : 'records',
         'traffic/popular/paths' : 'records'}

url_template = "https://api.github.com/repos/%s/%s/%s"

#token = "256c0e26d188c27adf7ffc6798f3aa98d99035eb"

def get(user, repo, token, info="/traffic/clones", url_template=url_template):
  url = url_template % (user, repo, info);
  result = requests.get(url, headers={"Authorization":'token ' + token})
  return result.json();


def update(user, repo, token, info="/traffic/clones", method='timestamps', url_template=url_template, file=None):
  if file is None:
    file = "Data/%s_%s_%s.json" % (user, repo, info.replace('/', '_'));
    
  #read file
  try:
    with open(file, 'r') as f:
      data = json.load(f)
  except:
    data = {};
  
  #download 
  download = get(user, repo, token, info, url_template=url_template)
  
  #update
  if method =='timestamps':
    name = info.split('/')[-1];
    
    #update timestamps
    timestamps = {d['timestamp'] : d for d in data.get(name, [])};
    timestamps.update({d['timestamp'] : d for d in download.get(name, [])});
    timestamps = list(timestamps.values());
    data[name] = timestamps; 
                       
    #update counts / uniques
    counts = sum([d['count'] for d in timestamps])
    data['counts'] = counts
    
    uniques = sum([d['uniques'] for d in timestamps])
    data['uniques'] = uniques
 
  elif method == 'records':
    name = info.split('/')[-1][:-1]
    
    #add records to time series
    timestamp = time.strftime('%Y-%m-%dT%H:%M:%SZ');
    records = data.get('records', {});
    records[timestamp] = download;
    data['records'] = records;
    
    #update totals
    totals = {};
    for record in data['records'].values():
      for entry in record:
        source = entry[name];
        t = totals.get(source, {});
        t['count'] = t.get('count', 0) + entry.get('count', 0);
        t['uiniques'] = t.get('uiniques', 0) + entry.get('uiniques', 0);  
        totals[source] = t;
        
    data['totals'] = totals;
  
  print(data);
  
  #write file
  with open(file, 'w') as f:
    data = json.dump(data, f)



if __name__ == "__main__":
  import sys;
  token = sys.argv[1];
  
  for repo in repos:
    print('Accessing repository %s' % repo)
    for info, method in infos.items():
      print("   %s" % info)
      update(user, repo, token, info, method=method);

  
