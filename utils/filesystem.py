import os
import csv
import networkx as nx


def add_to_csv(path, data):
  if os.path.exists(path):
      with open(path, 'a', newline='') as f:
          w = csv.DictWriter(f, data.keys())
          w.writerow(data)
  else:
      with open(path, 'w', newline='') as f:
          w = csv.DictWriter(f, data.keys())
          w.writeheader()
          w.writerow(data)

def read_graph(path):
  with open(path, 'r') as f:
    data = nx.readwrite.edgelist.read_edgelist(f)
  return data