"""
Preview Module
Compares original and modified file properties.
"""

import os
from typing import Dict, Optional
from PIL import Image


class PreviewModule:
    """Provides preview and comparison of image files."""
    
    @staticmethod
    def get_file_properties(file_path: str) -> Optional[Dict]:
        """
        Get properties of an image file.
        
        Args:
            file_path: Path to the image file
            
        Returns:
            Dictionary of file properties or None if file doesn't exist
        """
        if not os.path.exists(file_path):
            return None
        
        try:
            properties = {}
            
            # File properties
            stat = os.stat(file_path)
            properties['file_size'] = stat.st_size
            properties['file_size_mb'] = round(stat.st_size / (1024 * 1024), 2)
            from datetime import datetime

            local_time = datetime.fromtimestamp(stat.st_mtime)
            properties['modified_time'] = local_time
            
            # Image properties
            with Image.open(file_path) as img:
                properties['format'] = img.format
                properties['mode'] = img.mode
                properties['size'] = img.size
                properties['width'] = img.width
                properties['height'] = img.height
                
                # Metadata
                exifdata = img.getexif()
                if exifdata:
                    properties['has_exif'] = True
                    properties['exif_tags_count'] = len(exifdata)
                else:
                    properties['has_exif'] = False
                    properties['exif_tags_count'] = 0
            
            return properties
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def compare_files(original_path: str, modified_path: str) -> Dict:
        """
        Compare original and modified file properties.
        
        Args:
            original_path: Path to original file
            modified_path: Path to modified file
            
        Returns:
            Dictionary with comparison results
        """
        original_props = PreviewModule.get_file_properties(original_path)
        modified_props = PreviewModule.get_file_properties(modified_path)
        
        comparison = {
            'original': original_props,
            'modified': modified_props,
            'differences': {}
        }
        
        if original_props and modified_props:
            # Compare file sizes
            if original_props.get('file_size') != modified_props.get('file_size'):
                comparison['differences']['file_size'] = {
                    'original': original_props.get('file_size'),
                    'modified': modified_props.get('file_size')
                }
            
            # Compare EXIF tag counts
            if original_props.get('exif_tags_count') != modified_props.get('exif_tags_count'):
                comparison['differences']['exif_tags_count'] = {
                    'original': original_props.get('exif_tags_count'),
                    'modified': modified_props.get('exif_tags_count')
                }
            
            # Check if image properties are the same
            if original_props.get('size') != modified_props.get('size'):
                comparison['differences']['image_size'] = {
                    'original': original_props.get('size'),
                    'modified': modified_props.get('size')
                }
        
        return comparison

