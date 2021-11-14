class Solitaire:
  def deck_check(self, deck):
    if len(deck) != 54:
      raise ValueError('Invalid deck')
    
    for i in range(1, 55):
      if i not in deck:
        ValueError('Invalid deck')

  def __init__(self, deck = []):
    self.deck_check(deck)

    self.initial_deck = deck.copy()
    self.deck = deck.copy()
    self.jocker_1 = deck.index(53)
    self.jocker_2 = deck.index(54)
  
  def move_jocker(self, jocker_val, jocker,  steps):
    self.deck.pop(jocker_val)
    if jocker_val < (53 - steps):
      self.deck.insert(jocker_val + steps, jocker)
    else:
      steps += 1
      self.deck.insert((jocker_val + steps) % 54, jocker)
      jocker_val = (jocker_val + steps) % 54

    return jocker_val

  def move_jockers_down(self):
    self.jocker_1 = self.move_jocker(self.jocker_1, 53, 1)
    self.jocker_2 = self.deck.index(54)
    self.jocker_2 = self.move_jocker(self.jocker_2, 54, 2)

  def swap(self):
    first = min(self.jocker_1, self.jocker_2)
    second = max(self.jocker_1, self.jocker_2) + 1

    self.deck = self.deck[second:] + self.deck[first:second] + self.deck[:first]

    self.jocker_1 = self.deck.index(53)
    self.jocker_2 = self.deck.index(54)

  def swap_top(self):
    last = self.deck[-1] + 1

    if last < 53:
      self.deck = self.deck[last: -1] + self.deck[:last]
      self.deck.append(last - 1)
      self.jocker_1 = self.deck.index(53)
      self.jocker_2 = self.deck.index(54)

  def get(self, end):
    if end <= 0:
      return []

    random = []

    for i in range(end):
      byte = []
      j = 0
      while j < 8:
        self.move_jockers_down()
        self.swap()
        self.swap_top()

        top_card = self.deck[0]
        if top_card < 53:
          byte.append(top_card % 2)
          j += 1

      str_byte = ''.join(map(str, byte))
      random.append(int(str_byte, 2))

    return random

  def reset_adjust(self, start):
    self.deck = self.initial_deck.copy()
    self.jocker_1 = self.deck.index(53)
    self.jocker_2 = self.deck.index(54)
    
    for i in range(start):
      j = 0
      while j < 8:
        self.move_jockers_down()
        self.swap()
        self.swap_top()

        top_card = self.deck[0]
        if top_card < 53:
          j += 1
