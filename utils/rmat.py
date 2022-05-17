from pathlib import Path
import numpy as np
import multiprocessing as mp
import networkit as nk

from utils.filesystem import add_to_csv

lock = mp.Lock()

def rmat_to_file(N, E, a, b, c, d, dataset_folder, s):
  scale = np.ceil(np.log2(N))
  factor = E/N
  reduce = np.power(2, scale) - N

  Graph = nk.generators.RmatGenerator(scale, factor, a, b, c, d, weighted = True, reduceNodes = reduce).generate()
  Graph = nk.graph.Graph(Graph, False, False) # To undirected and unweigted
  Graph.removeSelfLoops()
  Graph = nk.components.ConnectedComponents(Graph).extractLargestConnectedComponent(Graph, compactGraph = True)
  out_filename = Path(dataset_folder,'graphs','RMAT_{}.txt'.format(s))
  print("Wrinting to:" + str(out_filename))
  nk.writeGraph(Graph, str(out_filename), nk.Format.EdgeListTabOne)
  with lock:
    add_to_csv(Path(dataset_folder,"dataset_description.csv"), {
      'N': N, 'E':E, 'a': a, 'b': b, 'c': c, 'd': d, 'name': out_filename, 'scale': scale, 'factor': factor, 'reduce': reduce
    })
  return s