"""iOS model resolver.

This module handles the resolution of model information from model numbers
using the model_mapping.csv file.
"""

import logging
import csv
import re
from typing import Dict, Any, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class ModelResolver:
    """Resolves detailed model information from model numbers."""
    
    def __init__(self):
        """Initialize the resolver with model mapping data."""
        # Define path to mapping file
        data_dir = Path(__file__).parent.parent.parent / 'data'
        self.model_mapping_path = data_dir / 'model_mapping.csv'
        
        # Initialize mappings
        self.model_mappings = {}
        self.normalized_mappings = {}  # For matching without first letter
        
        # Load mappings if file exists
        self._load_mappings()
    
    def _load_mappings(self):
        """Load model mapping data from CSV file."""
        try:
            # Load model mappings if file exists
            if self.model_mapping_path.exists():
                with open(self.model_mapping_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        model_number = row['model_number']
                        # Extract the base model without region suffix
                        base_model = self._extract_base_model(model_number)
                        
                        model_info = {
                            'model_name': row.get('model_name', ''),
                            'storage_capacity': row.get('storage_capacity', ''),
                            'housing_color': row.get('housing_color', ''),
                            'full_model_number': model_number  # Store the full model number too
                        }
                        
                        # Store mapping for the base model
                        if base_model and base_model != model_number:
                            # Only store if we don't already have an exact match
                            if base_model not in self.model_mappings:
                                self.model_mappings[base_model] = model_info
                        
                        # Also store the original model number
                        self.model_mappings[model_number] = model_info
                        
                        # Store normalized version (without first letter)
                        if len(base_model) > 1:
                            normalized_model = base_model[1:]  # Remove first letter
                            self.normalized_mappings[normalized_model] = model_info
                
                logger.info(f"Loaded {len(self.model_mappings)} model mappings")
                logger.info(f"Created {len(self.normalized_mappings)} normalized mappings")
            else:
                logger.warning(f"Model mapping file not found: {self.model_mapping_path}")
                
        except Exception as e:
            logger.error(f"Error loading model mappings: {str(e)}")
    
    def _extract_base_model(self, model_number: str) -> str:
        """Extract the base model number without region suffix.
        
        For example, "MQ8V3LL/A" -> "MQ8V3"
        
        Args:
            model_number: The full model number with region suffix
            
        Returns:
            The base model number without region suffix
        """
        # Pattern to match: Letters and numbers followed by 2 letters, slash, letter
        # Example: "MQ8V3LL/A" -> "MQ8V3"
        match = re.match(r'^([A-Za-z0-9]+)[A-Za-z]{2}/[A-Za-z]', model_number)
        if match:
            return match.group(1)
        return model_number
    
    def _normalize_model_number(self, model_number: str) -> str:
        """Normalize a model number by removing the first letter.
        
        For example, "MQ8V3" -> "Q8V3"
        
        Args:
            model_number: The model number to normalize
            
        Returns:
            The normalized model number without the first letter
        """
        if model_number and len(model_number) > 1:
            return model_number[1:]
        return model_number
    
    def resolve_model_info(self, model_number: str) -> Dict[str, str]:
        """Resolve detailed model information from model number.
        
        Args:
            model_number: The device model number (e.g., "MQ8V3" or "MQ8V3LL/A")
            
        Returns:
            Dictionary containing model_name, storage_capacity, and housing_color
        """
        # First try direct lookup
        if model_number in self.model_mappings:
            logger.info(f"Found exact mapping for model number {model_number}")
            return self.model_mappings[model_number]
        
        # Extract base model if it has a region code
        base_model = self._extract_base_model(model_number)
        if base_model != model_number and base_model in self.model_mappings:
            logger.info(f"Found mapping for base model {base_model}")
            return self.model_mappings[base_model]
        
        # Try looking up without the first letter
        normalized_model = self._normalize_model_number(base_model)
        if normalized_model in self.normalized_mappings:
            logger.info(f"Found mapping for normalized model {normalized_model} from {model_number}")
            return self.normalized_mappings[normalized_model]
        
        logger.warning(f"No mapping found for model number {model_number}")
        return {
            'model_name': f"Unknown ({model_number})",
            'storage_capacity': "Unknown",
            'housing_color': "Unknown"
        } 