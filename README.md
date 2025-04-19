# Threads Auto‑Post

## 1. Project Overview and Purpose

This project provides a **Flask**‑based web application and command‑line utilities to:

- **Generate** AI‑powered captions or narratives using the Anthropic Claude model (via `anthropic-python`).
- **Upload** images and text automatically to Instagram’s Threads platform through the `threadspipepy` library.
- Offer a simple browser UI (HTML/JS/CSS) plus a JSON‑API (`/api/chat`) for programmatic use.
- Manage and refresh long‑lived Threads access tokens with a CLI helper.

Use this to prototype creative automated workflows, e.g. AI‑generated image captions, galleries or “bot” accounts for art, photography, or visual journalism.

---

## 2. Installation Requirements

- **Python 3.10+**  
- **pip**  
- System packages to support Pillow (for image I/O)  
- A Threads developer account (to obtain App ID / Secret)  
- An Anthropic account + API key or any LLM Model you're using

---

## 3. Setup Instructions

   ### 3.1. **Clone** the repo:

      ```bash
      git clone https://github.com/yourusername/threads-auto-post.git
      cd threads-auto-post 

   ### 3.2. **Create & activate** a virtual environment:
      ```bash
      python3 -m venv .venv
      source .venv/bin/activate

   ### 3.3. **Install** Python dependencies:
      ```bash
      pip install -r requirements.txt

   ### 3.4. **Register** your Threads app if you haven’t yet:
      - Go to the Threads/Meta developer portal
      - Create an application, note the App ID and App Secret
      - Configure your OAuth redirect URI (e.g. http://localhost:5000)

---

## 4. Configuration Steps
   ```dotenv
   # Anthropic AI
   ANTHROPIC_API_KEY=sk-...
   
   # Threads credentials (for initial login)
   THREADS_USERNAME=your_threads_username
   THREADS_PASSWORD=your_threads_password
   
   # Meta App credentials (for access/token management)
   THREADS_APP_ID=1234567890
   THREADS_APP_SECRET=abcdef1234567890abcdef1234567890
   
   # (Optional) If you already have a long‑lived access token:
   THREADS_ACCESS_TOKEN=EAA...
   
   # Flask secret key (will default to random if omitted)
   FLASK_SECRET_KEY=supersecret123

   Security note: Never commit .env to source control. Add it to .gitignore.

---

## 5. Usage Examples

   5.1 Obtain / Refresh a Threads Access Token
   Use the built‑in CLI helper in threadspipepy:

   # Get a short‑lived code, then exchange for a token
   python -m threadspipepy.cli get_access_token \
     --app-id $THREADS_APP_ID \
     --app-secret $THREADS_APP_SECRET \
     --redirect-uri http://localhost:5000 \
     --env-path .env \
     --env-variable THREADS_ACCESS_TOKEN
   
   # Refresh a token when it’s about to expire
   python -m threadspipepy.cli refresh_token \
     --access-token $THREADS_ACCESS_TOKEN \
     --env-path .env \
     --env-variable THREADS_ACCESS_TOKEN

   5.2 Launch the Flask App
   ```bash
   export FLASK_APP=app.py
   flask run
   # OR, for real‑time updates / SocketIO support:
   python app.py
