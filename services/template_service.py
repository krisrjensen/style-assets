"""
Template Service
Manages template assets for different publication styles
"""

import os
import json
from typing import Dict, List, Any, Optional
from datetime import datetime

class TemplateService:
    """Service for managing template assets"""
    
    def __init__(self):
        self.templates_directory = 'templates'
        self._ensure_templates_directory()
        self.template_registry = self._initialize_template_registry()
        self._create_default_templates()
    
    def _ensure_templates_directory(self):
        """Ensure templates directory exists"""
        os.makedirs(self.templates_directory, exist_ok=True)
    
    def _initialize_template_registry(self) -> Dict[str, Any]:
        """Initialize template registry"""
        return {
            'templates': {},
            'categories': {
                'html': [],
                'css': [],
                'latex': [],
                'markdown': []
            },
            'metadata': {
                'last_updated': self._get_timestamp(),
                'total_templates': 0
            }
        }
    
    def _create_default_templates(self):
        """Create default templates"""
        templates_data = [
            {
                'name': 'IEEE Article HTML',
                'category': 'html',
                'description': 'HTML template for IEEE style articles',
                'file_extension': 'html',
                'content': self._get_ieee_html_template(),
                'style_compatibility': ['ieee'],
                'variables': ['title', 'authors', 'abstract', 'content'],
                'features': ['two_column', 'citations', 'figures']
            },
            {
                'name': 'Nature Article HTML',
                'category': 'html',
                'description': 'HTML template for Nature style articles',
                'file_extension': 'html',
                'content': self._get_nature_html_template(),
                'style_compatibility': ['nature'],
                'variables': ['title', 'authors', 'abstract', 'content'],
                'features': ['single_column', 'large_figures', 'author_affiliations']
            },
            {
                'name': 'IEEE CSS Stylesheet',
                'category': 'css',
                'description': 'CSS stylesheet for IEEE formatting',
                'file_extension': 'css',
                'content': self._get_ieee_css_template(),
                'style_compatibility': ['ieee'],
                'variables': ['primary_color', 'font_family', 'font_size'],
                'features': ['two_column_layout', 'academic_styling']
            },
            {
                'name': 'Modern CSS Framework',
                'category': 'css',
                'description': 'Modern CSS framework for publications',
                'file_extension': 'css',
                'content': self._get_modern_css_template(),
                'style_compatibility': ['modern', 'web'],
                'variables': ['color_scheme', 'typography', 'spacing'],
                'features': ['responsive', 'dark_mode', 'accessibility']
            },
            {
                'name': 'LaTeX IEEE Template',
                'category': 'latex',
                'description': 'LaTeX template for IEEE conferences',
                'file_extension': 'tex',
                'content': self._get_latex_ieee_template(),
                'style_compatibility': ['ieee'],
                'variables': ['title', 'authors', 'abstract', 'keywords'],
                'features': ['ieee_format', 'bibliography', 'figures']
            },
            {
                'name': 'Markdown Academic',
                'category': 'markdown',
                'description': 'Markdown template for academic papers',
                'file_extension': 'md',
                'content': self._get_markdown_template(),
                'style_compatibility': ['academic', 'github'],
                'variables': ['title', 'authors', 'date', 'abstract'],
                'features': ['pandoc_compatible', 'citations', 'tables']
            }
        ]
        
        for template_data in templates_data:
            self._save_template_to_file(template_data)
            template_id = self._generate_template_id(template_data['name'])
            
            self.template_registry['templates'][template_id] = {
                **template_data,
                'id': template_id,
                'created': self._get_timestamp(),
                'status': 'active',
                'usage_count': 0
            }
            
            # Add to category
            category = template_data['category']
            if category in self.template_registry['categories']:
                self.template_registry['categories'][category].append(template_id)
        
        # Update metadata
        self.template_registry['metadata']['total_templates'] = len(self.template_registry['templates'])
        self.template_registry['metadata']['last_updated'] = self._get_timestamp()
    
    def _get_ieee_html_template(self) -> str:
        """Get IEEE HTML template content"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="ieee.css">
</head>
<body>
    <div class="ieee-paper">
        <header class="paper-header">
            <h1 class="paper-title">{{title}}</h1>
            <div class="authors">{{authors}}</div>
        </header>
        
        <div class="two-column">
            <section class="abstract">
                <h2>Abstract</h2>
                <p>{{abstract}}</p>
                <div class="keywords">
                    <strong>Index Terms—</strong>{{keywords}}
                </div>
            </section>
            
            <main class="content">
                {{content}}
            </main>
        </div>
        
        <footer class="references">
            <h2>References</h2>
            <div class="reference-list">
                {{references}}
            </div>
        </footer>
    </div>
</body>
</html>'''
    
    def _get_nature_html_template(self) -> str:
        """Get Nature HTML template content"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{title}}</title>
    <link rel="stylesheet" href="nature.css">
</head>
<body>
    <article class="nature-article">
        <header>
            <h1>{{title}}</h1>
            <div class="author-info">
                <div class="authors">{{authors}}</div>
                <div class="affiliations">{{affiliations}}</div>
            </div>
        </header>
        
        <section class="abstract">
            {{abstract}}
        </section>
        
        <main class="article-body">
            {{content}}
        </main>
        
        <section class="methods">
            <h2>Methods</h2>
            {{methods}}
        </section>
        
        <section class="references">
            <h2>References</h2>
            {{references}}
        </section>
    </article>
</body>
</html>'''
    
    def _get_ieee_css_template(self) -> str:
        """Get IEEE CSS template content"""
        return '''/* IEEE Conference Paper Style */

body {
    font-family: "Times New Roman", serif;
    font-size: 10pt;
    line-height: 1.2;
    margin: 0;
    padding: 0;
}

.ieee-paper {
    max-width: 8.5in;
    margin: 0 auto;
    padding: 0.75in 0.625in 1in 0.625in;
}

.paper-title {
    font-size: 14pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 12pt;
    line-height: 1.2;
}

.authors {
    font-size: 12pt;
    text-align: center;
    margin-bottom: 6pt;
}

.two-column {
    column-count: 2;
    column-gap: 20pt;
    column-rule: none;
}

.abstract {
    font-size: 9pt;
    margin-bottom: 12pt;
    break-inside: avoid;
}

.abstract h2 {
    font-size: 9pt;
    font-weight: bold;
    margin: 0 0 6pt 0;
    text-align: left;
}

.keywords {
    margin-top: 6pt;
    font-size: 9pt;
    font-style: italic;
}

.content h1 {
    font-size: 10pt;
    font-weight: bold;
    margin: 12pt 0 6pt 0;
    text-transform: uppercase;
    text-align: center;
}

.content h2 {
    font-size: 10pt;
    font-weight: bold;
    margin: 6pt 0 3pt 0;
    text-align: left;
}

.content p {
    text-align: justify;
    margin: 0 0 6pt 0;
    text-indent: 12pt;
}

.references {
    break-before: column;
    font-size: 9pt;
}

.references h2 {
    font-size: 10pt;
    font-weight: bold;
    margin: 12pt 0 6pt 0;
    text-align: center;
}

.reference-list {
    text-align: left;
}

figure {
    text-align: center;
    margin: 6pt 0;
    break-inside: avoid;
}

figure img {
    max-width: 100%;
    height: auto;
}

figcaption {
    font-size: 9pt;
    margin-top: 3pt;
    text-align: center;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: 6pt 0;
    break-inside: avoid;
}

table caption {
    font-size: 9pt;
    font-weight: bold;
    text-align: center;
    margin-bottom: 3pt;
}

th, td {
    border: 1px solid #000;
    padding: 3pt;
    text-align: center;
    font-size: 8pt;
}

th {
    background-color: #f0f0f0;
    font-weight: bold;
}'''
    
    def _get_modern_css_template(self) -> str:
        """Get modern CSS template content"""
        return '''/* Modern Publication CSS Framework */

:root {
    --primary-color: #2c3e50;
    --secondary-color: #3498db;
    --accent-color: #e74c3c;
    --background-color: #ffffff;
    --text-color: #2c3e50;
    --border-color: #bdc3c7;
    --font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    --font-size-base: 16px;
    --line-height-base: 1.6;
    --spacing-unit: 1rem;
}

* {
    box-sizing: border-box;
}

body {
    font-family: var(--font-family);
    font-size: var(--font-size-base);
    line-height: var(--line-height-base);
    color: var(--text-color);
    background-color: var(--background-color);
    margin: 0;
    padding: 0;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 0 var(--spacing-unit);
}

h1, h2, h3, h4, h5, h6 {
    color: var(--primary-color);
    margin: calc(var(--spacing-unit) * 1.5) 0 var(--spacing-unit) 0;
    line-height: 1.3;
}

h1 { font-size: 2.5rem; }
h2 { font-size: 2rem; }
h3 { font-size: 1.5rem; }
h4 { font-size: 1.25rem; }
h5 { font-size: 1.125rem; }
h6 { font-size: 1rem; }

p {
    margin: 0 0 var(--spacing-unit) 0;
    text-align: justify;
}

a {
    color: var(--secondary-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.abstract {
    background-color: #f8f9fa;
    padding: var(--spacing-unit);
    border-left: 4px solid var(--secondary-color);
    margin: calc(var(--spacing-unit) * 2) 0;
}

.two-column {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: calc(var(--spacing-unit) * 2);
}

@media (max-width: 768px) {
    .two-column {
        grid-template-columns: 1fr;
    }
}

figure {
    margin: calc(var(--spacing-unit) * 2) 0;
    text-align: center;
}

figure img {
    max-width: 100%;
    height: auto;
    border-radius: 8px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

figcaption {
    margin-top: var(--spacing-unit);
    font-size: 0.9rem;
    color: #6c757d;
    font-style: italic;
}

table {
    width: 100%;
    border-collapse: collapse;
    margin: calc(var(--spacing-unit) * 2) 0;
    background-color: white;
    border-radius: 8px;
    overflow: hidden;
    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

th, td {
    padding: 0.75rem;
    text-align: left;
    border-bottom: 1px solid var(--border-color);
}

th {
    background-color: var(--primary-color);
    color: white;
    font-weight: 600;
}

.citation {
    font-size: 0.9rem;
    color: var(--secondary-color);
    cursor: pointer;
}

.citation:hover {
    background-color: #e3f2fd;
}

/* Dark mode support */
@media (prefers-color-scheme: dark) {
    :root {
        --background-color: #1a1a1a;
        --text-color: #e0e0e0;
        --primary-color: #4fc3f7;
        --border-color: #404040;
    }
    
    .abstract {
        background-color: #2a2a2a;
    }
    
    table {
        background-color: #2a2a2a;
    }
    
    th {
        background-color: var(--primary-color);
        color: #1a1a1a;
    }
}

/* Print styles */
@media print {
    body {
        font-size: 12pt;
        line-height: 1.4;
    }
    
    .container {
        max-width: none;
        padding: 0;
    }
    
    .two-column {
        display: block;
        columns: 2;
        column-gap: 1in;
    }
    
    h1, h2, h3 {
        break-after: avoid;
    }
    
    figure, table {
        break-inside: avoid;
    }
}'''
    
    def _get_latex_ieee_template(self) -> str:
        """Get LaTeX IEEE template content"""
        return '''\\documentclass[conference]{IEEEtran}
\\usepackage{cite}
\\usepackage{amsmath,amssymb,amsfonts}
\\usepackage{algorithmic}
\\usepackage{graphicx}
\\usepackage{textcomp}
\\usepackage{xcolor}

\\begin{document}

\\title{{{title}}}

\\author{
\\IEEEauthorblockN{{{authors}}}
\\IEEEauthorblockA{{{affiliations}}}
}

\\maketitle

\\begin{abstract}
{{abstract}}
\\end{abstract}

\\begin{IEEEkeywords}
{{keywords}}
\\end{IEEEkeywords}

\\section{Introduction}
{{introduction}}

\\section{Methodology}
{{methodology}}

\\section{Results}
{{results}}

\\section{Conclusion}
{{conclusion}}

\\section*{Acknowledgment}
{{acknowledgment}}

\\begin{thebibliography}{1}
{{references}}
\\end{thebibliography}

\\end{document}'''
    
    def _get_markdown_template(self) -> str:
        """Get Markdown template content"""
        return '''---
title: "{{title}}"
authors: {{authors}}
date: {{date}}
abstract: |
  {{abstract}}
keywords: [{{keywords}}]
bibliography: references.bib
---

# Abstract

{{abstract}}

# Introduction

{{introduction}}

# Methodology

{{methodology}}

# Results

{{results}}

# Discussion

{{discussion}}

# Conclusion

{{conclusion}}

# References

{{references}}'''
    
    def _save_template_to_file(self, template_data: Dict[str, Any]):
        """Save template to file"""
        filename = f"{template_data['name'].lower().replace(' ', '_')}.{template_data['file_extension']}"
        file_path = os.path.join(self.templates_directory, filename)
        
        with open(file_path, 'w') as f:
            f.write(template_data['content'])
    
    def get_available_templates(self) -> Dict[str, Any]:
        """Get list of available templates"""
        templates_list = []
        
        for template_id, template_info in self.template_registry['templates'].items():
            templates_list.append({
                'id': template_id,
                'name': template_info['name'],
                'category': template_info['category'],
                'description': template_info['description'],
                'file_extension': template_info['file_extension'],
                'style_compatibility': template_info['style_compatibility'],
                'features': template_info['features'],
                'status': template_info['status']
            })
        
        return {
            'templates': templates_list,
            'categories': {
                category: len(template_ids) 
                for category, template_ids in self.template_registry['categories'].items()
            },
            'total_templates': len(templates_list),
            'metadata': {
                'timestamp': self._get_timestamp(),
                'service': 'template_service'
            }
        }
    
    def get_template(self, template_name: str) -> Optional[Dict[str, Any]]:
        """Get specific template"""
        template_id = self._generate_template_id(template_name)
        
        if template_id in self.template_registry['templates']:
            template_info = self.template_registry['templates'][template_id].copy()
            
            # Update usage count
            self.template_registry['templates'][template_id]['usage_count'] += 1
            
            # Add metadata
            template_info['metadata'] = {
                'last_accessed': self._get_timestamp(),
                'download_url': f'/api/templates/{template_name}/download',
                'preview_url': f'/api/templates/{template_name}/preview'
            }
            
            return template_info
        
        return None
    
    def get_template_path(self, template_name: str) -> Optional[str]:
        """Get file path for template"""
        template_id = self._generate_template_id(template_name)
        
        if template_id in self.template_registry['templates']:
            template_info = self.template_registry['templates'][template_id]
            filename = f"{template_name.lower().replace(' ', '_')}.{template_info['file_extension']}"
            file_path = os.path.join(self.templates_directory, filename)
            
            if os.path.exists(file_path):
                return file_path
            else:
                # Create placeholder if file doesn't exist
                return self._create_template_placeholder(template_name, template_info)
        
        return None
    
    def get_templates_by_category(self, category: str) -> Dict[str, Any]:
        """Get templates by category"""
        if category not in self.template_registry['categories']:
            return {
                'error': f'Unknown category: {category}',
                'available_categories': list(self.template_registry['categories'].keys())
            }
        
        template_ids = self.template_registry['categories'][category]
        templates = []
        
        for template_id in template_ids:
            if template_id in self.template_registry['templates']:
                template_info = self.template_registry['templates'][template_id]
                templates.append({
                    'id': template_id,
                    'name': template_info['name'],
                    'description': template_info['description'],
                    'file_extension': template_info['file_extension'],
                    'style_compatibility': template_info['style_compatibility'],
                    'features': template_info['features']
                })
        
        return {
            'category': category,
            'templates': templates,
            'count': len(templates),
            'timestamp': self._get_timestamp()
        }
    
    def get_templates_by_style(self, style_name: str) -> Dict[str, Any]:
        """Get templates compatible with specific style"""
        compatible_templates = []
        
        for template_id, template_info in self.template_registry['templates'].items():
            if style_name in template_info.get('style_compatibility', []):
                compatible_templates.append({
                    'id': template_id,
                    'name': template_info['name'],
                    'category': template_info['category'],
                    'description': template_info['description'],
                    'file_extension': template_info['file_extension'],
                    'features': template_info['features']
                })
        
        return {
            'style': style_name,
            'compatible_templates': compatible_templates,
            'count': len(compatible_templates),
            'timestamp': self._get_timestamp()
        }
    
    def _create_template_placeholder(self, template_name: str, template_info: Dict[str, Any]) -> str:
        """Create placeholder template file"""
        placeholder_content = f"""
Template: {template_name}
Category: {template_info['category']}
Description: {template_info['description']}
Created: {self._get_timestamp()}

This is a placeholder for the {template_name} template.
The actual template content should be placed here.

Variables: {', '.join(template_info.get('variables', []))}
Features: {', '.join(template_info.get('features', []))}
"""
        
        filename = f"{template_name.lower().replace(' ', '_')}_placeholder.{template_info['file_extension']}"
        placeholder_path = os.path.join(self.templates_directory, filename)
        
        with open(placeholder_path, 'w') as f:
            f.write(placeholder_content)
        
        return placeholder_path
    
    def get_template_usage_stats(self) -> Dict[str, Any]:
        """Get template usage statistics"""
        stats = {
            'total_templates': len(self.template_registry['templates']),
            'category_breakdown': {},
            'most_used': [],
            'format_breakdown': {},
            'total_usage': 0
        }
        
        # Category breakdown
        for category, template_ids in self.template_registry['categories'].items():
            stats['category_breakdown'][category] = len(template_ids)
        
        # Most used templates
        templates_by_usage = sorted(
            self.template_registry['templates'].items(),
            key=lambda x: x[1]['usage_count'],
            reverse=True
        )
        
        stats['most_used'] = [
            {
                'name': template_info['name'],
                'usage_count': template_info['usage_count']
            }
            for template_id, template_info in templates_by_usage[:5]
        ]
        
        # Format breakdown and total usage
        format_counts = {}
        for template_info in self.template_registry['templates'].values():
            file_ext = template_info.get('file_extension', 'unknown')
            format_counts[file_ext] = format_counts.get(file_ext, 0) + 1
            stats['total_usage'] += template_info['usage_count']
        
        stats['format_breakdown'] = format_counts
        stats['timestamp'] = self._get_timestamp()
        
        return stats
    
    def _generate_template_id(self, template_name: str) -> str:
        """Generate unique template ID"""
        return template_name.lower().replace(' ', '_').replace('-', '_')
    
    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        return datetime.now().isoformat()