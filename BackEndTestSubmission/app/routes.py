from flask import request, jsonify, redirect, current_app as app
from . import db
from .models import ShortURL
import string, random, logging
from datetime import datetime

logger = logging.getLogger(__name__)

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

@app.route("/shorturls", methods=["POST"])
def shorten_url():
    data = request.get_json()
    long_url = data.get("long_url")
    custom_code = data.get("custom_code")
    valid_time = data.get("valid_time", 30)

    if not long_url:
        return jsonify({"error": "Missing 'long_url'"}), 400

    if custom_code:
        if ShortURL.query.filter_by(short_code=custom_code).first():
            return jsonify({"error": "Custom code already taken"}), 400
        short_code = custom_code
    else:
        while True:
            short_code = generate_short_code()
            if not ShortURL.query.filter_by(short_code=short_code).first():
                break

    url = ShortURL(long_url=long_url, short_code=short_code, valid_time=valid_time)
    db.session.add(url)
    db.session.commit()

    logger.info(f"Created short URL: {short_code} for {long_url}")
    return jsonify({
        "short_url": request.host_url + short_code,
        "valid_time": valid_time,
        "created_at": url.created_at.isoformat()
    }), 201


@app.route("/<string:short_code>", methods=["GET"])
def get_stats(short_code):
    url = ShortURL.query.filter_by(short_code=short_code).first()
    if not url:
        return jsonify({"error": "Short URL not found"}), 404

    return jsonify({
        "long_url": url.long_url,
        "short_code": url.short_code,
        "clicks": url.clicks,
        "valid_time": url.valid_time,
        "created_at": url.created_at.isoformat(),
        "is_valid": url.is_valid()
    })
