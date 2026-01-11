"""
Hill Cipher Implementation
A classical cipher that uses matrix multiplication for encryption/decryption.
"""

import numpy as np
from typing import List, Tuple


class HillCipher:
    """Hill Cipher implementation using matrix multiplication."""
    
    def __init__(self, key_matrix: List[List[int]]):
        """
        Initialize Hill Cipher with a key matrix.
        
        Args:
            key_matrix: 2x2 or 3x3 matrix of integers (mod 26)
        """
        self.key_matrix = np.array(key_matrix, dtype=int)
        self.n = len(key_matrix)
        
        # Validate key matrix
        if self.n not in [2, 3]:
            raise ValueError("Key matrix must be 2x2 or 3x3")
        
        # Check if key matrix is invertible (mod 26)
        det = int(np.round(np.linalg.det(self.key_matrix))) % 26
        if det == 0 or np.gcd(det, 26) != 1:
            raise ValueError("Key matrix must be invertible modulo 26")
        
        # Calculate inverse matrix
        self.inverse_key = self._mod_inverse_matrix(self.key_matrix)
    
    def _mod_inverse_matrix(self, matrix: np.ndarray) -> np.ndarray:
        """Calculate the modular inverse of the key matrix."""
        det = int(np.round(np.linalg.det(matrix))) % 26
        
        # Find modular inverse of determinant
        det_inv = self._mod_inverse(det, 26)
        
        # Calculate adjugate matrix
        if self.n == 2:
            adj = np.array([[matrix[1, 1], -matrix[0, 1]],
                           [-matrix[1, 0], matrix[0, 0]]])
        else:  # n == 3
            adj = np.round(np.linalg.inv(matrix) * np.linalg.det(matrix))
        
        # Multiply by determinant inverse and mod 26
        inverse = (det_inv * adj) % 26
        return inverse.astype(int)
    
    def _mod_inverse(self, a: int, m: int) -> int:
        """Calculate modular inverse using extended Euclidean algorithm."""
        a = a % m
        for x in range(1, m):
            if (a * x) % m == 1:
                return x
        raise ValueError("Modular inverse does not exist")
    
    def _text_to_numbers(self, text: str) -> List[int]:
        """Convert text to numbers (A=0, B=1, ..., Z=25)."""
        return [ord(c.upper()) - ord('A') for c in text if c.isalpha()]
    
    def _numbers_to_text(self, numbers: List[int]) -> str:
        """Convert numbers to text."""
        return ''.join(chr(n + ord('A')) for n in numbers)
    
    def _pad_text(self, text: str) -> str:
        """Pad text to be multiple of n."""
        # Remove non-alphabetic characters and convert to uppercase
        text = ''.join(c.upper() for c in text if c.isalpha())
        
        # Pad with 'X' if necessary
        remainder = len(text) % self.n
        if remainder != 0:
            text += 'X' * (self.n - remainder)
        
        return text
    
    def encrypt(self, plaintext: str) -> str:
        """
        Encrypt plaintext using Hill cipher.
        
        Args:
            plaintext: Text to encrypt
            
        Returns:
            Encrypted ciphertext
        """
        # Pad and convert to numbers
        padded_text = self._pad_text(plaintext)
        numbers = self._text_to_numbers(padded_text)
        
        # Encrypt in blocks
        ciphertext_numbers = []
        for i in range(0, len(numbers), self.n):
            block = np.array(numbers[i:i+self.n])
            encrypted_block = (self.key_matrix @ block) % 26
            ciphertext_numbers.extend(encrypted_block.tolist())
        
        return self._numbers_to_text(ciphertext_numbers)
    
    def decrypt(self, ciphertext: str) -> str:
        """
        Decrypt ciphertext using Hill cipher.
        
        Args:
            ciphertext: Text to decrypt
            
        Returns:
            Decrypted plaintext
        """
        # Convert to numbers
        numbers = self._text_to_numbers(ciphertext)
        
        # Decrypt in blocks
        plaintext_numbers = []
        for i in range(0, len(numbers), self.n):
            block = np.array(numbers[i:i+self.n])
            decrypted_block = (self.inverse_key @ block) % 26
            plaintext_numbers.extend(decrypted_block.tolist())
        
        return self._numbers_to_text(plaintext_numbers)

