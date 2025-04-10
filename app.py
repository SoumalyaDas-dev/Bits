# Main Flask application for AI-Powered Local Business Booster

from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session, flash
import os
import json
import uuid
import datetime
from werkzeug.utils import secure_filename
import requests

# Import configuration
import config

# Import core modules
from modules.business_processor import BusinessProcessor
from modules.content_generator import ContentGenerator
from modules.image_service import ImageService
from modules.file_storage import FileStorage
from modules.export_service import ExportService

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = config.SECRET_KEY
app.config['UPLOAD_FOLDER'] = config.UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = config.MAX_CONTENT_LENGTH

# Create upload folder if it doesn't exist
if not os.path.exists(config.UPLOAD_FOLDER):
    os.makedirs(config.UPLOAD_FOLDER)

# Initialize services
business_processor = BusinessProcessor()
content_generator = ContentGenerator(
    api_key=config.GEMMA_API_KEY
)
image_service = ImageService(
    stability_api_key=config.STABILITY_AI_API_KEY,
    bria_api_key=config.BRIA_API_KEY,
    unsplash_api_key=config.UNSPLASH_API_KEY,
    unsplash_secret_key=config.UNSPLASH_SECRET_KEY
)
file_storage = FileStorage(api_key=config.TINYCLOUD_API_KEY)
export_service = ExportService()

# Helper function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in config.ALLOWED_EXTENSIONS

# Routes
@app.route('/')
def index():
    return render_template('index.html', 
                           business_types=config.BUSINESS_TYPES,
                           style_preferences=config.STYLE_PREFERENCES)

@app.route('/generate', methods=['POST'])
def generate_content():
    try:
        # Process form data
        business_data = {
            'name': request.form.get('business_name'),
            'type': request.form.get('business_type'),
            'description': request.form.get('business_description'),
            'location': request.form.get('business_location'),
            'target_audience': request.form.get('target_audience'),
            'style_preference': request.form.get('style_preference')
        }

        # Validate required fields
        for field, value in business_data.items():
            if not value:
                flash(f"Please fill in the {field.replace('_', ' ')} field.", "error")
                return redirect(url_for('index'))
        
        # Process business data
        processed_data = business_processor.process(business_data)
        
        # Generate content using DeepSeek API
        content = content_generator.generate(processed_data)
        
        # Store content in session immediately
        session['generated_content'] = content
        session['business_data'] = business_data
        
        # Get relevant images after content is generated
        try:
            images = image_service.get_images(business_data['type'], business_data['style_preference'])
            session['images'] = images
        except Exception as e:
            print(f"Error fetching images: {e}")
            # Provide empty images list if image fetching fails
            session['images'] = []
        
        # Redirect to results page
        return redirect(url_for('results'))
    except Exception as e:
        print(f"Error generating content: {e}")
        # Flash an error message
        flash(f"An error occurred while generating content. Please try again.", "error")
        return redirect(url_for('index'))

@app.route('/results')
def results():
    # Get data from session
    content = session.get('generated_content', {})
    images = session.get('images', [])
    business_data = session.get('business_data', {})
    
    # Ensure content has the expected structure
    if not content:
        content = {
            'description': {'short': '', 'medium': '', 'long': ''},
            'email': {'welcome': {'subject': '', 'body': ''}, 'promotional': {'subject': '', 'body': ''}, 'newsletter': {'subject': '', 'body': ''}},
            'social_media': []
        }
    elif not isinstance(content.get('description'), dict):
        content['description'] = {'short': '', 'medium': '', 'long': ''}
    
    return render_template('results.html', 
                           content=content, 
                           images=images, 
                           business_data=business_data)

@app.route('/export/<content_type>')
def export(content_type):
    content = session.get('generated_content', {})
    business_data = session.get('business_data', {})
    images = session.get('images', [])
    
    if content_type == 'email':
        file_path = export_service.create_email_template(content['email'], business_data)
        return send_file(file_path, as_attachment=True, download_name=f"{business_data['name']}_email.html")
    
    elif content_type == 'social':
        file_path = export_service.create_social_post(content['social_media'], business_data, images[0] if images else None)
        return send_file(file_path, as_attachment=True, download_name=f"{business_data['name']}_social_post.png")
    
    elif content_type == 'description':
        file_path = export_service.create_business_description(content['description'], business_data)
        return send_file(file_path, as_attachment=True, download_name=f"{business_data['name']}_description.txt")
    
    return redirect(url_for('results'))

@app.route('/api/content', methods=['GET'])
def get_content():
    content_type = request.args.get('type')
    content = session.get('generated_content', {})
    
    if content_type in content:
        return jsonify({'content': content[content_type]})
    
    return jsonify({'error': 'Content type not found'}), 404

@app.route('/api/images', methods=['GET'])
def get_images():
    images = session.get('images', [])
    return jsonify({'images': images})

# Error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

if __name__ == '__main__':
    app.run(debug=config.DEBUG)