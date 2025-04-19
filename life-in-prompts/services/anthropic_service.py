import anthropic
import base64
import os
from io import BytesIO
from PIL import Image

class AnthropicService:
    def __init__(self, api_key):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = "claude-3-7-sonnet-20250219"
    
    def process_image(self, image_data):
        """Process image data and convert to base64 for Anthropic API"""
        try:
            # Open the image using PIL
            img = Image.open(BytesIO(image_data))
            
            # Convert to RGB if it's not already (e.g., if it's RGBA)
            if img.mode != 'RGB':
                img = img.convert('RGB')
            
            # Save to BytesIO object
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            
            # Get base64 encoded string
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            
            return {
                "type": "image",
                "source": {
                    "type": "base64",
                    "media_type": "image/jpeg",
                    "data": img_str
                }
            }
        except Exception as e:
            print(f"Error processing image: {e}")
            return None
    
    def get_response(self, prompt, image_data=None):
        """Get response from Anthropic API"""
        try:
            messages = [{"role": "user", "content": []}]
            
            # Add text content
            if prompt:
                messages[0]["content"].append({"type": "text", "text": prompt})
            
            # Add image content if provided
            if image_data:
                image_content = self.process_image(image_data)
                if image_content:
                    messages[0]["content"].append(image_content)
            
            # Make API call
            response = self.client.messages.create(
                model=self.model,
                max_tokens=4096,
                messages=messages
            )
            
            # Check if response and content are valid
            if response and hasattr(response, 'content') and response.content:
                return response.content[0].text
            else:
                error_msg = "Empty or invalid response from Anthropic API"
                print(error_msg)
                return f"Error: {error_msg}"
                
        except anthropic.APIError as api_err:
            error_msg = f"Anthropic API Error: {api_err}"
            print(error_msg)
            return f"Error: {error_msg}"
        except anthropic.APIConnectionError as conn_err:
            error_msg = f"Connection Error: {conn_err}"
            print(error_msg)
            return f"Error: {error_msg}"
        except anthropic.RateLimitError as rate_err:
            error_msg = f"Rate Limit Error: {rate_err}"
            print(error_msg)
            return f"Error: {error_msg}"
        except Exception as e:
            error_msg = f"Error getting response from Anthropic: {e}"
            print(error_msg)
            return f"Error: {error_msg}"
