# Image Service Module

import requests
import random
import json

class ImageService:
    """
    Handles image generation using Stability AI and Bria2.3 APIs based on business type and style.
    """
    
    def __init__(self, stability_api_key=None, bria_api_key=None, unsplash_api_key=None, unsplash_secret_key=None):
        """
        Initialize the ImageService with API keys.
        
        Args:
            stability_api_key (str): Stability AI API key
            bria_api_key (str): Bria2.3 API key
            unsplash_api_key (str): Unsplash API key (for fallback)
            unsplash_secret_key (str): Unsplash Secret key (for fallback)
        """
        self.stability_api_key = stability_api_key
        self.bria_api_key = bria_api_key
        self.unsplash_api_key = unsplash_api_key
        self.unsplash_secret_key = unsplash_secret_key
        
        # API endpoints
        self.stability_api_url = "https://api.stability.ai/v1/generation/stable-diffusion-xl-1024-v1-0/text-to-image"
        self.bria_api_url = "https://api.nvcf.nvidia.com/v2/nvcf/pexec/functions/bria"
        self.unsplash_api_url = "https://api.unsplash.com/search/photos"
    
    def get_images(self, business_type, style_preference, count=3):
        """
        Get relevant images based on business type and style preference.
        
        Args:
            business_type (str): Type of business
            style_preference (str): Preferred style
            count (int): Number of images to return
            
        Returns:
            list: List of image URLs
        """
        # Determine search terms based on business type and style
        search_terms = self._get_search_terms(business_type, style_preference)
        
        # Create a prompt for AI image generation
        prompt = self._create_image_prompt(business_type, style_preference)
        
        # Try to generate images with Stability AI first
        stability_images = self._generate_with_stability(prompt, count=count)
        
        # If we don't have enough images from Stability AI, try Bria2.3
        if len(stability_images) < count:
            bria_images = self._generate_with_bria(prompt, count=count-len(stability_images))
            images = stability_images + bria_images
        else:
            images = stability_images[:count]
        
        # If we still don't have enough images, try Unsplash as fallback
        if len(images) < count and self.unsplash_api_key:
            unsplash_images = self._get_unsplash_images(search_terms, count-len(images))
            images = images + unsplash_images
        
        return images[:count]  # Ensure we only return the requested number of images
    
    def _get_search_terms(self, business_type, style_preference):
        """
        Generate search terms based on business type and style preference.
        
        Args:
            business_type (str): Type of business
            style_preference (str): Preferred style
            
        Returns:
            list: List of search terms
        """
        # Base search terms from business type
        base_terms = [business_type.lower()]
        
        # Add style-specific terms
        style_terms = {
            "Modern": ["modern", "contemporary", "sleek"],
            "Classic": ["classic", "traditional", "timeless"],
            "Bold": ["bold", "vibrant", "striking"],
            "Minimal": ["minimal", "clean", "simple"],
            "Elegant": ["elegant", "sophisticated", "refined"]
        }
        
        # Add business-specific terms
        business_terms = {
            "Restaurant": ["food", "dining", "restaurant interior"],
            "Retail Store": ["retail", "store", "shopping"],
            "Salon/Spa": ["salon", "spa", "beauty"],
            "Fitness Center": ["fitness", "gym", "workout"],
            "Cafe": ["cafe", "coffee", "cozy"],
            "Bakery": ["bakery", "pastry", "bread"],
            "Consulting": ["consulting", "business", "professional"],
            "Legal Services": ["legal", "law", "professional"],
            "Healthcare": ["healthcare", "medical", "wellness"],
            "Real Estate": ["real estate", "property", "home"],
            "Technology": ["technology", "tech", "digital"],
            "Education": ["education", "learning", "school"],
            "Art Gallery": ["art", "gallery", "exhibition"],
            "Automotive": ["automotive", "car", "vehicle"],
            "Construction": ["construction", "building", "architecture"],
            "Event Planning": ["event", "celebration", "planning"],
            "Financial Services": ["financial", "banking", "business"],
            "Home Services": ["home", "services", "interior"],
            "Pet Services": ["pet", "animal", "dog cat"],
        }
        
        # Combine terms
        combined_terms = base_terms.copy()
        combined_terms.extend(style_terms.get(style_preference, ["professional", "business"]))
        combined_terms.extend(business_terms.get(business_type, ["business", "professional"]))
        
        # Create search queries by combining terms
        search_queries = [
            f"{business_type.lower()} {style_preference.lower()}",
            f"{business_type.lower()} business",
            random.choice(combined_terms)
        ]
        
        return search_queries
    
    def _create_image_prompt(self, business_type, style_preference):
        """
        Create a detailed prompt for AI image generation.
        
        Args:
            business_type (str): Type of business
            style_preference (str): Preferred style
            
        Returns:
            str: Detailed prompt for image generation
        """
        # Base prompt structure
        base_prompt = f"A professional, high-quality image for a {business_type.lower()} business"
        
        # Style modifiers
        style_modifiers = {
            "Modern": "with a modern, sleek, and contemporary aesthetic",
            "Classic": "with a classic, traditional, and timeless design",
            "Bold": "with bold, vibrant colors and striking visual elements",
            "Minimal": "with a minimalist, clean, and simple design",
            "Elegant": "with an elegant, sophisticated, and refined appearance",
            "Playful": "with a playful, fun, and energetic atmosphere",
            "Professional": "with a professional, corporate, and polished look",
            "Rustic": "with a rustic, warm, and natural ambiance",
            "Luxurious": "with a luxurious, premium, and high-end feel",
            "Eco-friendly": "with an eco-friendly, sustainable, and natural theme"
        }
        
        # Business-specific details
        business_details = {
            "Restaurant": "showing an inviting dining area with elegant table settings and ambient lighting",
            "Retail Store": "featuring a well-organized store interior with attractive product displays",
            "Salon/Spa": "depicting a serene and relaxing spa environment with soft lighting and clean spaces",
            "Fitness Center": "showing a modern gym with well-maintained equipment and motivational atmosphere",
            "Cafe": "with a cozy coffee shop interior, featuring warm lighting and comfortable seating",
            "Bakery": "displaying artisanal baked goods in an inviting bakery setting",
            "Consulting": "with a professional office environment conveying trust and expertise",
            "Legal Services": "featuring a sophisticated law office with professional decor and bookshelves",
            "Healthcare": "showing a clean, welcoming medical facility that conveys care and professionalism",
            "Real Estate": "featuring an attractive property with appealing architectural elements",
            "Technology": "with a modern tech workspace showing innovation and digital elements",
            "Education": "depicting an engaging learning environment with educational resources",
            "Art Gallery": "showing an elegant gallery space with proper lighting and artistic displays",
            "Automotive": "featuring a professional automotive service center or showroom",
            "Construction": "showing a construction project with professional equipment and safety measures",
            "Event Planning": "depicting a beautifully decorated event space with attention to detail",
            "Financial Services": "with a professional financial office conveying trust and security",
            "Home Services": "showing a professional performing home maintenance or improvement",
            "Pet Services": "featuring a clean, friendly environment for pet care and services"
        }
        
        # Quality and technical specifications
        quality_specs = "8k resolution, professional photography, perfect lighting, photorealistic"
        
        # Combine all elements
        style_modifier = style_modifiers.get(style_preference, "with a professional and appealing design")
        business_detail = business_details.get(business_type, "in a professional setting")
        
        prompt = f"{base_prompt} {style_modifier}, {business_detail}. {quality_specs}"
        
        return prompt
    
    def _generate_with_stability(self, prompt, count=1):
        """
        Generate images using Stability AI API.
        
        Args:
            prompt (str): Detailed prompt for image generation
            count (int): Number of images to generate
            
        Returns:
            list: List of generated image URLs and metadata
        """
        images = []
        
        if not self.stability_api_key:
            print("Stability AI API key not provided. Skipping Stability AI generation.")
            return images
        
        try:
            headers = {
                "Authorization": f"Bearer {self.stability_api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            data = {
                "text_prompts": [
                    {
                        "text": prompt,
                        "weight": 1.0
                    },
                    {
                        "text": "blurry, distorted, low quality, unrealistic, pixelated",
                        "weight": -1.0
                    }
                ],
                "cfg_scale": 7.0,
                "height": 1024,
                "width": 1024,
                "samples": min(count, 4),  # Limit to reasonable number
                "steps": 30
            }
            
            response = requests.post(self.stability_api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                artifacts = result.get("artifacts", [])
                
                for i, artifact in enumerate(artifacts):
                    if i >= count:
                        break
                    
                    # In a real app, you would save this base64 image to a file or cloud storage
                    # For this example, we'll create a placeholder URL structure
                    image_data = artifact.get("base64", None)
                    seed = artifact.get("seed", 0)
                    
                    if image_data:
                        # In a real implementation, you would save this image and get a real URL
                        # For now, we'll use a placeholder structure
                        image_url = f"data:image/png;base64,{image_data}"
                        
                        images.append({
                            "url": image_url,
                            "source": "Stability AI",
                            "prompt": prompt,
                            "id": f"stability-{seed}",
                            "download_url": image_url
                        })
            elif response.status_code == 401:
                print(f"Stability AI API authentication error: Invalid API key or unauthorized access")
            elif response.status_code == 429:
                print(f"Stability AI API rate limit exceeded. Try again later.")
            else:
                print(f"Stability AI API error: Status code {response.status_code}")
                if response.text:
                    try:
                        error_data = response.json()
                        print(f"Error details: {error_data}")
                    except:
                        print(f"Error response: {response.text}")
        except Exception as e:
            print(f"Error generating images with Stability AI: {e}")
        
        return images
    
    def _generate_with_bria(self, prompt, count=1):
        """
        Generate images using Bria2.3 API.
        
        Args:
            prompt (str): Detailed prompt for image generation
            count (int): Number of images to generate
            
        Returns:
            list: List of generated image URLs and metadata
        """
        images = []
        
        if not self.bria_api_key:
            print("Bria2.3 API key not provided. Skipping Bria2.3 generation.")
            return images
        
        try:
            headers = {
                "Authorization": f"Bearer {self.bria_api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "prompt": prompt,
                "negative_prompt": "blurry, distorted, low quality, unrealistic, pixelated",
                "num_images": min(count, 4),  # Limit to reasonable number
                "guidance_scale": 7.5,
                "width": 1024,
                "height": 1024,
                "num_inference_steps": 30
            }
            
            response = requests.post(self.bria_api_url, headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                output_data = result.get("data", {}).get("output", [])
                
                for i, image_data in enumerate(output_data):
                    if i >= count:
                        break
                    
                    # For this example, we'll create a placeholder URL structure
                    # In a real app, you would save this image to a file or cloud storage
                    image_url = image_data.get("image", None)
                    
                    if image_url:
                        images.append({
                            "url": image_url,
                            "source": "Bria2.3",
                            "prompt": prompt,
                            "id": f"bria-{i}",
                            "download_url": image_url
                        })
            elif response.status_code == 401:
                print(f"Bria2.3 API authentication error: Invalid API key or unauthorized access")
            elif response.status_code == 429:
                print(f"Bria2.3 API rate limit exceeded. Try again later.")
            else:
                print(f"Bria2.3 API error: Status code {response.status_code}")
                if response.text:
                    try:
                        error_data = response.json()
                        print(f"Error details: {error_data}")
                    except:
                        print(f"Error response: {response.text}")
        except Exception as e:
            print(f"Error generating images with Bria2.3: {e}")
        
        return images
    
    def _get_unsplash_images(self, search_terms, count):
        """
        Get images from Unsplash API as fallback.
        
        Args:
            search_terms (list): List of search terms
            count (int): Number of images to return
            
        Returns:
            list: List of image URLs
        """
        images = []
        
        if not self.unsplash_api_key:
            return images
        
        try:
            # Try each search term until we have enough images
            for term in search_terms:
                if len(images) >= count:
                    break
                    
                params = {
                    "query": term,
                    "per_page": count,
                    "orientation": "landscape"
                }
                
                headers = {
                    "Authorization": f"Client-ID {self.unsplash_api_key}"
                }
                
                response = requests.get(self.unsplash_api_url, params=params, headers=headers)
                
                if response.status_code == 200:
                    data = response.json()
                    results = data.get("results", [])
                    
                    for result in results:
                        if len(images) >= count:
                            break
                            
                        image_url = result.get("urls", {}).get("regular")
                        if image_url and image_url not in [img.get("url") for img in images]:
                            images.append({
                                "url": image_url,
                                "source": "Unsplash",
                                "photographer": result.get("user", {}).get("name", "Unknown"),
                                "photographer_url": result.get("user", {}).get("links", {}).get("html", ""),
                                "download_url": image_url
                            })
                elif response.status_code == 401:
                    print(f"Unsplash API authentication error: Invalid API key or unauthorized access")
                elif response.status_code == 429:
                    print(f"Unsplash API rate limit exceeded. Try again later.")
                else:
                    print(f"Unsplash API error: Status code {response.status_code}")
        except Exception as e:
            print(f"Error fetching images from Unsplash: {e}")
        
        return images