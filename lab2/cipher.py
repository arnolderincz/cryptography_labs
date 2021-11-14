class Cipher:
  def __init__(self, generator = None, seed = None):
      self.offset = 0
      self.seed = seed
      self.generator = generator(seed)

  def get_offset(self):
    return self.offset

  def encrypt(self, plain_text):
    message = bytes(plain_text, 'ascii')
    length = len(message)
    self.offset += length

    random = self.generator.get(length)

    return bytes(random ^ char for char in list(message))

  def decrypt(self, message, offset):
    message = bytes(message)
    length = len(message)
    self.offset += length

    random = self.generator.get(length)

    if offset != self.offset:
      random = self.generator.getInterval(offset, offset + length)

    return bytes(rand ^ char for (rand, char) in zip(random, list(message)))
 