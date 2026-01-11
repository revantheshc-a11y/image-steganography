"""
Classical Cipher Engine
Combines Hill and Vigenère ciphers in a two-stage pipeline.
"""

from typing import List
from .ciphers.hill_cipher import HillCipher
from .ciphers.vigenere_cipher import VigenereCipher


class CipherEngine:
    """Two-stage cipher engine using Hill and Vigenère ciphers."""
    
    def __init__(self, hill_key: List[List[int]], vigenere_key: str):
        """
        Initialize cipher engine with keys for both ciphers.
        
        Args:
            hill_key: 2x2 or 3x3 matrix for Hill cipher
            vigenere_key: String key for Vigenère cipher
        """
        self.hill_cipher = HillCipher(hill_key)
        self.vigenere_cipher = VigenereCipher(vigenere_key)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using two-stage pipeline: Hill -> Vigenère.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Encrypted ciphertext
        """
        # Stage 1: Hill cipher
        hill_encrypted = self.hill_cipher.encrypt(plaintext)
        
        # Stage 2: Vigenère cipher
        final_encrypted = self.vigenere_cipher.encrypt(hill_encrypted)
        
        return final_encrypted
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using reverse pipeline: Vigenère -> Hill.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            Decrypted plaintext
        """
        # Stage 1: Vigenère decryption
        vigenere_decrypted = self.vigenere_cipher.decrypt(ciphertext)
        
        # Stage 2: Hill decryption
        final_decrypted = self.hill_cipher.decrypt(vigenere_decrypted)
        
        return final_decrypted

