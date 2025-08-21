import json
import os
from django.conf import settings

def get_static_files():
    manifest_path = os.path.join(settings.REACT_APP_DIR, 'build', 'asset-manifest.json')
    try:
        with open(manifest_path, 'r') as f:
            manifest = json.load(f)
        js = manifest['files'].get('main.js', '')
        css = manifest['files'].get('main.css', '')
        print("JS file:", js)   # → должно быть: /static/js/main.abc123.js
        print("CSS file:", css)
        return {'js': js, 'css': css}
    except Exception as e:
        print("Error:", e)
        return {'js': '', 'css': ''}