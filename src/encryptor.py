import random
import csv
from src.encryption_schemes import ENCRYPTION_SCHEMES

class Encryptor:
    def __init__(self, schemes, seed):
        """
        Initializes the Encryptor with a set of encryption schemes and a fixed seed.
        """
        self.schemes = schemes
        self.seed = seed
        random.seed(self.seed)

    def encrypt(self, plaintext):
        ciphertext = []
        scheme_names = list(self.schemes.keys())

        for char in plaintext:
            # Randomly select a scheme
            scheme_name = random.choice(scheme_names)
            scheme_func = self.schemes[scheme_name]

            # Encrypt the character
            encrypted_char = scheme_func(char)

            # Append to results
            ciphertext.append(str(encrypted_char))

        
        complete_ciphertext = "".join(ciphertext)
        return(complete_ciphertext)