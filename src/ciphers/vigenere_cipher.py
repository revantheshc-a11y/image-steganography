"""
Vigenère Cipher Implementation
A classical polyalphabetic substitution cipher.
"""

from typing import List


class VigenereCipher:
    """Vigenère Cipher implementation."""
    
    def __init__(self, key: str):
        """
        Initialize Vigenère Cipher with a key.
        
        Args:
            key: Encryption key (alphabetic characters only)
        """
        self.key = ''.join(c.upper() for c in key if c.isalpha())
        if not self.key:
            raise ValueError("Key must contain at least one alphabetic character")
        
        # Convert key to numbers
        self.key_numbers = [ord(c) - ord('A') for c in self.key]
    
    def _text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)."""
        return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]
    
    def _numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers to text."""
        return ''.join(chr(n + ord('A')) for n in numbers)
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Vigenère cipher.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Encrypted ciphertext
        """
        # Convert to uppercase and filter alphabetic characters
        text = ''.join(c.upper() for c in plaintext if c.isalpha())
        text_numbers = self._text_to_numbers(text)
        
        # Encrypt using key
        ciphertext_numbers = []
        for i, char_num in enumerate(text_numbers):
            key_index = i % len(self.key_numbers)
            encrypted_num = (char_num + self.key_numbers[key_index]) % 26
            ciphertext_numbers.append(encrypted_num)
        
        return self._numbers_to_text(ciphertext_numbers)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Vigenère cipher.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            Decrypted plaintext
        """
        # Convert to uppercase and filter alphabetic characters
        text = ''.join(c.upper() for c in ciphertext if c.isalpha())
        text_numbers = self._text_to_numbers(text)
        
        # Decrypt using key
        plaintext_numbers = []
        for i, char_num in enumerate(text_numbers):
            key_index = i % len(self.key_numbers)
            decrypted_num = (char_num - self.key_numbers[key_index]) % 26
            plaintext_numbers.append(decrypted_num)
        
        return self._numbers_to_text(plaintext_numbers)

