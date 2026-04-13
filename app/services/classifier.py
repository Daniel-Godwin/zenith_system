import json
import os
import re

class SmartClassifier:
    """
    The Brain: Dynamically loads knowledge from JSON to classify files.
    """
    def __init__(self):
        # Dynamically find the path to the JSON file
        base_dir = os.path.dirname(os.path.dirname(__file__)) # Goes up to /app
        config_path = os.path.join(base_dir, "core", "knowledge.json")
        
        try:
            with open(config_path, 'r') as f:
                self.knowledge_base = json.load(f)
        except FileNotFoundError:
            print(f"Warning: Knowledge base not found at {config_path}. Using empty brain.")
            self.knowledge_base = {}

    def predict(self, text: str) -> str:
        """
        Improved Brain: Finds keywords even when they are part of 
        longer filenames (like 'ucimlrepo' matching 'repo').
        """
        text = text.lower()
        
        for category, keywords in self.knowledge_base.items():
            for word in keywords:
                # Fuzzy match: checks if the keyword exists anywhere in the filename
                if word.lower() in text:
                    return category
        
        return "Unclassified"