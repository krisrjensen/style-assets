"""
Font Service
Manages font assets and metadata
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class FontService:
    """Service for managing font assets"""
    
    def __init__(self):
        self.fonts_directory = 'fonts'
        self._ensure_fonts_directory()
        self.font_registry = self._initialize_font_registry()
        self._register_default_fonts()
    
    def _ensure_fonts_directory(self):
        """Ensure fonts directory exists"""
        os.makedirs(self.fonts_directory, exist_ok=True)
    
    def _initialize_font_registry(self) -> Dict[str, Any]:
        """Initialize font registry"""
        return {
            'fonts': {},
            'categories': {
                'serif': [],
                'sans_serif': [],
                'monospace': [],
                'decorative': []
            },
            'metadata': {
                'last_updated': self._get_timestamp(),
                'total_fonts': 0
            }
        }
    
    def _register_default_fonts(self):
        """Register default system fonts"""
        default_fonts = [
            {
                'name': 'Times New Roman',
                'family': 'Times',
                'category': 'serif',
                'weight': 'normal',
                'style': 'normal',
                'formats': ['ttf'],
                'usage': 'Academic papers, formal documents',
                'compatibility': ['ieee', 'nature', 'apa'],
                'file_size': '1.2MB',
                'character_set': 'latin_extended',
                'license': 'commercial'
            },
            {
                'name': 'Arial',
                'family': 'Arial',
                'category': 'sans_serif',
                'weight': 'normal',
                'style': 'normal',
                'formats': ['ttf'],
                'usage': 'Modern documents, presentations',
                'compatibility': ['modern', 'web'],
                'file_size': '1.1MB',
                'character_set': 'latin_extended',
                'license': 'commercial'
            },
            {
                'name': 'Helvetica',
                'family': 'Helvetica',
                'category': 'sans_serif',
                'weight': 'normal',
                'style': 'normal',
                'formats': ['ttf', 'otf'],
                'usage': 'Professional documents, branding',
                'compatibility': ['modern', 'corporate'],
                'file_size': '1.3MB',
                'character_set': 'latin_extended',
                'license': 'commercial'
            },
            {
                'name': 'Courier New',
                'family': 'Courier',
                'category': 'monospace',
                'weight': 'normal',
                'style': 'normal',
                'formats': ['ttf'],
                'usage': 'Code blocks, technical documentation',
                'compatibility': ['technical', 'code'],
                'file_size': '0.8MB',
                'character_set': 'latin_basic',
                'license': 'commercial'
            },
            {
                'name': 'Georgia',
                'family': 'Georgia',
                'category': 'serif',
                'weight': 'normal',
                'style': 'normal',
                'formats': ['ttf'],
                'usage': 'Web content, readable documents',
                'compatibility': ['web', 'modern'],
                'file_size': '1.0MB',
                'character_set': 'latin_extended',
                'license': 'commercial'
            }
        ]
        
        for font_info in default_fonts:
            font_id = self._generate_font_id(font_info['name'])
            self.font_registry['fonts'][font_id] = {
                **font_info,
                'id': font_id,
                'registered': self._get_timestamp(),
                'status': 'available',
                'download_count': 0
            }
            
            # Add to category
            category = font_info['category']
            if category in self.font_registry['categories']:
                self.font_registry['categories'][category].append(font_id)
        
        # Update metadata
        self.font_registry['metadata']['total_fonts'] = len(self.font_registry['fonts'])
        self.font_registry['metadata']['last_updated'] = self._get_timestamp()
    
    def get_available_fonts(self) -> Dict[str, Any]:
        """Get list of available fonts"""
        fonts_list = []
        
        for font_id, font_info in self.font_registry['fonts'].items():
            fonts_list.append({
                'id': font_id,
                'name': font_info['name'],
                'family': font_info['family'],
                'category': font_info['category'],
                'weight': font_info['weight'],
                'style': font_info['style'],
                'formats': font_info['formats'],
                'usage': font_info['usage'],
                'compatibility': font_info['compatibility'],
                'status': font_info['status']
            })
        
        return {
            'fonts': fonts_list,
            'categories': {
                category: len(font_ids) 
                for category, font_ids in self.font_registry['categories'].items()
            },
            'total_fonts': len(fonts_list),
            'metadata': {
                'timestamp': self._get_timestamp(),
                'service': 'font_service'
            }
        }
    
    def get_font_details(self, font_name: str) -> Optional[Dict[str, Any]]:
        """Get detailed information for specific font"""
        font_id = self._generate_font_id(font_name)
        
        if font_id in self.font_registry['fonts']:
            font_info = self.font_registry['fonts'][font_id].copy()
            
            # Add additional details
            font_info['metadata'] = {
                'last_accessed': self._get_timestamp(),
                'download_url': f'/api/fonts/{font_name}/download',
                'preview_url': f'/api/fonts/{font_name}/preview'
            }
            
            return font_info
        
        return None
    
    def get_font_path(self, font_name: str) -> Optional[str]:
        """Get file path for font"""
        font_id = self._generate_font_id(font_name)
        
        if font_id in self.font_registry['fonts']:
            font_info = self.font_registry['fonts'][font_id]
            
            # Try different file extensions
            for format_ext in font_info['formats']:
                file_path = os.path.join(
                    self.fonts_directory, 
                    f"{font_name.lower().replace(' ', '_')}.{format_ext}"
                )
                if os.path.exists(file_path):
                    # Update download count
                    self.font_registry['fonts'][font_id]['download_count'] += 1
                    return file_path
            
            # If no file exists, create a placeholder
            return self._create_font_placeholder(font_name)
        
        return None
    
    def get_fonts_by_category(self, category: str) -> Dict[str, Any]:
        """Get fonts by category"""
        if category not in self.font_registry['categories']:
            return {
                'error': f'Unknown category: {category}',
                'available_categories': list(self.font_registry['categories'].keys())
            }
        
        font_ids = self.font_registry['categories'][category]
        fonts = []
        
        for font_id in font_ids:
            if font_id in self.font_registry['fonts']:
                font_info = self.font_registry['fonts'][font_id]
                fonts.append({
                    'id': font_id,
                    'name': font_info['name'],
                    'family': font_info['family'],
                    'weight': font_info['weight'],
                    'style': font_info['style'],
                    'usage': font_info['usage']
                })
        
        return {
            'category': category,
            'fonts': fonts,
            'count': len(fonts),
            'timestamp': self._get_timestamp()
        }
    
    def get_fonts_by_compatibility(self, style_name: str) -> Dict[str, Any]:
        """Get fonts compatible with specific style"""
        compatible_fonts = []
        
        for font_id, font_info in self.font_registry['fonts'].items():
            if style_name in font_info.get('compatibility', []):
                compatible_fonts.append({
                    'id': font_id,
                    'name': font_info['name'],
                    'family': font_info['family'],
                    'category': font_info['category'],
                    'weight': font_info['weight'],
                    'usage': font_info['usage']
                })
        
        return {
            'style': style_name,
            'compatible_fonts': compatible_fonts,
            'count': len(compatible_fonts),
            'timestamp': self._get_timestamp()
        }
    
    def register_custom_font(self, font_data: Dict[str, Any]) -> Dict[str, Any]:
        """Register a custom font"""
        required_fields = ['name', 'family', 'category']
        for field in required_fields:
            if field not in font_data:
                return {
                    'success': False,
                    'error': f'Missing required field: {field}'
                }
        
        font_id = self._generate_font_id(font_data['name'])
        
        # Check if font already exists
        if font_id in self.font_registry['fonts']:
            return {
                'success': False,
                'error': f'Font {font_data["name"]} already exists'
            }
        
        # Add default values
        font_info = {
            'id': font_id,
            'name': font_data['name'],
            'family': font_data['family'],
            'category': font_data['category'],
            'weight': font_data.get('weight', 'normal'),
            'style': font_data.get('style', 'normal'),
            'formats': font_data.get('formats', ['ttf']),
            'usage': font_data.get('usage', 'General purpose'),
            'compatibility': font_data.get('compatibility', []),
            'file_size': font_data.get('file_size', 'Unknown'),
            'character_set': font_data.get('character_set', 'latin_basic'),
            'license': font_data.get('license', 'custom'),
            'registered': self._get_timestamp(),
            'status': 'available',
            'download_count': 0
        }
        
        # Register font
        self.font_registry['fonts'][font_id] = font_info
        
        # Add to category
        category = font_info['category']
        if category in self.font_registry['categories']:
            self.font_registry['categories'][category].append(font_id)
        else:
            self.font_registry['categories'][category] = [font_id]
        
        # Update metadata
        self.font_registry['metadata']['total_fonts'] = len(self.font_registry['fonts'])
        self.font_registry['metadata']['last_updated'] = self._get_timestamp()
        
        return {
            'success': True,
            'font_id': font_id,
            'message': f'Font {font_data["name"]} registered successfully',
            'timestamp': self._get_timestamp()
        }
    
    def get_font_usage_stats(self) -> Dict[str, Any]:
        """Get font usage statistics"""
        stats = {
            'total_fonts': len(self.font_registry['fonts']),
            'category_breakdown': {},
            'most_downloaded': [],
            'recent_additions': [],
            'license_breakdown': {}
        }
        
        # Category breakdown
        for category, font_ids in self.font_registry['categories'].items():
            stats['category_breakdown'][category] = len(font_ids)
        
        # Most downloaded fonts
        fonts_by_downloads = sorted(
            self.font_registry['fonts'].items(),
            key=lambda x: x[1]['download_count'],
            reverse=True
        )
        
        stats['most_downloaded'] = [
            {
                'name': font_info['name'],
                'downloads': font_info['download_count']
            }
            for font_id, font_info in fonts_by_downloads[:5]
        ]
        
        # License breakdown
        license_counts = {}
        for font_info in self.font_registry['fonts'].values():
            license_type = font_info.get('license', 'unknown')
            license_counts[license_type] = license_counts.get(license_type, 0) + 1
        
        stats['license_breakdown'] = license_counts
        stats['timestamp'] = self._get_timestamp()
        
        return stats
    
    def _create_font_placeholder(self, font_name: str) -> str:
        """Create a placeholder font file"""
        placeholder_content = f"""
        Font: {font_name}
        Status: Placeholder file
        Created: {self._get_timestamp()}
        
        This is a placeholder for the {font_name} font.
        The actual font file should be placed in the fonts directory.
        """
        
        placeholder_path = os.path.join(
            self.fonts_directory, 
            f"{font_name.lower().replace(' ', '_')}_placeholder.txt"
        )
        
        with open(placeholder_path, 'w') as f:
            f.write(placeholder_content)
        
        return placeholder_path
    
    def _generate_font_id(self, font_name: str) -> str:
        """Generate unique font ID"""
        return font_name.lower().replace(' ', '_').replace('-', '_')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()