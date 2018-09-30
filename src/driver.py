import json
from ctypes import cdll, c_float

def get_handler(source):
  if not source:
    source = 'default' #super dumb way to make sure the code i wrote works
  lib = cdll.LoadLibrary("./build/" + source + ".dylib")
  lib.init()
  lib.tick.restype = c_float
  def handler(inval):
    if inval > 1.0:
      inval = 1.0
    if inval < -1.0:
      inval = -1.0
    return lib.tick(c_float(inval))
  return handler

# todo: make it so that it sums over all sources
def propagate(nodes, value):
  for node in nodes:
    node.tick(value)

class Node:
  def __init__(self, handler):
    self.handler = handler
    self.output = 0.0

  def tick(self, inval):
    outval = self.handler(inval)
    self.outval = outval
    return outval

class NonTerminalNode(Node):
  def set_children(self, children):
    self.children = children

  def tick(self, outval):
    nextVal = super().tick(outval)
    propagate(self.children, nextVal)

class SourceNode(NonTerminalNode):
  def tick(self):
    super().tick(0.0)

class IntermediateNode(NonTerminalNode):
  pass

class SinkNode(Node):
  def __init__(self):
    super().__init__(get_handler('default'))

class Network:
  def __init__(self, nodelist):
    self.sources = []
    self.sinks = []
    self.nodes = {}

    for node in nodelist:
      node_type = node['type']
      if node_type == 'source':
        handler = get_handler(node['definition'])
        new_node = SourceNode(handler)
        self.sources.append(new_node)
      elif node_type == 'node':
        handler = get_handler(node['definition'])
        new_node = IntermediateNode(handler)
      elif node_type == 'sink':
        new_node = SinkNode()
        self.sinks.append(new_node)
      else:
        raise Exception("unrecognized node type: ", node_type)
      self.nodes[node['id']] = new_node

    for node in nodelist:
      if node['type'] != 'sink':
        node_children = [ self.nodes[id] for id in node['outputs'] ]
        self.nodes[node['id']].set_children(node_children)

  def tick(self):
    for source in self.sources:
      source.tick()

def load_nodelist(fname):
  json_data = open(fname)
  nodelist = json.load(json_data)
  json_data.close()
  return nodelist

def make_network():
  return Network(load_nodelist('./data/sample.json'))

network = make_network()
network.tick()
print(network.sinks[0].outval)

