from Utils.Config import Config
from Utils.Cipher import Cipher

config = Config()
cipher = Cipher(config.get_generator(), config.get_key())

encrypted = cipher.encrypt('This is really nice', 0)
print("Encrypted {}", encrypted)
print('Decrypted {}', cipher.decrypt(encrypted, cipher.get_offset()- len(encrypted)))
