from flask_talisman import Talisman
from flask import request

# Define CSP dictionaries
DEFAULT_CSP = {
    'default-src': "'self'",
    'script-src': "'self'",
    'style-src': "'self'",
    'font-src': "'self'",
    'img-src': "'self'",
    'connect-src': "'self'",
    'frame-ancestors': "'none'",
    'object-src': "'none'",
    'base-uri': "'self'"
}

SWAGGER_CSP = {
    'default-src': "'self'",
    'script-src': [
        "'self'", "'unsafe-inline'",
        'https://cdnjs.cloudflare.com',
        'https://cdn.jsdelivr.net'
    ],
    'style-src': [
        "'self'", "'unsafe-inline'",
        'https://fonts.googleapis.com',
        'https://cdn.jsdelivr.net'
    ],
    'font-src': [
        "'self'",
        'https://fonts.gstatic.com',
        'https://migaku-public-data.migaku.com'
    ],
    'img-src': ["'self'", 'data:'],
    'connect-src': ["'self'"],
    'frame-ancestors': ["'none'"],
    'object-src': ["'none'"],
    'base-uri': ["'self'"]
}

def build_csp_header(csp_dict):
    """
    Converts a dict-style CSP into a valid CSP header string.
    """
    parts = []
    for directive, value in csp_dict.items():
        if isinstance(value, list):
            value = ' '.join(value)
        parts.append(f"{directive} {value}")
    return '; '.join(parts)

def dynamic_csp():
    """
    Function passed to Talisman to set the CSP dynamically per request.
    """
    path = request.path
    if path.startswith("/apidocs") or path.startswith("/flasgger_static"):
        return SWAGGER_CSP
    return DEFAULT_CSP

def configure_talisman(app):
    # Talisman uses the callable to decide CSP per request
    Talisman(
        app,
        content_security_policy=dynamic_csp,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        frame_options="DENY",
        session_cookie_secure=True,
        session_cookie_http_only=True,
        referrer_policy="no-referrer"
    )
    return app
