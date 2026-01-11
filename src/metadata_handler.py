"""
Metadata Handler Module
Handles reading and writing EXIF metadata in image files.
"""

from PIL import Image
from PIL.ExifTags import TAGS
import os
from typing import Optional, Dict


class MetadataHandler:
    """Handles EXIF metadata operations for images."""
    
    def __init__(self, image_path: str):
        """
        Initialize metadata handler with an image file.
        
        Args:
            image_path: Path to the image file
        """
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image file not found: {image_path}")
        
        self.image_path = image_path
        self.image = Image.open(image_path)
    
    def read_metadata(self) -> Dict:
        """
        Read all metadata from the image.
        
        Returns:
            Dictionary of metadata tags
        """
        metadata = {}
        
        # Read EXIF data
        exifdata = self.image.getexif()
        if exifdata:
            for tag_id, value in exifdata.items():
                tag = TAGS.get(tag_id, tag_id)
                metadata[tag] = value
        
        # Read other metadata
        metadata['format'] = self.image.format
        metadata['mode'] = self.image.mode
        metadata['size'] = self.image.size
        
        return metadata
    
    def read_comment(self) -> Optional[str]:
        """
        Read comment from image metadata.
        
        Returns:
            Comment string or None if not found
        """
        exifdata = self.image.getexif()
        
        # Try different comment tags
        comment_tags = [270, 37510, 40092]  # ImageDescription, UserComment, etc.
        
        for tag_id in comment_tags:
            if tag_id in exifdata:
                comment = exifdata[tag_id]
                if isinstance(comment, (str, bytes)):
                    if isinstance(comment, bytes):
                        try:
                            comment = comment.decode('utf-8')
                        except UnicodeDecodeError:
                            continue
                    return comment
        
        return None
    
    def write_comment(self, comment: str, output_path: str) -> bool:
        """
        Write comment to image metadata and save to output path.
        
        Args:
            comment: Comment string to write
            output_path: Path to save the modified image
            
        Returns:
            True if successful, False otherwise
        """
        try:
            # Create output directory if it doesn't exist
            os.makedirs(os.path.dirname(output_path) if os.path.dirname(output_path) else '.', exist_ok=True)
            
            # Copy image
            output_image = self.image.copy()
            
            # Get existing EXIF data or create new
            exifdata = output_image.getexif()
            
            # Write comment to ImageDescription tag (tag 270)
            exifdata[270] = comment
            
            # Save image with EXIF data
            output_image.save(output_path, exif=exifdata)
            
            return True
        except Exception as e:
            print(f"Error writing metadata: {e}")
            return False
    
    def close(self):
        """Close the image file."""
        if self.image:
            self.image.close()

