from Generators.Solitaire import Solitaire


class Config:
  def __init__(self):
    self.generator = None
    self.key = None
    with open('./config.txt') as file:
      type = file.readline().strip()

      if type == 'solitaire':
        line = file.readline().strip()
        deck = line.split()
        self.key = [int(i) for i in deck]
        
        self.generator = Solitaire(self.key)

  def get_generator(self):
    return self.generator

  def get_key(self):
    return self.key
