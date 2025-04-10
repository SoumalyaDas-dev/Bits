# AI-Powered Local Business Booster

A web application that helps small businesses generate professional marketing materials by simply entering basic information. This tool uses AI to create flyers, email templates, business descriptions, and social media posts tailored to the business's vibe and local trends.

## Features

- **Simple Business Information Form**: Collect business name, type, description, location, target audience, and style preferences
- **AI-Generated Content**: Professional business descriptions, flyer designs, email templates, and social media posts
- **Image Integration**: Relevant stock images based on business type and style preferences
- **Export Options**: Download generated content as PDFs, HTML, or images, with copy to clipboard functionality
- **Clean, Apple-Inspired Design**: Intuitive interface with responsive design for all devices

## Project Structure

- `app.py`: Main Flask application
- `config.py`: Configuration file with API keys and settings
- `modules/`: Core functionality modules
  - `business_processor.py`: Processes business information
  - `content_generator.py`: Generates content using AI APIs
  - `image_service.py`: Fetches relevant images
  - `file_storage.py`: Handles file storage
  - `export_service.py`: Creates downloadable files
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files

## Installation

1. Clone the repository or download the files

2. Install the required dependencies:

```bash
pip install -r requirements.txt
```

3. The API keys are already included in the `config.py` file:
   - Stability AI API (for image generation)
   - Bria2.3 API (for image generation)
   - Qwen2.5 API (for text generation)
   - Mistral AI API (for text generation)
   - TinyCloud API (for file storage)
   - Unsplash API (for fallback image retrieval)

## Running the Application

1. Start the Flask development server:

```bash
python app.py
```

2. Open your web browser and navigate to `http://127.0.0.1:5000`

3. Fill out the business information form and submit to generate content

4. View, copy, and download the generated marketing materials

## Technologies Used

- **Backend**: Flask (Python)
- **Frontend**: HTML, CSS, JavaScript
- **AI Content Generation**: DeepSeek API, Gemini API
- **Image Services**: Unsplash API, Pexels API
- **File Storage**: TinyCloud API
- **Export Formats**: PDF, HTML, PNG, TXT

## Project Created for Hackathon

This project was developed as part of a hackathon to demonstrate the power of AI in helping small businesses with their marketing needs.