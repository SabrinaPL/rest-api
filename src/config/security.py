from flask_talisman import Talisman

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

    # Allow Swagger static files (CSS, JS etc.) to be loaded
    @app.after_request
    def add_swagger_headers(response):
        """
        Add specific headers to allow Flasgger's Swagger UI resources (JS, CSS, etc.) to be loaded.
        """
        if 'flasgger_static' in response.request.path:
            response.headers['X-Content-Type-Options'] = 'nosniff'  # Prevent content-type sniffing
            response.headers['Content-Security-Policy'] = "default-src 'self';"  # Relax CSP for Swagger
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['X-Frame-Options'] = 'ALLOW-FROM *'  # Allow the Swagger UI to be framed

        return response

    return talisman

