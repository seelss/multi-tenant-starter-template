"""iOS region resolver.

This module handles the resolution of region information from region codes
using the region.csv file.
"""

import logging
import csv
from typing import Dict, Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class RegionResolver:
    """Resolves human-readable region names from region codes."""
    
    def __init__(self):
        """Initialize the resolver with region mapping data."""
        # Define path to mapping file
        data_dir = Path(__file__).parent.parent.parent / 'data'
        self.region_mapping_path = data_dir / 'region.csv'
        
        # Initialize mappings
        self.region_mappings = {}
        
        # Load mappings if file exists
        self._load_mappings()
    
    def _load_mappings(self):
        """Load region mapping data from CSV file."""
        try:
            # Load region mappings if file exists
            if self.region_mapping_path.exists():
                with open(self.region_mapping_path, 'r') as f:
                    reader = csv.DictReader(f)
                    for row in reader:
                        self.region_mappings[row['code']] = row.get('region', '')
                logger.info(f"Loaded {len(self.region_mappings)} region mappings")
            else:
                logger.warning(f"Region mapping file not found: {self.region_mapping_path}")
                
        except Exception as e:
            logger.error(f"Error loading region mappings: {str(e)}")
    
    def resolve_region_info(self, region_code: str) -> str:
        """Resolve human-readable region name from region code.
        
        Args:
            region_code: The region code (e.g., "LL/A" or "A")
            
        Returns:
            Human-readable region name
        """
        original_code = region_code
        
        # Extract the region code from model number format (e.g., "LL/A" -> "LL")
        if '/' in region_code:
            parts = region_code.split('/')
            if len(parts) > 0:
                region_code = parts[0]  # Use the part before the slash
        
        if region_code in self.region_mappings:
            logger.info(f"Found mapping for region code {region_code} from {original_code}")
            return self.region_mappings[region_code]
        
        logger.warning(f"No mapping found for region code {region_code} from {original_code}")
        return f"Unknown ({original_code})" 