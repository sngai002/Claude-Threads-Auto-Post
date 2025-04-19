# Life in Prompts

## 1.1. Project Overview

'Life in Prompts' is an automated system that documents every conversation with Claude AI by capturing user prompts and posting them to Threads. This project creates a lifelong archive of AI interactions, transforming ephemeral digital conversations into preserved artifacts.

## 1.2. Purpose

The official Claude.ai interface doesn't provide direct access to user prompts for archival purposes. This project solves that limitation by creating a Python-based Claude clone using the Anthropic API, which allows for:

- **Prompt Capture:** Direct access to the text of user promptsAutomated
- **Documentation**: Systematic recording of every AI interaction
- **Public Archiving**: Seamless posting to Threads for public preservation

This tool enables the creation of a living document of human-AI interaction, serving both as a personal archive and a historical record of early AI conversation patterns during a significant period of technological evolution.

## 1.3. Conceptual Foundation

Inspired by conceptual artists like On Kawara (date paintings) and Martin John Callanan (Photoshop command documentation), this project explores what deserves preservation in our digital lives. As T.S. Eliot measured life in coffee spoons, this project measures life through AI interactions—capturing not just queries but a specific moment in technological evolution.
The system creates a continuous, unfiltered record that will span a lifetime, challenging conventional notions of what deserves documentation while preserving the evolution of human-AI dialogue.

## 1.4. Core Functionality

- Python-based Claude clone utilizing the Anthropic API
- Prompt scraping mechanism that captures user inputs
- Integration with Threads via ThreadsPipePy
- Continuous, automated operation for lifelong documentation

---

## 2. Installation & Setup

1. Clone the repository
   ```
   git clone https://github.com/yourusername/threads-auto-post.git.cd threads-auto-post
2. Create & activate a Python virtual environment
   ```
   python3 -m venv .venv
   source .venv/bin/activate
3. Install dependencies
   ```
   pip install -r requirements.txt
4. Configure your credentials
   ``` python
   # Anthropic AI key
   ANTHROPIC_API_KEY=sk-<your_anthropic_api_key>
   
   # Threads login (for initial sign‑in)
   THREADS_USERNAME=<your_threads_username>
   THREADS_PASSWORD=<your_threads_password>
   
   # Meta/Threads App credentials
   THREADS_APP_ID=<your_app_id>
   THREADS_APP_SECRET=<your_app_secret>
   
   # (Optional) if you have a long‑lived token already:
   THREADS_ACCESS_TOKEN=<your_long_lived_token>
   
   # (Optional) override Flask secret
   FLASK_SECRET_KEY=<your_flask_secret>
---

## 3. Running the App
   - Browser UI (with live updates via SocketIO):
      ``` python
      python app.py
      ```
      Then open http://localhost:5000 in your browser.

   - JSON API:
   ```
   curl -X POST http://localhost:5000/api/chat \
     -F "prompt=Your message here" \
     -F "image=@/path/to/photo.jpg"
   ```

---

## 4. CLI Token Helpers (Optional)
If you need to obtain or refresh your Threads access token, use the built‑in CLI:
   
   ``` python
   # Exchange code for token:
   python -m threadspipepy.cli get_access_token \
     --app-id $THREADS_APP_ID \
     --app-secret $THREADS_APP_SECRET \
     --redirect-uri http://localhost:5000 \
     --env-path .env \
     --env-variable THREADS_ACCESS_TOKEN

   # Refresh an existing token:
   python -m threadspipepy.cli refresh_token \
     --access-token $THREADS_ACCESS_TOKEN \
     --env-path .env \
     --env-variable THREADS_ACCESS_TOKEN
   ```
## 5. Troubleshooting

- Login failures: Verify THREADS_USERNAME/PASSWORD or refreshed access token.
- Anthropic errors: Check your key and rate limits in anthropic_service.py.
- File upload issues: Confirm valid image formats (JPEG/PNG) and Pillow installed.

---

With just your keys and usernames, you’re all set—enjoy automating your Threads posts!
I’m excited to see artists, researchers, and technologists exploring the evolution of AI interaction over time!🚀🤖

