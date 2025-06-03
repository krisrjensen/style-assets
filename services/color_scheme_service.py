"""
Color Scheme Service
Manages color schemes for different publication styles
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class ColorSchemeService:
    """Service for managing color schemes"""
    
    def __init__(self):
        self.schemes_directory = 'color_schemes'
        self._ensure_schemes_directory()
        self.scheme_registry = self._initialize_scheme_registry()
        self._create_default_schemes()
    
    def _ensure_schemes_directory(self):
        """Ensure color schemes directory exists"""
        os.makedirs(self.schemes_directory, exist_ok=True)
    
    def _initialize_scheme_registry(self) -> Dict[str, Any]:
        """Initialize color scheme registry"""
        return {
            'schemes': {},
            'categories': {
                'academic': [],
                'modern': [],
                'corporate': [],
                'creative': []
            },
            'metadata': {
                'last_updated': self._get_timestamp(),
                'total_schemes': 0
            }
        }
    
    def _create_default_schemes(self):
        """Create default color schemes"""
        default_schemes = [
            {
                'name': 'Academic Blue',
                'category': 'academic',
                'description': 'Professional blue tones for academic publications',
                'colors': {
                    'primary': '#003366',
                    'secondary': '#0066CC',
                    'accent': '#3399FF',
                    'background': '#FFFFFF',
                    'text': '#000000',
                    'text_secondary': '#333333',
                    'border': '#CCCCCC',
                    'highlight': '#FFFF99',
                    'error': '#CC0000',
                    'success': '#006600'
                },
                'usage': 'IEEE papers, technical documents',
                'compatibility': ['ieee', 'technical'],
                'accessibility': {
                    'wcag_aa_compliant': True,
                    'contrast_ratio': 4.5
                }
            },
            {
                'name': 'Nature Green',
                'category': 'academic',
                'description': 'Natural green palette for scientific publications',
                'colors': {
                    'primary': '#2D5016',
                    'secondary': '#4A7C28',
                    'accent': '#6FA83B',
                    'background': '#FFFFFF',
                    'text': '#000000',
                    'text_secondary': '#2D2D2D',
                    'border': '#B8D4A5',
                    'highlight': '#E8F5E8',
                    'error': '#B71C1C',
                    'success': '#2E7D32'
                },
                'usage': 'Nature journal style, environmental studies',
                'compatibility': ['nature', 'environmental'],
                'accessibility': {
                    'wcag_aa_compliant': True,
                    'contrast_ratio': 4.8
                }
            },
            {
                'name': 'Modern Grayscale',
                'category': 'modern',
                'description': 'Clean grayscale palette for contemporary designs',
                'colors': {
                    'primary': '#2C2C2C',
                    'secondary': '#4A4A4A',
                    'accent': '#007ACC',
                    'background': '#FFFFFF',
                    'text': '#1A1A1A',
                    'text_secondary': '#666666',
                    'border': '#E0E0E0',
                    'highlight': '#F5F5F5',
                    'error': '#E53E3E',
                    'success': '#38A169'
                },
                'usage': 'Modern documents, presentations',
                'compatibility': ['modern', 'minimal'],
                'accessibility': {
                    'wcag_aa_compliant': True,
                    'contrast_ratio': 7.2
                }
            },
            {
                'name': 'Corporate Blue',
                'category': 'corporate',
                'description': 'Professional corporate color scheme',
                'colors': {
                    'primary': '#1E3A8A',
                    'secondary': '#3B82F6',
                    'accent': '#60A5FA',
                    'background': '#FFFFFF',
                    'text': '#111827',
                    'text_secondary': '#4B5563',
                    'border': '#D1D5DB',
                    'highlight': '#EBF8FF',
                    'error': '#DC2626',
                    'success': '#059669'
                },
                'usage': 'Business reports, corporate documents',
                'compatibility': ['corporate', 'business'],
                'accessibility': {
                    'wcag_aa_compliant': True,
                    'contrast_ratio': 5.1
                }
            },
            {
                'name': 'Creative Palette',
                'category': 'creative',
                'description': 'Vibrant colors for creative projects',
                'colors': {
                    'primary': '#7C3AED',
                    'secondary': '#A855F7',
                    'accent': '#C084FC',
                    'background': '#FEFEFE',
                    'text': '#1F2937',
                    'text_secondary': '#374151',
                    'border': '#E5E7EB',
                    'highlight': '#FDF4FF',
                    'error': '#F87171',
                    'success': '#34D399'
                },
                'usage': 'Creative presentations, artistic documents',
                'compatibility': ['creative', 'artistic'],
                'accessibility': {
                    'wcag_aa_compliant': False,
                    'contrast_ratio': 3.8
                }
            }
        ]
        
        for scheme_data in default_schemes:
            self._save_scheme_to_file(scheme_data)
            scheme_id = self._generate_scheme_id(scheme_data['name'])
            
            self.scheme_registry['schemes'][scheme_id] = {
                **scheme_data,
                'id': scheme_id,
                'created': self._get_timestamp(),
                'status': 'active',
                'usage_count': 0
            }
            
            # Add to category
            category = scheme_data['category']
            if category in self.scheme_registry['categories']:
                self.scheme_registry['categories'][category].append(scheme_id)
        
        # Update metadata
        self.scheme_registry['metadata']['total_schemes'] = len(self.scheme_registry['schemes'])
        self.scheme_registry['metadata']['last_updated'] = self._get_timestamp()
    
    def _save_scheme_to_file(self, scheme_data: Dict[str, Any]):
        """Save color scheme to JSON file"""
        filename = f"{scheme_data['name'].lower().replace(' ', '_')}.json"
        file_path = os.path.join(self.schemes_directory, filename)
        
        with open(file_path, 'w') as f:
            json.dump(scheme_data, f, indent=2)
    
    def get_available_schemes(self) -> Dict[str, Any]:
        """Get list of available color schemes"""
        schemes_list = []
        
        for scheme_id, scheme_info in self.scheme_registry['schemes'].items():
            schemes_list.append({
                'id': scheme_id,
                'name': scheme_info['name'],
                'category': scheme_info['category'],
                'description': scheme_info['description'],
                'usage': scheme_info['usage'],
                'compatibility': scheme_info['compatibility'],
                'accessibility': scheme_info['accessibility'],
                'status': scheme_info['status']
            })
        
        return {
            'schemes': schemes_list,
            'categories': {
                category: len(scheme_ids) 
                for category, scheme_ids in self.scheme_registry['categories'].items()
            },
            'total_schemes': len(schemes_list),
            'metadata': {
                'timestamp': self._get_timestamp(),
                'service': 'color_scheme_service'
            }
        }
    
    def get_scheme(self, scheme_name: str) -> Optional[Dict[str, Any]]:
        """Get specific color scheme"""
        scheme_id = self._generate_scheme_id(scheme_name)
        
        if scheme_id in self.scheme_registry['schemes']:
            scheme_info = self.scheme_registry['schemes'][scheme_id].copy()
            
            # Update usage count
            self.scheme_registry['schemes'][scheme_id]['usage_count'] += 1
            
            # Add metadata
            scheme_info['metadata'] = {
                'last_accessed': self._get_timestamp(),
                'preview_url': f'/api/color-schemes/{scheme_name}/preview',
                'css_url': f'/api/color-schemes/{scheme_name}/css'
            }
            
            return scheme_info
        
        return None
    
    def create_scheme(self, scheme_data: Dict[str, Any]) -> Dict[str, Any]:
        """Create new color scheme"""
        required_fields = ['name', 'category', 'colors']
        for field in required_fields:
            if field not in scheme_data:
                return {
                    'success': False,
                    'error': f'Missing required field: {field}'
                }
        
        scheme_id = self._generate_scheme_id(scheme_data['name'])
        
        # Check if scheme already exists
        if scheme_id in self.scheme_registry['schemes']:
            return {
                'success': False,
                'error': f'Color scheme {scheme_data["name"]} already exists'
            }
        
        # Validate colors
        color_validation = self._validate_colors(scheme_data['colors'])
        if not color_validation['valid']:
            return {
                'success': False,
                'error': 'Invalid color format',
                'details': color_validation['errors']
            }
        
        # Add default values
        scheme_info = {
            'id': scheme_id,
            'name': scheme_data['name'],
            'category': scheme_data['category'],
            'description': scheme_data.get('description', ''),
            'colors': scheme_data['colors'],
            'usage': scheme_data.get('usage', 'General purpose'),
            'compatibility': scheme_data.get('compatibility', []),
            'accessibility': scheme_data.get('accessibility', {
                'wcag_aa_compliant': False,
                'contrast_ratio': 0
            }),
            'created': self._get_timestamp(),
            'status': 'active',
            'usage_count': 0
        }
        
        # Save to file
        self._save_scheme_to_file(scheme_info)
        
        # Register scheme
        self.scheme_registry['schemes'][scheme_id] = scheme_info
        
        # Add to category
        category = scheme_info['category']
        if category in self.scheme_registry['categories']:
            self.scheme_registry['categories'][category].append(scheme_id)
        else:
            self.scheme_registry['categories'][category] = [scheme_id]
        
        # Update metadata
        self.scheme_registry['metadata']['total_schemes'] = len(self.scheme_registry['schemes'])
        self.scheme_registry['metadata']['last_updated'] = self._get_timestamp()
        
        return {
            'success': True,
            'scheme_id': scheme_id,
            'message': f'Color scheme {scheme_data["name"]} created successfully',
            'timestamp': self._get_timestamp()
        }
    
    def get_schemes_by_category(self, category: str) -> Dict[str, Any]:
        """Get color schemes by category"""
        if category not in self.scheme_registry['categories']:
            return {
                'error': f'Unknown category: {category}',
                'available_categories': list(self.scheme_registry['categories'].keys())
            }
        
        scheme_ids = self.scheme_registry['categories'][category]
        schemes = []
        
        for scheme_id in scheme_ids:
            if scheme_id in self.scheme_registry['schemes']:
                scheme_info = self.scheme_registry['schemes'][scheme_id]
                schemes.append({
                    'id': scheme_id,
                    'name': scheme_info['name'],
                    'description': scheme_info['description'],
                    'colors': scheme_info['colors'],
                    'usage': scheme_info['usage']
                })
        
        return {
            'category': category,
            'schemes': schemes,
            'count': len(schemes),
            'timestamp': self._get_timestamp()
        }
    
    def get_schemes_by_compatibility(self, style_name: str) -> Dict[str, Any]:
        """Get color schemes compatible with specific style"""
        compatible_schemes = []
        
        for scheme_id, scheme_info in self.scheme_registry['schemes'].items():
            if style_name in scheme_info.get('compatibility', []):
                compatible_schemes.append({
                    'id': scheme_id,
                    'name': scheme_info['name'],
                    'category': scheme_info['category'],
                    'description': scheme_info['description'],
                    'colors': scheme_info['colors']
                })
        
        return {
            'style': style_name,
            'compatible_schemes': compatible_schemes,
            'count': len(compatible_schemes),
            'timestamp': self._get_timestamp()
        }
    
    def generate_css(self, scheme_name: str, css_format: str = 'variables') -> Dict[str, Any]:
        """Generate CSS from color scheme"""
        scheme = self.get_scheme(scheme_name)
        if not scheme:
            return {
                'success': False,
                'error': 'Color scheme not found'
            }
        
        colors = scheme['colors']
        
        if css_format == 'variables':
            css_content = self._generate_css_variables(colors)
        elif css_format == 'classes':
            css_content = self._generate_css_classes(colors)
        elif css_format == 'complete':
            css_content = self._generate_complete_css(colors, scheme_name)
        else:
            return {
                'success': False,
                'error': f'Unknown CSS format: {css_format}'
            }
        
        return {
            'success': True,
            'scheme_name': scheme_name,
            'css_format': css_format,
            'css_content': css_content,
            'timestamp': self._get_timestamp()
        }
    
    def _generate_css_variables(self, colors: Dict[str, str]) -> str:
        """Generate CSS variables"""
        css_lines = [':root {']
        
        for color_name, color_value in colors.items():
            css_lines.append(f'  --color-{color_name.replace("_", "-")}: {color_value};')
        
        css_lines.append('}')
        return '\n'.join(css_lines)
    
    def _generate_css_classes(self, colors: Dict[str, str]) -> str:
        """Generate CSS classes for colors"""
        css_lines = []
        
        for color_name, color_value in colors.items():
            class_name = color_name.replace('_', '-')
            
            # Background color class
            css_lines.append(f'.bg-{class_name} {{')
            css_lines.append(f'  background-color: {color_value};')
            css_lines.append('}')
            css_lines.append('')
            
            # Text color class
            css_lines.append(f'.text-{class_name} {{')
            css_lines.append(f'  color: {color_value};')
            css_lines.append('}')
            css_lines.append('')
            
            # Border color class
            css_lines.append(f'.border-{class_name} {{')
            css_lines.append(f'  border-color: {color_value};')
            css_lines.append('}')
            css_lines.append('')
        
        return '\n'.join(css_lines)
    
    def _generate_complete_css(self, colors: Dict[str, str], scheme_name: str) -> str:
        """Generate complete CSS theme"""
        css_lines = [
            f'/* {scheme_name} Color Scheme */',
            f'/* Generated on {self._get_timestamp()} */',
            '',
            self._generate_css_variables(colors),
            '',
            self._generate_css_classes(colors),
            '',
            '/* Base styling */',
            'body {',
            f'  background-color: {colors.get("background", "#FFFFFF")};',
            f'  color: {colors.get("text", "#000000")};',
            '}',
            '',
            'h1, h2, h3, h4, h5, h6 {',
            f'  color: {colors.get("primary", "#000000")};',
            '}',
            '',
            'a {',
            f'  color: {colors.get("accent", "#0066CC")};',
            '}',
            '',
            'a:hover {',
            f'  color: {colors.get("secondary", "#003366")};',
            '}',
            '',
            '.highlight {',
            f'  background-color: {colors.get("highlight", "#FFFF99")};',
            '}',
            '',
            '.error {',
            f'  color: {colors.get("error", "#CC0000")};',
            '}',
            '',
            '.success {',
            f'  color: {colors.get("success", "#006600")};',
            '}'
        ]
        
        return '\n'.join(css_lines)
    
    def _validate_colors(self, colors: Dict[str, str]) -> Dict[str, Any]:
        """Validate color format"""
        validation = {
            'valid': True,
            'errors': []
        }
        
        import re
        hex_pattern = re.compile(r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$')
        rgb_pattern = re.compile(r'^rgb\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*\)$')
        rgba_pattern = re.compile(r'^rgba\(\s*\d+\s*,\s*\d+\s*,\s*\d+\s*,\s*[\d.]+\s*\)$')
        
        for color_name, color_value in colors.items():
            if not (hex_pattern.match(color_value) or 
                   rgb_pattern.match(color_value) or 
                   rgba_pattern.match(color_value)):
                validation['errors'].append(
                    f'Invalid color format for {color_name}: {color_value}'
                )
                validation['valid'] = False
        
        return validation
    
    def get_scheme_usage_stats(self) -> Dict[str, Any]:
        """Get color scheme usage statistics"""
        stats = {
            'total_schemes': len(self.scheme_registry['schemes']),
            'category_breakdown': {},
            'most_used': [],
            'accessibility_compliant': 0,
            'total_usage': 0
        }
        
        # Category breakdown
        for category, scheme_ids in self.scheme_registry['categories'].items():
            stats['category_breakdown'][category] = len(scheme_ids)
        
        # Most used schemes
        schemes_by_usage = sorted(
            self.scheme_registry['schemes'].items(),
            key=lambda x: x[1]['usage_count'],
            reverse=True
        )
        
        stats['most_used'] = [
            {
                'name': scheme_info['name'],
                'usage_count': scheme_info['usage_count']
            }
            for scheme_id, scheme_info in schemes_by_usage[:5]
        ]
        
        # Accessibility and total usage
        for scheme_info in self.scheme_registry['schemes'].values():
            if scheme_info.get('accessibility', {}).get('wcag_aa_compliant', False):
                stats['accessibility_compliant'] += 1
            stats['total_usage'] += scheme_info['usage_count']
        
        stats['timestamp'] = self._get_timestamp()
        return stats
    
    def _generate_scheme_id(self, scheme_name: str) -> str:
        """Generate unique scheme ID"""
        return scheme_name.lower().replace(' ', '_').replace('-', '_')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()