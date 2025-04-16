from flask_talisman import Talisman
from flask import request

def configure_talisman(app):
    """
    Configures Flask-Talisman for security headers.
    """
    talisman = Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,  # 1 year
        frame_options="DENY",  # Prevents clickjacking
        session_cookie_secure=True,  # Ensures cookies are only sent over HTTPS
        session_cookie_http_only=True,  # Protects against XSS
        referrer_policy="no-referrer"  # Enhances privacy
    )

    @app.after_request
    def add_swagger_headers(response):
        """
        Add specific headers to allow Flasgger's Swagger UI resources (JS, CSS, etc.) to be loaded.
        """
        if 'flasgger_static' in request.path:
            return response  # Don't modify headers for Flasgger static assets

        # These headers apply to other responses
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['Content-Security-Policy'] = "default-src 'self';"
        response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
        response.headers['X-Frame-Options'] = 'ALLOW-FROM *'  # or DENY, depending on your use case

        return response

    return talisman

