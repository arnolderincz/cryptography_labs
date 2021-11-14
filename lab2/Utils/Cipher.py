class Cipher:
  def __init__(self, generator = None, seed = None):
      self.offset = 0
      self.seed = seed
      self.generator = generator

  def get_offset(self):
    return self.offset

  def encrypt(self, plain_text, offset):
    message = bytes(plain_text, 'ascii')
    return self.algorithm(message, offset)
  
  def decrypt(self, cipher, offset):
    message = bytes(cipher)
    return self.algorithm(message, offset)

  def algorithm(self, message, offset):
    length = len(message)
    
    if offset != self.offset:
      self.offset = offset + length
      self.generator.reset_adjust(offset)
    else:
      self.offset += length
    
    random = self.generator.get(length)

    return bytes(int(rand) ^ char for (rand, char) in zip(random, list(message)))
 