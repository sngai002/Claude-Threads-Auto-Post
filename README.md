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

1. **Clone** the repo:

   ```bash
   git clone https://github.com/yourusername/threads-auto-post.git
   cd threads-auto-post 
