import requests
import json
import os
import time
import uuid
from werkzeug.utils import secure_filename
from urllib.parse import urlparse

from threadspipepy.threadspipe import ThreadsPipe

import logging
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class ThreadsService:
    def __init__(self, username=None, password=None, app_id=None, app_secret=None, access_token=None):
        """Initialize Threads API with credentials"""
        self.app_id = app_id or ""
        self.app_secret = app_secret or ""
        self.access_token = access_token or ""
        self.api_base_url = "https://graph.threads.net/v1.0"
        self.logged_in = self.validate_token()
        
        if self.logged_in:
            print("Successfully authenticated with Threads API")
        else:
            print("Failed to authenticate with Threads API")
            
        self.api = ThreadsPipe(
            access_token= self.access_token, 
            user_id= self.user_id, 
            handle_hashtags=True, 
            auto_handle_hashtags=False, 
            gh_bearer_token = "",
            gh_repo_name = "",
            gh_username = '',
        )
            
    def validate_token(self):
        """Validate the access token by making a test API call"""
        try:
            # Try to get user info to validate the token
            url = f"{self.api_base_url}/me?fields=id,username"
            headers = {
                "Authorization": f"Bearer {self.access_token}"
            }
            response = requests.get(url, headers=headers)
            
            if response.status_code == 200:
                user_data = response.json()
                self.user_id = user_data.get("id")
                self.username = user_data.get("username")
                return True
            else:
                print(f"Token validation failed: {response.text}")
                return False
        except Exception as e:
            print(f"Error validating token: {e}")
            return False
    
    def is_logged_in(self):
        """Check if logged in to Threads"""
        return self.logged_in
    
    def post_text(self, text):
        if not self.is_logged_in():
            return False, "Not logged in to Threads"

        try:
            pipe = self.api.pipe(
            text,
        )

            print("pipe", pipe)
            
            return True, f"Post successfully sent to Threads"

        except Exception as e:
            return False, f"Error posting to Threads: {e}"

    def post_with_image(self, text, uploaded_files_or_urls):
        if not self.is_logged_in():
            return False, "Not logged in to Threads"

        upload_dir = "uploads"
        os.makedirs(upload_dir, exist_ok=True)
        valid_files = []
        try:
            for item in uploaded_files_or_urls:
                image_bytes = None

                if hasattr(item, 'read'):
                    try:
                        image_bytes = item.read()
                        if image_bytes:
                            print(f"✅ Read {len(image_bytes)} bytes from uploaded file: {item.filename}")
                        else:
                            print(f"⚠️ Uploaded file was empty: {item.filename}")
                    except Exception as e:
                        print(f"❌ Error reading uploaded file: {item.filename} — {e}")

                elif isinstance(item, str):
                    if is_valid_url(item):
                        try:
                            response = requests.get(item, timeout=10)
                            if response.status_code == 200 and 'image' in response.headers.get('Content-Type', ''):
                                image_bytes = response.content
                            else:
                                print(f"❌ Skipped invalid content type: {item}")
                        except Exception as e:
                            print(f"❌ Skipped failed URL fetch: {item} — {e}")
                    elif os.path.exists(item):  # Local path
                        try:
                            with open(item, "rb") as f:
                                image_bytes = f.read()
                        except Exception as e:
                            print(f"❌ Failed to read local file: {item} — {e}")

                if image_bytes:
                    valid_files.append(image_bytes)
                else:
                    print(f"⚠️ Skipped: No valid content for item: {item}")

            if not valid_files:
                return False, "No valid image or video files to post"

            pipe = self.api.pipe(text, files=valid_files)
            print("pipe", pipe)

            return True, f"Post successfully sent to Threads with {len(valid_files)} file(s)"

        except Exception as e:
            return False, f"Error uploading or posting to Threads: {e}"



def is_valid_url(url):
        try:
            result = urlparse(url)
            return result.scheme in ("http", "https") and bool(result.netloc)
        except:
            return False