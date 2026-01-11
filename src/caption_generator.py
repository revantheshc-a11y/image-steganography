"""
Caption Generator Module
Generates captions from labels and learns from user input over time.
"""

import json
import os
from typing import List, Set
from pathlib import Path


class CaptionGenerator:
    """Generates captions from labels with learning capability."""
    
    def __init__(self, dictionary_file: str = "data/caption_dictionary.json"):
        """
        Initialize caption generator.
        
        Args:
            dictionary_file: Path to JSON file storing learned labels
        """
        self.dictionary_file = dictionary_file
        self.dictionary: Set[str] = set()
        self._load_dictionary()
    
    def _load_dictionary(self):
        """Load dictionary from file if it exists."""
        if os.path.exists(self.dictionary_file):
            try:
                with open(self.dictionary_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.dictionary = set(data.get('labels', []))
            except (json.JSONDecodeError, IOError):
                self.dictionary = set()
        else:
            # Create directory if it doesn't exist
            os.makedirs(os.path.dirname(self.dictionary_file), exist_ok=True)
            self.dictionary = set()
    
    def _save_dictionary(self):
        """Save dictionary to file."""
        os.makedirs(os.path.dirname(self.dictionary_file), exist_ok=True)
        with open(self.dictionary_file, 'w', encoding='utf-8') as f:
            json.dump({'labels': sorted(list(self.dictionary))}, f, indent=2)
    
    def add_labels(self, labels: List[str]):
        """
        Add new labels to the dictionary.
        
        Args:
            labels: List of label strings to add
        """
        for label in labels:
            if label.strip():
                self.dictionary.add(label.strip().lower())
        self._save_dictionary()
    
    def generate_caption(self, labels: List[str]) -> str:
        """
        Generate a caption from given labels.
        
        Args:
            labels: List of labels to include in caption
            
        Returns:
            Generated caption string
        """
        if not labels:
            return "No labels provided"
        
        # Clean and validate labels
        clean_labels = [label.strip() for label in labels if label.strip()]
        
        if not clean_labels:
            return "No valid labels provided"
        
        # Generate simple caption: "A [label1], [label2], and [label3]"
        if len(clean_labels) == 1:
            caption = f"A {clean_labels[0]}"
        elif len(clean_labels) == 2:
            caption = f"A {clean_labels[0]} and {clean_labels[1]}"
        else:
            caption = f"A {', '.join(clean_labels[:-1])}, and {clean_labels[-1]}"
        
        # Add labels to dictionary for future use
        self.add_labels(clean_labels)
        
        return caption
    
    def get_suggestions(self, prefix: str = "") -> List[str]:
        """
        Get suggested labels from dictionary.
        
        Args:
            prefix: Optional prefix to filter suggestions
            
        Returns:
            List of suggested labels
        """
        suggestions = sorted(list(self.dictionary))
        if prefix:
            prefix_lower = prefix.lower()
            suggestions = [s for s in suggestions if s.startswith(prefix_lower)]
        return suggestions[:10]  # Return top 10 suggestions

