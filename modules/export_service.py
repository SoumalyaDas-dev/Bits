# Export Service Module

import os
import io
from datetime import datetime
from PIL import Image, ImageDraw, ImageFont
import requests
from fpdf import FPDF
import textwrap

class ExportService:
    """
    Handles exporting generated content to various file formats.
    """
    
    def __init__(self):
        """
        Initialize the ExportService.
        """
        self.export_dir = "exports"
        
        # Create export directory if it doesn't exist
        if not os.path.exists(self.export_dir):
            os.makedirs(self.export_dir)
    
    
    def create_email_template(self, email_content, business_data):
        """
        Create an HTML email template.
        
        Args:
            email_content (dict): Generated email content
            business_data (dict): Business information
            
        Returns:
            str: Path to the created HTML file
        """
        # Determine which email template to use
        email_type = list(email_content.keys())[0] if email_content else "welcome"
        email_data = email_content.get(email_type, {})
        
        # Create HTML content
        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>{business_data['name']} - {email_type.capitalize()} Email</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    line-height: 1.6;
                    color: #333;
                    max-width: 600px;
                    margin: 0 auto;
                    padding: 20px;
                }}
                .header {{
                    text-align: center;
                    padding-bottom: 20px;
                    border-bottom: 1px solid #eee;
                }}
                .content {{
                    padding: 20px 0;
                }}
                .footer {{
                    text-align: center;
                    padding-top: 20px;
                    border-top: 1px solid #eee;
                    font-size: 12px;
                    color: #777;
                }}
                .cta {{
                    display: inline-block;
                    background-color: #4CAF50;
                    color: white;
                    padding: 10px 20px;
                    text-decoration: none;
                    border-radius: 5px;
                    margin: 20px 0;
                }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>{business_data['name']}</h1>
                <p>{business_data['type']} in {business_data['location']}</p>
            </div>
            
            <div class="content">
                <p>{email_data.get('greeting', 'Hello,')}</p>
                
                <div class="email-body">
                    {email_data.get('body', '')}
                </div>
                
                <a href="#" class="cta">{email_data.get('cta', 'Learn More')}</a>
            </div>
            
            <div class="footer">
                <p>{email_data.get('sign_off', 'Best regards,')}<br>
                {business_data['name']} Team</p>
                <p>© {datetime.now().year} {business_data['name']}. All rights reserved.</p>
                <p>You are receiving this email because you signed up for updates from {business_data['name']}.</p>
            </div>
        </body>
        </html>
        """
        
        # Generate filename and save
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{business_data['name'].replace(' ', '_')}_{timestamp}_{email_type}_email.html"
        file_path = os.path.join(self.export_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(html)
        
        return file_path
    
    def create_social_post(self, social_content, business_data, image_url=None):
        """
        Create a social media post image with text overlay.
        
        Args:
            social_content (dict): Generated social media content
            business_data (dict): Business information
            image_url (str, optional): URL of an image to use as background
            
        Returns:
            str: Path to the created image file
        """
        # Determine which social platform to use
        platform = list(social_content.keys())[0] if social_content else "instagram"
        post_text = social_content.get(platform, "")
        
        # Create image
        width, height = 1080, 1080  # Instagram size
        
        # Start with a background image if provided, otherwise create a blank one
        if image_url:
            try:
                # Download image
                response = requests.get(image_url)
                if response.status_code == 200:
                    img = Image.open(io.BytesIO(response.content))
                    
                    # Resize and crop to square
                    img_ratio = img.width / img.height
                    if img_ratio > 1:
                        # Image is wider than tall
                        new_width = int(height * img_ratio)
                        img = img.resize((new_width, height), Image.LANCZOS)
                        left = (new_width - width) // 2
                        img = img.crop((left, 0, left + width, height))
                    else:
                        # Image is taller than wide
                        new_height = int(width / img_ratio)
                        img = img.resize((width, new_height), Image.LANCZOS)
                        top = (new_height - height) // 2
                        img = img.crop((0, top, width, top + height))
            except Exception as e:
                print(f"Error processing image for social post: {e}")
                # Create a blank image if there's an error
                img = Image.new('RGB', (width, height), color=(240, 240, 240))
        else:
            # Create a blank image with a gradient background
            img = Image.new('RGB', (width, height), color=(240, 240, 240))
            draw = ImageDraw.Draw(img)
            for y in range(height):
                r = int(220 + (y / height) * 35)
                g = int(220 + (y / height) * 35)
                b = int(240 - (y / height) * 40)
                draw.line([(0, y), (width, y)], fill=(r, g, b))
        
        # Add semi-transparent overlay to make text more readable
        overlay = Image.new('RGBA', (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(overlay)
        draw.rectangle([(0, height//2), (width, height)], fill=(0, 0, 0, 128))
        img = Image.alpha_composite(img.convert('RGBA'), overlay).convert('RGB')
        
        # Add text
        draw = ImageDraw.Draw(img)
        
        # Try to load a font, fall back to default if not available
        try:
            title_font = ImageFont.truetype("Arial.ttf", 60)
            body_font = ImageFont.truetype("Arial.ttf", 40)
        except IOError:
            title_font = ImageFont.load_default()
            body_font = ImageFont.load_default()
        
        # Add business name at the top
        draw.text((width//2, 100), business_data['name'], fill=(255, 255, 255), font=title_font, anchor="mm")
        
        # Add post text in the middle
        # Wrap text to fit width
        if post_text:
            wrapped_text = textwrap.fill(post_text, width=30)
            lines = wrapped_text.split('\n')
            y_position = height//2
            for line in lines[:5]:  # Limit to 5 lines
                draw.text((width//2, y_position), line, fill=(255, 255, 255), font=body_font, anchor="mm")
                y_position += 50
        
        # Generate filename and save
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{business_data['name'].replace(' ', '_')}_{timestamp}_{platform}_post.png"
        file_path = os.path.join(self.export_dir, filename)
        img.save(file_path)
        
        return file_path
    
    def create_business_description(self, description_content, business_data):
        """
        Create a text file with the business description.
        
        Args:
            description_content (dict): Generated description content
            business_data (dict): Business information
            
        Returns:
            str: Path to the created text file
        """
        # Compile the content
        content = f"""{business_data['name']} - Business Description\n
{'-' * 50}\n
Business Type: {business_data['type']}\nLocation: {business_data['location']}\nTarget Audience: {business_data['target_audience']}\nStyle: {business_data['style_preference']}\n
{'-' * 50}\n
SHORT DESCRIPTION:\n{description_content.get('short', '')}\n\n
MEDIUM DESCRIPTION:\n{description_content.get('medium', '')}\n\n
LONG DESCRIPTION:\n{description_content.get('long', '')}\n\n
{'-' * 50}\n
Generated on {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n"""
        
        # Generate filename and save
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        filename = f"{business_data['name'].replace(' ', '_')}_{timestamp}_description.txt"
        file_path = os.path.join(self.export_dir, filename)
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
        return file_path