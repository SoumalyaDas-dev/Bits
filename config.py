# Configuration file for AI-Powered Local Business Booster

# API Keys
# Image Generation APIs
STABILITY_AI_API_KEY = "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"
BRIA_API_KEY = "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"

# LLM API
GEMMA_API_KEY = "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"

# Other APIs
TINYCLOUD_API_KEY = "cvvhwn9fyklicc1qzwccmq91b2li680e3lxpa8b4wyacqgj8"
UNSPLASH_API_KEY = "czgKy4fWZ1XC9gT_WPdkoVXE9zoc_U57whxMb5O1AK8"
UNSPLASH_SECRET_KEY = "rh4SF48lwdK4QK0pHuVWe4b0NBzaU1ma5Bt9TM5i4g0"

# Application Settings
DEBUG = True
SECRET_KEY = "your-secret-key-for-flask-sessions"

# File Storage Settings
UPLOAD_FOLDER = "uploads"
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg"}
MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload size

# Content Generation Settings
BUSINESS_TYPES = [
    "Restaurant", "Retail Store", "Salon/Spa", "Fitness Center", 
    "Cafe", "Bakery", "Consulting", "Legal Services", "Healthcare", 
    "Real Estate", "Technology", "Education", "Art Gallery", "Automotive", 
    "Construction", "Event Planning", "Financial Services", "Home Services", 
    "Pet Services", "Other"
]

STYLE_PREFERENCES = [
    "Modern", "Classic", "Bold", "Minimal", "Elegant", 
    "Playful", "Professional", "Rustic", "Luxurious", "Eco-friendly"
]

# Image Service Settings
IMAGE_CATEGORIES = {
    "Restaurant": ["restaurant", "food", "dining"],
    "Retail Store": ["retail", "store", "shopping"],
    "Salon/Spa": ["salon", "spa", "beauty"],
    "Fitness Center": ["fitness", "gym", "workout"],
    "Cafe": ["cafe", "coffee", "cozy"],
    "Bakery": ["bakery", "pastry", "bread"],
    "Consulting": ["consulting", "business", "professional"],
    "Legal Services": ["legal", "law", "attorney"],
    "Healthcare": ["healthcare", "medical", "wellness"],
    "Real Estate": ["real estate", "property", "home"],
    "Technology": ["technology", "tech", "digital"],
    "Education": ["education", "learning", "school"],
    "Art Gallery": ["art", "gallery", "creative"],
    "Automotive": ["automotive", "car", "mechanic"],
    "Construction": ["construction", "building", "contractor"],
    "Event Planning": ["event", "planning", "celebration"],
    "Financial Services": ["financial", "banking", "investment"],
    "Home Services": ["home", "services", "repair"],
    "Pet Services": ["pet", "animal", "veterinary"],
    "Other": ["business", "professional", "service"]
}

DEFAULT_IMAGE_COUNT = 3
IMAGE_QUALITY = "high"