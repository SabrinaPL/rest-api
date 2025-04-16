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
        referrer_policy="no-referrer",  # Enhances privacy
        content_security_policy={
            'default-src': "'self'",
            'script-src': ["'self'", "'unsafe-inline'", "https://cdnjs.cloudflare.com", "https://cdn.jsdelivr.net"],
            'style-src': ["'self'", "'unsafe-inline'", "https://fonts.googleapis.com", "https://cdn.jsdelivr.net"],
            'font-src': ["'self'", "https://fonts.gstatic.com"],
            'img-src': ["'self'", 'data:'],
            'connect-src': ["'self'"],
            'frame-ancestors': ["'none'"],
            'object-src': ["'none'"],
            'base-uri': ["'self'"]
        }
    )
    return talisman