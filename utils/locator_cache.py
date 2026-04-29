# utils/locator_cache.py

import os
import json
from typing import List, Dict, Optional

class LocatorCache:
    """
    A cache class to store and retrieve healed locators.
    Implements the Single Responsibility Principle by handling only caching logic.
    """
    
    def __init__(self):
        """Initialize the cache with the correct file path."""
        # Get the directory where this file is located
        base_dir = os.path.dirname(os.path.abspath(__file__))
        # Set the path to the cache file in __pycache__ directory
        self.cache_path = os.path.join(base_dir, "__pycache__", "healed-locator.json")
        # Initialize an empty cache list
        self._cache: List[Dict[str, str]] = []
        # Print the resolved path for verification
        print(f"Resolved Cache Path: {self.cache_path}")
    
    def load_from_file(self) -> None:
        """Load cached locators from the JSON file if it exists."""
        if os.path.exists(self.cache_path):
            try:
                with open(self.cache_path, 'r') as file:
                    self._cache = json.loads(file.read())
                print(f"Cache loaded successfully. {len(self._cache)} entries found.")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Failed to load cache file. {str(e)}")
                self._cache = []
    
    def save_cache_to_file(self) -> None:
        """Save the current cache to the JSON file."""
        try:
            # Ensure the directory exists
            os.makedirs(os.path.dirname(self.cache_path), exist_ok=True)
            with open(self.cache_path, 'w') as file:
                json.dump(self._cache, file, indent=4)
            print(f"Cache saved successfully to {self.cache_path}")
        except IOError as e:
            print(f"Error: Failed to save cache file. {str(e)}")
    
    def save_healed_locator(self, original_locator: str, new_strategy_dict: Dict[str, str]) -> None:
        """
        Save or update a healed locator in the cache.
        
        Args:
            original_locator: The original locator that failed
            new_strategy_dict: Dictionary containing the new locator strategies
        """
        # Check if the original locator already exists in the cache
        existing_entry = next(
            (item for item in self._cache if item.get("original") == original_locator),
            None
        )
        
        if existing_entry:
            # Update the existing entry
            existing_entry.update(new_strategy_dict)
            print(f"Updated existing cache entry for: {original_locator}")
        else:
            # Create a new entry and add it to the cache
            new_entry = {"original": original_locator}
            new_entry.update(new_strategy_dict)
            self._cache.append(new_entry)
            print(f"Added new cache entry for: {original_locator}")
        
        # Save the updated cache to file
        self.save_cache_to_file()
    
    def get_healed_locator(self, original_locator: str) -> Optional[Dict[str, str]]:
        """
        Retrieve a healed locator from the cache if it exists.
        
        Args:
            original_locator: The original locator to look up
            
        Returns:
            Dictionary containing the healed locator strategies or None if not found
        """
        entry = next(
            (item for item in self._cache if item.get("original") == original_locator),
            None
        )
        return entry
    
    def clear_cache(self) -> None:
        """Clear all entries from the cache."""
        self._cache = []
        self.save_cache_to_file()
        print("Cache cleared successfully.")
