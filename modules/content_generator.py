# Content Generator Module

import requests
import json
import random

class ContentGenerator:
    """
    Generates marketing content using Qwen2.5 and Mistral AI APIs.
    """
    
    def __init__(self, api_key=None):
        """
        Initialize the ContentGenerator with API key.
        
        Args:
            api_key (str): NVIDIA API key for Gemma model
        """
        self.api_key = api_key
        self.api_url = "https://integrate.api.nvidia.com/v1"
    
    def _make_api_request(self, prompt, request_type="content"):
        """Helper method to make API requests with error handling"""
        if not self.api_key:
            raise Exception("No valid API key provided for content generation.")

        try:
            from openai import OpenAI
            
            client = OpenAI(
                base_url=self.api_url,
                api_key=self.api_key
            )
            
            completion = client.chat.completions.create(
                model="google/gemma-3-1b-it",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.1,
                top_p=0.7,
                max_tokens=512,
                stream=True
            )
            
            # Collect the streamed response
            generated_text = ""
            for chunk in completion:
                if chunk.choices[0].delta.content is not None:
                    generated_text += chunk.choices[0].delta.content
            
            return generated_text
            
        except Exception as e:
            if "429" in str(e):
                raise Exception("API rate limit reached. Please try again later.")
            elif "401" in str(e):
                raise Exception("Invalid API key or authentication error.")
            elif "503" in str(e):
                raise Exception("API service is currently unavailable. Please try again later.")
            else:
                raise Exception(f"Failed to generate {request_type}: {str(e)}")

    def generate(self, business_data):
        """
        Generate marketing content based on business data.
        
        Args:
            business_data (dict): Processed business information
            
        Returns:
            dict: Generated content including business description, email templates,
                 and social media posts
        """
        try:
            # Generate different types of content
            description = self._generate_business_description(business_data)
            email = self._generate_email_templates(business_data)
            social_media = self._generate_social_media_posts(business_data)
            
            # Return all generated content
            return {
                "description": description,
                "email": email,
                "social_media": social_media
            }
        except Exception as e:
            print(f"Error in content generation: {str(e)}")
            # Return fallback content
            return {
                "description": {
                    "short": "Error generating content. Please try again.",
                    "medium": "We're experiencing technical difficulties with our content generation service.",
                    "long": "Our content generation service is temporarily unavailable. Please try again later."
                },
                "email": {
                    "welcome": {
                        "subject": "Welcome to Our Business",
                        "greeting": "Dear valued customer,",
                        "body": "We're excited to have you join us!",
                        "cta": "Visit us soon!",
                        "sign_off": "Best regards,"
                    },
                    "promotional": {
                        "subject": "Special Offer",
                        "greeting": "Hello!",
                        "body": "Check out our latest offers!",
                        "cta": "Don't miss out!",
                        "sign_off": "Best regards,"
                    },
                    "newsletter": {
                        "subject": "Monthly Update",
                        "greeting": "Hello!",
                        "body": "Here's what's new with us!",
                        "cta": "Stay tuned for more!",
                        "sign_off": "Best regards,"
                    }
                },
                "social_media": {
                    "instagram": "Follow us for updates!",
                    "facebook": "Like our page for news!",
                    "twitter": "Follow us for updates!",
                    "linkedin": "Connect with us professionally!"
                }
            }
    
    def _generate_business_description(self, business_data):
        """
        Generate a professional business description.
        
        Args:
            business_data (dict): Processed business information
            
        Returns:
            dict: Generated business description content
        """
        prompt = f"""Create a professional business description for '{business_data['name']}', a {business_data['type']} located in {business_data['location']}.
        
Business details:
- Description provided by owner: {business_data['description']}
- Target audience: {business_data['target_audience']}
- Style preference: {business_data['style_preference']}

Use a {business_data['tone']['voice']} tone and include {', '.join(business_data['business_context']['key_selling_points'])} as key selling points.

Generate three versions:
1. A short 50-word description for quick reference
2. A medium 150-word description for general use
3. A comprehensive 300-word description for detailed marketing materials

Each description should highlight what makes this business unique and appeal to their target audience."""

        try:
            content = self._make_api_request(prompt, "business description")
            
            # Parse the content into sections
            sections = content.split("\n\n")
            short_desc = ""
            medium_desc = ""
            long_desc = ""
            
            # Find descriptions based on keywords and numbering
            for section in sections:
                section = section.strip()
                if any(marker in section.lower() for marker in ["1.", "short", "50-word"]):
                    short_desc = section.split(":", 1)[1].strip() if ":" in section else section.lstrip("1.").strip()
                elif any(marker in section.lower() for marker in ["2.", "medium", "150-word"]):
                    medium_desc = section.split(":", 1)[1].strip() if ":" in section else section.lstrip("2.").strip()
                elif any(marker in section.lower() for marker in ["3.", "long", "comprehensive", "300-word"]):
                    long_desc = section.split(":", 1)[1].strip() if ":" in section else section.lstrip("3.").strip()

            # Clean up descriptions
            for desc in [short_desc, medium_desc, long_desc]:
                if not desc:
                    desc = "Content generation failed. Please try again."

            # Remove any remaining numbering or labels
            short_desc = short_desc.lstrip("123.").strip()
            medium_desc = medium_desc.lstrip("123.").strip()
            long_desc = long_desc.lstrip("123.").strip()

            if not any([short_desc, medium_desc, long_desc]):
                raise Exception("Failed to parse generated content properly")

        except Exception as e:
            # Provide fallback content when API fails
            return {
                "short": f"Error generating content: {str(e)}",
                "medium": "We apologize, but we're currently experiencing technical difficulties with our content generation service. Please try again later.",
                "long": "Our content generation service is temporarily unavailable. This could be due to API rate limits or service disruption. Please wait a few minutes and try your request again. If the problem persists, please contact support."
            }

        return {
            "short": short_desc.strip(),
            "medium": medium_desc.strip(),
            "long": long_desc.strip()
        }
    
    def _generate_email_templates(self, business_data):
        prompt = f"""Create email marketing templates for '{business_data['name']}', a {business_data['type']} business.
        
Business details:
- Description: {business_data['description']}
- Target audience: {business_data['target_audience']}
- Style preference: {business_data['style_preference']}

Generate three email templates:
1. Welcome email for new subscribers
2. Promotional email for special offers
3. Newsletter template for updates

Each template should have a subject line and body content.
Use a {business_data['tone']['voice']} tone and focus on {', '.join(business_data['business_context']['marketing_focus'])}."""

        try:
            content = self._make_api_request(prompt, "email templates")
            
            # Parse the content into templates
            templates = {}
            current_template = None
            current_section = None
            subject = ""
            body = ""
            
            for line in content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                
                # Detect template type
                if "welcome" in line.lower():
                    if subject and body and current_template:
                        templates[current_template] = {"subject": subject, "body": body}
                    current_template = "welcome"
                    subject = ""
                    body = ""
                elif "promotional" in line.lower() or "special offer" in line.lower():
                    if subject and body and current_template:
                        templates[current_template] = {"subject": subject, "body": body}
                    current_template = "promotional"
                    subject = ""
                    body = ""
                elif "newsletter" in line.lower():
                    if subject and body and current_template:
                        templates[current_template] = {"subject": subject, "body": body}
                    current_template = "newsletter"
                    subject = ""
                    body = ""
                
                # Detect sections
                if "subject" in line.lower() or "subject line" in line.lower():
                    current_section = "subject"
                    subject = line.split(":", 1)[1].strip() if ":" in line else ""
                elif "body" in line.lower() or "content" in line.lower():
                    current_section = "body"
                    body = line.split(":", 1)[1].strip() if ":" in line else ""
                elif current_section == "body":
                    body += "\n" + line
            
            # Add the last template
            if current_template and subject and body:
                templates[current_template] = {"subject": subject, "body": body}
            
            # Verify we have all templates
            if not all(key in templates for key in ["welcome", "promotional", "newsletter"]):
                raise Exception("Failed to generate all email templates")
            
            return templates
            
        except Exception as e:
            # Provide fallback content when API fails
            return {
                "welcome": {
                    "subject": "Service Temporarily Unavailable",
                    "body": f"Error generating welcome email template: {str(e)}\n\nPlease try again later."
                },
                "promotional": {
                    "subject": "Content Generation Service Disruption",
                    "body": "We're experiencing technical difficulties with our content generation service.\nThis may be due to API rate limits or service disruption.\nPlease try again in a few minutes."
                },
                "newsletter": {
                    "subject": "System Maintenance Notice",
                    "body": "Our content generation system is currently undergoing maintenance.\nWe apologize for any inconvenience.\nPlease refresh the page or try again later."
                }
            }
    
    def _generate_social_media_posts(self, business_data):
        prompt = f"""Create social media posts for '{business_data['name']}', a {business_data['type']} business.
        
Business details:
- Target audience: {business_data['target_audience']}
- Style preference: {business_data['style_preference']}

Generate three posts each for:
1. Facebook - Longer form, engaging content
2. Twitter/X - Short, punchy messages
3. Instagram - Visual-focused descriptions

Use a {business_data['tone']['voice']} tone and focus on {', '.join(business_data['business_context']['marketing_focus'])}."""

        try:
            content = self._make_api_request(prompt, "social media posts")
            
            # Parse the content into platform-specific posts
            posts = {}
            current_platform = None
            platform_posts = []
            
            for line in content.split("\n"):
                line = line.strip()
                if not line:
                    continue
                
                # Detect platform sections
                if "facebook" in line.lower():
                    if current_platform and platform_posts:
                        posts[current_platform] = platform_posts
                    current_platform = "facebook"
                    platform_posts = []
                elif "twitter" in line.lower() or "x:" in line.lower():
                    if current_platform and platform_posts:
                        posts[current_platform] = platform_posts
                    current_platform = "twitter"
                    platform_posts = []
                elif "instagram" in line.lower():
                    if current_platform and platform_posts:
                        posts[current_platform] = platform_posts
                    current_platform = "instagram"
                    platform_posts = []
                elif current_platform and (line.startswith("-") or line.startswith("*") or line[0].isdigit()):
                    platform_posts.append(line.lstrip("-*0123456789. ").strip())
            
            # Add the last platform's posts
            if current_platform and platform_posts:
                posts[current_platform] = platform_posts
            
            # Verify we have content for all platforms
            if not all(key in posts for key in ["facebook", "twitter", "instagram"]):
                raise Exception("Failed to generate posts for all platforms")
            
            return posts
            
        except Exception as e:
            # Provide fallback content when API fails
            return {
                "facebook": [
                    f"Error generating Facebook posts: {str(e)}",
                    "Our content generation service is temporarily unavailable.",
                    "Please try again in a few minutes."
                ],
                "twitter": [
                    "🚧 Service Update",
                    "Content generation temporarily unavailable due to technical issues.",
                    "Please retry shortly."
                ],
                "instagram": [
                    "System Maintenance Notice 🔧",
                    "Content generation service disruption.",
                    "We'll be back soon! Try again later."
                ]
            }