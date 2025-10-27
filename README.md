
# Evan J. Corbin — Author Website

Bold, modern site to showcase books by **Evan J. Corbin** with a newsletter pop-up integrated to Mailchimp.

## Local preview

1. Ensure Python 3.10+ is installed.
2. In this folder:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # on Windows: .venv\Scripts\activate
   pip install flask requests python-docx
   python app.py
   ```
3. Open http://127.0.0.1:5000 to view the homepage.
4. Visit subpages:
   - `/books/atonement-camp`
   - `/books/atonement-camp-redemption`
   - `/books/asher-and-the-prince`
   - `/books/jingled`
   - `/about`

If you don't set Mailchimp keys, newsletter signups are saved to `local_signups/signups.csv`.

## Mailchimp (Render-ready)

Add these environment variables in Render (or locally):
- `MAILCHIMP_API_KEY`: e.g., `xxxx-us21` (find in Mailchimp)
- `MAILCHIMP_SERVER_PREFIX`: e.g., `us21` (the part after the dash in your API key)
- `MAILCHIMP_AUDIENCE_ID`: your Mailchimp Audience (List) ID

## Deploy to Render

- Create a new **Web Service** from your GitHub repo containing this folder.
- Runtime: Python 3.x
- Build Command: `pip install -r requirements.txt`
- Start Command: `gunicorn app:app`

Create `requirements.txt` with:
```
flask
requests
gunicorn
python-docx
```

## Customize

- Templates live in `templates/` (Tailwind via CDN for speed).
- Images live in `static/images/` (replace with higher-res as needed).
- Extra styles in `static/css/custom.css`.
