from Generators.BlumBlumShub import BlumBlumShub
from Generators.Solitaire import Solitaire

class Config:
  def __init__(self):
    self.generator = None
    self.key = None
    with open('./configS.txt') as file:
      type = file.readline().strip()

      if type == 'solitaire':
        line = file.readline().strip()
        deck = line.split()
        self.key = [int(i) for i in deck]
        
        self.generator = Solitaire(self.key)
      elif type == 'bbs':
        line = file.readline().strip()
        seed = int(line.split()[0])
        self.key = seed

        self.generator = BlumBlumShub(seed)

  def get_generator(self):
    return self.generator

  def get_key(self):
    return self.key
