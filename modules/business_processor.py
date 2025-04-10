# Business Information Processor Module

class BusinessProcessor:
    """
    Processes business information submitted by users and prepares it for content generation.
    """
    
    def __init__(self):
        """
        Initialize the BusinessProcessor.
        """
        pass
    
    def process(self, business_data):
        """
        Process the business data to prepare it for content generation.
        
        Args:
            business_data (dict): Dictionary containing business information
                - name: Business name
                - type: Type of business
                - description: Brief description of the business
                - location: Business location
                - target_audience: Target audience description
                - style_preference: Preferred style for content
                
        Returns:
            dict: Processed business data with additional context
        """
        try:
            # Validate required fields
            required_fields = ['name', 'type', 'description', 'location', 'target_audience', 'style_preference']
            for field in required_fields:
                if not business_data.get(field):
                    raise ValueError(f"Missing required field: {field}")

            # Create a copy of the original data
            processed_data = business_data.copy()
            
            # Add additional context based on business type
            processed_data['business_context'] = self._get_business_context(business_data['type'])
            
            # Add tone based on style preference
            processed_data['tone'] = self._get_tone(business_data['style_preference'])
            
            # Add local context based on location
            processed_data['local_context'] = self._get_local_context(business_data['location'])
            
            # Add audience insights
            processed_data['audience_insights'] = self._analyze_audience(business_data['target_audience'])

            # Ensure all required fields for content generation are present
            if not all(key in processed_data for key in ['business_context', 'tone', 'local_context', 'audience_insights']):
                raise ValueError("Failed to generate all required context data")
            
            return processed_data
            
        except Exception as e:
            print(f"Error processing business data: {str(e)}")
            # Return a simplified version of the data that can still be used
            return {
                'name': business_data.get('name', ''),
                'type': business_data.get('type', ''),
                'description': business_data.get('description', ''),
                'location': business_data.get('location', ''),
                'target_audience': business_data.get('target_audience', ''),
                'style_preference': business_data.get('style_preference', ''),
                'business_context': {
                    'key_selling_points': ['quality service', 'customer satisfaction'],
                    'marketing_focus': ['customer benefits', 'reliability']
                },
                'tone': {
                    'voice': 'professional and friendly',
                    'sentence_style': 'clear and engaging'
                },
                'local_context': {
                    'local_terms': ['local', 'community'],
                    'community_focus': ['serving the community']
                },
                'audience_insights': {
                    'pain_points': ['convenience', 'quality'],
                    'motivations': ['improvement', 'enjoyment'],
                    'communication_style': 'clear and relatable'
                }
            }
    
    def _get_business_context(self, business_type):
        """
        Get additional context based on business type.
        
        Args:
            business_type (str): Type of business
            
        Returns:
            dict: Business context information
        """
        # Define common challenges and opportunities for different business types
        context_map = {
            "Restaurant": {
                "key_selling_points": ["cuisine", "ambiance", "dining experience"],
                "common_challenges": ["competition", "food quality consistency", "customer service"],
                "marketing_focus": ["menu highlights", "special offers", "unique dining experience"]
            },
            "Retail Store": {
                "key_selling_points": ["product selection", "customer service", "shopping experience"],
                "common_challenges": ["online competition", "inventory management", "customer retention"],
                "marketing_focus": ["product quality", "exclusive items", "in-store experience"]
            },
            "Salon/Spa": {
                "key_selling_points": ["skilled professionals", "relaxing environment", "quality services"],
                "common_challenges": ["appointment scheduling", "client retention", "service consistency"],
                "marketing_focus": ["expertise", "relaxation", "self-care", "transformation"]
            },
            "Fitness Center": {
                "key_selling_points": ["equipment variety", "class offerings", "expert trainers"],
                "common_challenges": ["member retention", "facility maintenance", "competition"],
                "marketing_focus": ["results", "community", "health benefits", "expert guidance"]
            },
            "Cafe": {
                "key_selling_points": ["coffee quality", "ambiance", "food options"],
                "common_challenges": ["competition", "consistency", "peak hour management"],
                "marketing_focus": ["coffee expertise", "cozy atmosphere", "community space"]
            }
        }
        
        # Return context for the specific business type or a generic one if not found
        return context_map.get(business_type, {
            "key_selling_points": ["quality service", "customer satisfaction", "expertise"],
            "common_challenges": ["market visibility", "customer acquisition", "service delivery"],
            "marketing_focus": ["unique value proposition", "customer benefits", "reliability"]
        })
    
    def _get_tone(self, style_preference):
        """
        Determine the appropriate tone based on style preference.
        
        Args:
            style_preference (str): Preferred style for content
            
        Returns:
            dict: Tone information
        """
        tone_map = {
            "Modern": {
                "adjectives": ["innovative", "cutting-edge", "sleek", "contemporary"],
                "voice": "confident and forward-thinking",
                "sentence_style": "concise and impactful"
            },
            "Classic": {
                "adjectives": ["timeless", "traditional", "established", "trusted"],
                "voice": "authoritative and refined",
                "sentence_style": "well-structured and elegant"
            },
            "Bold": {
                "adjectives": ["striking", "powerful", "dynamic", "fearless"],
                "voice": "assertive and energetic",
                "sentence_style": "direct and attention-grabbing"
            },
            "Minimal": {
                "adjectives": ["clean", "essential", "streamlined", "uncluttered"],
                "voice": "straightforward and precise",
                "sentence_style": "simple and focused"
            },
            "Elegant": {
                "adjectives": ["sophisticated", "refined", "luxurious", "graceful"],
                "voice": "polished and sophisticated",
                "sentence_style": "flowing and articulate"
            }
        }
        
        # Return tone for the specific style or a generic one if not found
        return tone_map.get(style_preference, {
            "adjectives": ["professional", "reliable", "quality", "dedicated"],
            "voice": "friendly and professional",
            "sentence_style": "clear and engaging"
        })
    
    def _get_local_context(self, location):
        """
        Get local context based on location.
        
        Args:
            location (str): Business location
            
        Returns:
            dict: Local context information
        """
        # In a real application, this could use a location API to get more specific information
        # For now, we'll return a generic structure that can be filled with more specific info later
        return {
            "local_terms": ["local", "community", "neighborhood"],
            "community_focus": ["serving the community", "local favorite", "neighborhood gem"],
            "regional_appeal": ["in the heart of " + location, "serving " + location + " and surrounding areas"]
        }
    
    def _analyze_audience(self, target_audience):
        """
        Analyze target audience to provide insights.
        
        Args:
            target_audience (str): Target audience description
            
        Returns:
            dict: Audience insights
        """
        # In a real application, this could use NLP to analyze the target audience description
        # For now, we'll return a generic structure
        return {
            "pain_points": ["convenience", "quality", "value"],
            "motivations": ["improvement", "enjoyment", "necessity"],
            "communication_style": "clear and relatable"
        }