"""
Style Assets Server
Asset management service for fonts, color schemes, and templates
Version: 20250602_000000_0_0_0_001
"""

from flask import Flask, request, jsonify, send_file, render_template
from services.asset_manager import AssetManager
from services.font_service import FontService
from services.color_scheme_service import ColorSchemeService
from services.template_service import TemplateService
import logging
import os

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

asset_manager = AssetManager()
font_service = FontService()
color_scheme_service = ColorSchemeService()
template_service = TemplateService()

@app.route('/')
def index():
    """Main interface for style assets"""
    return jsonify({
        'service': 'style-assets',
        'version': '20250602_000000_0_0_0_001',
        'endpoints': {
            'fonts': '/api/fonts',
            'color_schemes': '/api/color-schemes',
            'templates': '/api/templates',
            'assets': '/api/assets'
        }
    })

@app.route('/api/fonts', methods=['GET'])
def get_fonts():
    """Get available fonts"""
    try:
        fonts = font_service.get_available_fonts()
        return jsonify(fonts)
    except Exception as e:
        app.logger.error(f"Error getting fonts: {str(e)}")
        return jsonify({'error': 'Failed to retrieve fonts'}), 500

@app.route('/api/fonts/<font_name>', methods=['GET'])
def get_font_details(font_name):
    """Get details for specific font"""
    try:
        font_details = font_service.get_font_details(font_name)
        if font_details:
            return jsonify(font_details)
        else:
            return jsonify({'error': 'Font not found'}), 404
    except Exception as e:
        app.logger.error(f"Error getting font details: {str(e)}")
        return jsonify({'error': 'Failed to retrieve font details'}), 500

@app.route('/api/fonts/<font_name>/download', methods=['GET'])
def download_font(font_name):
    """Download font file"""
    try:
        font_path = font_service.get_font_path(font_name)
        if font_path and os.path.exists(font_path):
            return send_file(font_path, as_attachment=True)
        else:
            return jsonify({'error': 'Font file not found'}), 404
    except Exception as e:
        app.logger.error(f"Error downloading font: {str(e)}")
        return jsonify({'error': 'Failed to download font'}), 500

@app.route('/api/color-schemes', methods=['GET'])
def get_color_schemes():
    """Get available color schemes"""
    try:
        schemes = color_scheme_service.get_available_schemes()
        return jsonify(schemes)
    except Exception as e:
        app.logger.error(f"Error getting color schemes: {str(e)}")
        return jsonify({'error': 'Failed to retrieve color schemes'}), 500

@app.route('/api/color-schemes/<scheme_name>', methods=['GET'])
def get_color_scheme(scheme_name):
    """Get specific color scheme"""
    try:
        scheme = color_scheme_service.get_scheme(scheme_name)
        if scheme:
            return jsonify(scheme)
        else:
            return jsonify({'error': 'Color scheme not found'}), 404
    except Exception as e:
        app.logger.error(f"Error getting color scheme: {str(e)}")
        return jsonify({'error': 'Failed to retrieve color scheme'}), 500

@app.route('/api/color-schemes', methods=['POST'])
def create_color_scheme():
    """Create new color scheme"""
    try:
        scheme_data = request.get_json()
        result = color_scheme_service.create_scheme(scheme_data)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error creating color scheme: {str(e)}")
        return jsonify({'error': 'Failed to create color scheme'}), 500

@app.route('/api/templates', methods=['GET'])
def get_templates():
    """Get available templates"""
    try:
        templates = template_service.get_available_templates()
        return jsonify(templates)
    except Exception as e:
        app.logger.error(f"Error getting templates: {str(e)}")
        return jsonify({'error': 'Failed to retrieve templates'}), 500

@app.route('/api/templates/<template_name>', methods=['GET'])
def get_template(template_name):
    """Get specific template"""
    try:
        template = template_service.get_template(template_name)
        if template:
            return jsonify(template)
        else:
            return jsonify({'error': 'Template not found'}), 404
    except Exception as e:
        app.logger.error(f"Error getting template: {str(e)}")
        return jsonify({'error': 'Failed to retrieve template'}), 500

@app.route('/api/templates/<template_name>/download', methods=['GET'])
def download_template(template_name):
    """Download template file"""
    try:
        template_path = template_service.get_template_path(template_name)
        if template_path and os.path.exists(template_path):
            return send_file(template_path, as_attachment=True)
        else:
            return jsonify({'error': 'Template file not found'}), 404
    except Exception as e:
        app.logger.error(f"Error downloading template: {str(e)}")
        return jsonify({'error': 'Failed to download template'}), 500

@app.route('/api/assets/bundle', methods=['POST'])
def create_asset_bundle():
    """Create asset bundle for specific style"""
    try:
        bundle_config = request.get_json()
        result = asset_manager.create_bundle(bundle_config)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error creating asset bundle: {str(e)}")
        return jsonify({'error': 'Failed to create asset bundle'}), 500

@app.route('/api/assets/validate', methods=['POST'])
def validate_assets():
    """Validate asset compatibility"""
    try:
        asset_config = request.get_json()
        result = asset_manager.validate_assets(asset_config)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error validating assets: {str(e)}")
        return jsonify({'error': 'Failed to validate assets'}), 500

@app.route('/api/assets/sync', methods=['POST'])
def sync_assets():
    """Sync assets with other services"""
    try:
        sync_config = request.get_json()
        result = asset_manager.sync_with_services(sync_config)
        return jsonify(result)
    except Exception as e:
        app.logger.error(f"Error syncing assets: {str(e)}")
        return jsonify({'error': 'Failed to sync assets'}), 500

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'service': 'style-assets'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5003)