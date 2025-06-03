"""
Asset Manager Service
Manages style assets across the ecosystem
"""

import os
import json
import zipfile
import shutil
from typing import Dict, List, Any, Optional
from datetime import datetime
import hashlib

class AssetManager:
    """Service for managing style assets"""
    
    def __init__(self):
        self.assets_root = '.'
        self.bundle_directory = 'bundles'
        self._ensure_directories()
        self.asset_registry = self._initialize_asset_registry()
    
    def _ensure_directories(self):
        """Ensure required directories exist"""
        directories = [
            'fonts', 'color_schemes', 'templates', self.bundle_directory
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    def _initialize_asset_registry(self) -> Dict[str, Any]:
        """Initialize asset registry"""
        return {
            'fonts': {},
            'color_schemes': {},
            'templates': {},
            'bundles': {},
            'metadata': {
                'last_updated': self._get_timestamp(),
                'version': '1.0.0'
            }
        }
    
    def create_bundle(self, bundle_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create asset bundle for specific style configuration
        
        Args:
            bundle_config: Bundle configuration
            
        Returns:
            Dictionary containing bundle information
        """
        bundle_name = bundle_config.get('name', 'default_bundle')
        style_name = bundle_config.get('style', 'default')
        include_fonts = bundle_config.get('include_fonts', True)
        include_color_schemes = bundle_config.get('include_color_schemes', True)
        include_templates = bundle_config.get('include_templates', True)
        
        bundle_id = self._generate_bundle_id(bundle_name, style_name)
        bundle_path = os.path.join(self.bundle_directory, f'{bundle_id}.zip')
        
        # Create bundle manifest
        manifest = {
            'bundle_id': bundle_id,
            'bundle_name': bundle_name,
            'style': style_name,
            'created': self._get_timestamp(),
            'assets': {
                'fonts': [],
                'color_schemes': [],
                'templates': []
            },
            'metadata': bundle_config.get('metadata', {})
        }
        
        # Create ZIP bundle
        with zipfile.ZipFile(bundle_path, 'w', zipfile.ZIP_DEFLATED) as bundle_zip:
            # Add fonts if requested
            if include_fonts:
                font_assets = self._get_style_fonts(style_name)
                for font_asset in font_assets:
                    if os.path.exists(font_asset['path']):
                        bundle_zip.write(font_asset['path'], f"fonts/{font_asset['filename']}")
                        manifest['assets']['fonts'].append(font_asset)
            
            # Add color schemes if requested
            if include_color_schemes:
                color_assets = self._get_style_color_schemes(style_name)
                for color_asset in color_assets:
                    if os.path.exists(color_asset['path']):
                        bundle_zip.write(color_asset['path'], f"color_schemes/{color_asset['filename']}")
                        manifest['assets']['color_schemes'].append(color_asset)
            
            # Add templates if requested
            if include_templates:
                template_assets = self._get_style_templates(style_name)
                for template_asset in template_assets:
                    if os.path.exists(template_asset['path']):
                        bundle_zip.write(template_asset['path'], f"templates/{template_asset['filename']}")
                        manifest['assets']['templates'].append(template_asset)
            
            # Add manifest
            manifest_json = json.dumps(manifest, indent=2)
            bundle_zip.writestr('manifest.json', manifest_json)
        
        # Calculate bundle size and checksum
        bundle_size = os.path.getsize(bundle_path)
        bundle_checksum = self._calculate_file_checksum(bundle_path)
        
        # Update asset registry
        self.asset_registry['bundles'][bundle_id] = {
            'bundle_name': bundle_name,
            'style': style_name,
            'path': bundle_path,
            'size': bundle_size,
            'checksum': bundle_checksum,
            'created': self._get_timestamp(),
            'manifest': manifest
        }
        
        return {
            'success': True,
            'bundle_id': bundle_id,
            'bundle_name': bundle_name,
            'style': style_name,
            'bundle_path': bundle_path,
            'bundle_size': bundle_size,
            'checksum': bundle_checksum,
            'asset_count': {
                'fonts': len(manifest['assets']['fonts']),
                'color_schemes': len(manifest['assets']['color_schemes']),
                'templates': len(manifest['assets']['templates'])
            },
            'download_url': f'/api/bundles/{bundle_id}/download',
            'timestamp': self._get_timestamp()
        }
    
    def _get_style_fonts(self, style_name: str) -> List[Dict[str, Any]]:
        """Get fonts for specific style"""
        # Mock implementation - would be based on style configuration
        default_fonts = [
            {
                'name': 'Times New Roman',
                'filename': 'times-new-roman.ttf',
                'path': 'fonts/times-new-roman.ttf',
                'type': 'serif',
                'weight': 'normal'
            },
            {
                'name': 'Arial',
                'filename': 'arial.ttf',
                'path': 'fonts/arial.ttf',
                'type': 'sans-serif',
                'weight': 'normal'
            }
        ]
        
        # Style-specific font mappings
        style_fonts = {
            'ieee': [default_fonts[0]],  # Times New Roman
            'nature': [default_fonts[0]],  # Times New Roman
            'apa': [default_fonts[0]],  # Times New Roman
            'modern': [default_fonts[1]]  # Arial
        }
        
        return style_fonts.get(style_name, default_fonts)
    
    def _get_style_color_schemes(self, style_name: str) -> List[Dict[str, Any]]:
        """Get color schemes for specific style"""
        default_schemes = [
            {
                'name': 'Academic',
                'filename': 'academic.json',
                'path': 'color_schemes/academic.json',
                'type': 'professional'
            },
            {
                'name': 'Modern Blue',
                'filename': 'modern_blue.json',
                'path': 'color_schemes/modern_blue.json',
                'type': 'contemporary'
            }
        ]
        
        return default_schemes
    
    def _get_style_templates(self, style_name: str) -> List[Dict[str, Any]]:
        """Get templates for specific style"""
        style_templates = [
            {
                'name': f'{style_name.upper()} Article Template',
                'filename': f'{style_name}_article.html',
                'path': f'templates/{style_name}_article.html',
                'type': 'article'
            },
            {
                'name': f'{style_name.upper()} CSS',
                'filename': f'{style_name}.css',
                'path': f'templates/{style_name}.css',
                'type': 'stylesheet'
            }
        ]
        
        return style_templates
    
    def validate_assets(self, asset_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate asset compatibility and integrity
        
        Args:
            asset_config: Asset configuration to validate
            
        Returns:
            Dictionary containing validation results
        """
        validation_result = {
            'valid': True,
            'errors': [],
            'warnings': [],
            'asset_checks': {},
            'timestamp': self._get_timestamp()
        }
        
        # Validate fonts
        if 'fonts' in asset_config:
            font_validation = self._validate_fonts(asset_config['fonts'])
            validation_result['asset_checks']['fonts'] = font_validation
            if not font_validation['valid']:
                validation_result['valid'] = False
                validation_result['errors'].extend(font_validation['errors'])
        
        # Validate color schemes
        if 'color_schemes' in asset_config:
            color_validation = self._validate_color_schemes(asset_config['color_schemes'])
            validation_result['asset_checks']['color_schemes'] = color_validation
            if not color_validation['valid']:
                validation_result['valid'] = False
                validation_result['errors'].extend(color_validation['errors'])
        
        # Validate templates
        if 'templates' in asset_config:
            template_validation = self._validate_templates(asset_config['templates'])
            validation_result['asset_checks']['templates'] = template_validation
            if not template_validation['valid']:
                validation_result['valid'] = False
                validation_result['errors'].extend(template_validation['errors'])
        
        # Check asset compatibility
        compatibility_check = self._check_asset_compatibility(asset_config)
        validation_result['compatibility'] = compatibility_check
        if compatibility_check['warnings']:
            validation_result['warnings'].extend(compatibility_check['warnings'])
        
        return validation_result
    
    def _validate_fonts(self, fonts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate font assets"""
        validation = {
            'valid': True,
            'errors': [],
            'checked_fonts': []
        }
        
        for font in fonts:
            font_check = {
                'name': font.get('name', 'Unknown'),
                'exists': False,
                'valid_format': False,
                'size': 0
            }
            
            if 'path' in font and os.path.exists(font['path']):
                font_check['exists'] = True
                font_check['size'] = os.path.getsize(font['path'])
                
                # Check file format
                if font['path'].lower().endswith(('.ttf', '.otf', '.woff', '.woff2')):
                    font_check['valid_format'] = True
                else:
                    validation['errors'].append(f"Invalid font format: {font['path']}")
                    validation['valid'] = False
            else:
                validation['errors'].append(f"Font file not found: {font.get('path', 'No path specified')}")
                validation['valid'] = False
            
            validation['checked_fonts'].append(font_check)
        
        return validation
    
    def _validate_color_schemes(self, color_schemes: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate color scheme assets"""
        validation = {
            'valid': True,
            'errors': [],
            'checked_schemes': []
        }
        
        for scheme in color_schemes:
            scheme_check = {
                'name': scheme.get('name', 'Unknown'),
                'exists': False,
                'valid_json': False,
                'color_count': 0
            }
            
            if 'path' in scheme and os.path.exists(scheme['path']):
                scheme_check['exists'] = True
                
                try:
                    with open(scheme['path'], 'r') as f:
                        scheme_data = json.load(f)
                        scheme_check['valid_json'] = True
                        scheme_check['color_count'] = len(scheme_data.get('colors', {}))
                except json.JSONDecodeError:
                    validation['errors'].append(f"Invalid JSON in color scheme: {scheme['path']}")
                    validation['valid'] = False
            else:
                validation['errors'].append(f"Color scheme file not found: {scheme.get('path', 'No path specified')}")
                validation['valid'] = False
            
            validation['checked_schemes'].append(scheme_check)
        
        return validation
    
    def _validate_templates(self, templates: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Validate template assets"""
        validation = {
            'valid': True,
            'errors': [],
            'checked_templates': []
        }
        
        for template in templates:
            template_check = {
                'name': template.get('name', 'Unknown'),
                'exists': False,
                'valid_format': False,
                'size': 0
            }
            
            if 'path' in template and os.path.exists(template['path']):
                template_check['exists'] = True
                template_check['size'] = os.path.getsize(template['path'])
                
                # Check file format
                if template['path'].lower().endswith(('.html', '.css', '.js', '.tex', '.md')):
                    template_check['valid_format'] = True
                else:
                    validation['errors'].append(f"Unknown template format: {template['path']}")
                    # Don't mark as invalid for unknown formats, just warn
            else:
                validation['errors'].append(f"Template file not found: {template.get('path', 'No path specified')}")
                validation['valid'] = False
            
            validation['checked_templates'].append(template_check)
        
        return validation
    
    def _check_asset_compatibility(self, asset_config: Dict[str, Any]) -> Dict[str, Any]:
        """Check compatibility between different assets"""
        compatibility = {
            'compatible': True,
            'warnings': [],
            'recommendations': []
        }
        
        # Check font and color scheme compatibility
        if 'fonts' in asset_config and 'color_schemes' in asset_config:
            # Example compatibility check
            serif_fonts = [f for f in asset_config['fonts'] if f.get('type') == 'serif']
            if serif_fonts and asset_config.get('style') == 'modern':
                compatibility['warnings'].append(
                    'Serif fonts may not be optimal for modern style designs'
                )
                compatibility['recommendations'].append(
                    'Consider using sans-serif fonts for modern designs'
                )
        
        return compatibility
    
    def sync_with_services(self, sync_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sync assets with other services in the ecosystem
        
        Args:
            sync_config: Synchronization configuration
            
        Returns:
            Dictionary containing sync results
        """
        target_services = sync_config.get('target_services', [])
        sync_type = sync_config.get('sync_type', 'push')  # push, pull, or bidirectional
        
        sync_result = {
            'success': True,
            'synced_services': [],
            'failed_services': [],
            'sync_summary': {},
            'timestamp': self._get_timestamp()
        }
        
        for service in target_services:
            try:
                service_sync_result = self._sync_with_service(service, sync_type)
                
                if service_sync_result['success']:
                    sync_result['synced_services'].append(service)
                else:
                    sync_result['failed_services'].append({
                        'service': service,
                        'error': service_sync_result.get('error', 'Unknown error')
                    })
            
            except Exception as e:
                sync_result['failed_services'].append({
                    'service': service,
                    'error': str(e)
                })
        
        # Update sync summary
        sync_result['sync_summary'] = {
            'total_services': len(target_services),
            'successful_syncs': len(sync_result['synced_services']),
            'failed_syncs': len(sync_result['failed_services']),
            'success_rate': len(sync_result['synced_services']) / len(target_services) if target_services else 0
        }
        
        if sync_result['failed_services']:
            sync_result['success'] = False
        
        return sync_result
    
    def _sync_with_service(self, service: str, sync_type: str) -> Dict[str, Any]:
        """Sync with individual service"""
        # Mock implementation - would make actual service calls
        service_urls = {
            'styles_gallery': 'http://localhost:5000',
            'publication_style_config_server': 'http://localhost:5002',
            'distance_server': 'http://localhost:5001'
        }
        
        if service not in service_urls:
            return {
                'success': False,
                'error': f'Unknown service: {service}'
            }
        
        # Mock successful sync
        return {
            'success': True,
            'service': service,
            'sync_type': sync_type,
            'assets_synced': 15,
            'timestamp': self._get_timestamp()
        }
    
    def _generate_bundle_id(self, bundle_name: str, style_name: str) -> str:
        """Generate unique bundle ID"""
        base_string = f"{bundle_name}_{style_name}_{self._get_timestamp()}"
        return hashlib.md5(base_string.encode()).hexdigest()[:12]
    
    def _calculate_file_checksum(self, file_path: str) -> str:
        """Calculate file checksum"""
        hash_md5 = hashlib.md5()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()