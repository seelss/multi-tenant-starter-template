"""iOS model resolver.

This module handles the resolution of model information from model numbers
using the model_mapping.csv file.
"""

import logging
import csv
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
                        self.model_mappings[row['model_number']] = {
                            'model_name': row.get('model_name', ''),
                            'storage_capacity': row.get('storage_capacity', ''),
                            'housing_color': row.get('housing_color', '')
                        }
                logger.info(f"Loaded {len(self.model_mappings)} model mappings")
            else:
                logger.warning(f"Model mapping file not found: {self.model_mapping_path}")
                
        except Exception as e:
            logger.error(f"Error loading model mappings: {str(e)}")
    
    def resolve_model_info(self, model_number: str) -> Dict[str, str]:
        """Resolve detailed model information from model number.
        
        Args:
            model_number: The device model number (e.g., "MT0H2LL/A")
            
        Returns:
            Dictionary containing model_name, storage_capacity, and housing_color
        """
        if model_number in self.model_mappings:
            logger.info(f"Found mapping for model number {model_number}")
            return self.model_mappings[model_number]
        
        logger.warning(f"No mapping found for model number {model_number}")
        return {
            'model_name': f"Unknown ({model_number})",
            'storage_capacity': "Unknown",
            'housing_color': "Unknown"
        } 