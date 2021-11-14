class BlumBlumShub:
  def __init__(self, seed):
    self.p = 7043
    self.q = 4271
    self.seed = seed
    self.N = self.p * self.q
    self.current = (seed ** 2) % self.N

  def get(self, length):
    if(length <= 0):
      return []

    random = []

    for i in range(length):
      byte = []
      for j  in range(8):
        byte.append(self.current % 2)
        self.current = (self.current ** 2) % self.N

      str_byte = ''.join(map(str, byte))
      random.append(int(str_byte, 2))

    return random

  def reset_adjust(self, start):
    self.current = (self.seed ** 2) % self.N
    
    for i in range(start):
      byte = []
      for j  in range(8):
        byte.append(self.current % 2)
        self.current = (self.current ** 2) % self.N

