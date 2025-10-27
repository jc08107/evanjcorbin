
import os
from flask import Flask, render_template, send_from_directory, request, jsonify
import requests

app = Flask(__name__)

@app.context_processor
def inject_globals():
    import datetime
    return {
        "now": datetime.datetime.utcnow,
        "PEN_NAME": "Evan J. Corbin",
    }


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/books/<slug>")
def book_page(slug):
    # Map slug to template filenames we created
    mapping = {
        "atonement-camp": "atonement-camp.html",
        "atonement-camp-redemption": "atonement-camp-redemption.html",
        "asher-and-the-prince": "asher-and-the-prince.html",
        "jingled": "jingled.html",
    }
    tpl = mapping.get(slug)
    if not tpl:
        return "Not found", 404
    return render_template(tpl)

@app.route("/privacy")
def privacy():
    return render_template("privacy-policy.html")

@app.route("/subscribe", methods=["POST"])
def subscribe():
    data = request.get_json(force=True)
    email = data.get("email")
    first = data.get("first_name")
    last = data.get("last_name")

    if not email:
        return jsonify({"ok": False, "message": "Email is required."}), 400

    # Env vars for Mailchimp
    api_key = os.getenv("MAILCHIMP_API_KEY")
    audience_id = os.getenv("MAILCHIMP_AUDIENCE_ID")  # also called 'list id'
    server_prefix = os.getenv("MAILCHIMP_SERVER_PREFIX")  # like 'us21'

    if not (api_key and audience_id and server_prefix):
        # Local/dev fallback: pretend success and write to a local file for your records
        os.makedirs("local_signups", exist_ok=True)
        with open(os.path.join("local_signups", "signups.csv"), "a", encoding="utf-8") as f:
            f.write(f"{email},{first or ''},{last or ''}\n")
        return jsonify({"ok": True, "message": "Thanks! (Saved locally — add Mailchimp keys to enable live signup.)"})

    # Mailchimp API call
    url = f"https://{server_prefix}.api.mailchimp.com/3.0/lists/{audience_id}/members"
    payload = {
        "email_address": email,
        "status": "subscribed",
        "merge_fields": {"FNAME": first or "", "LNAME": last or ""},
    }
    auth = ("anystring", api_key)
    resp = requests.post(url, json=payload, auth=auth, timeout=10)
    if resp.status_code in (200, 201):
        return jsonify({"ok": True, "message": "Subscribed! Check your inbox."})
    # If already subscribed or other error
    try:
        err = resp.json()
    except Exception:
        err = {"detail": resp.text}
    return jsonify({"ok": False, "message": err.get("detail", "Subscription failed.")}), 400

if __name__ == "__main__":
    app.run(debug=True)
