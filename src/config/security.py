from flask_talisman import Talisman
from flask import request

def configure_talisman(app):
    """
    Configures Flask-Talisman with relaxed CSP headers for Swagger UI.
    """
    talisman = Talisman(
        app,
        force_https=True,
        strict_transport_security=True,
        strict_transport_security_max_age=31536000,
        frame_options="DENY",
        session_cookie_secure=True,
        session_cookie_http_only=True,
        referrer_policy="no-referrer"
    )

    @app.after_request
    def add_swagger_headers(response):
        """
        Add CSP and other headers allowing Flasgger Swagger UI to function.
        """
        if 'flasgger_static' in request.path or '/apidocs' in request.path:
            print("Adding relaxed CSP headers for Swagger route: {request.path}")
            response.headers['Content-Security-Policy'] = (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-inline' https://cdnjs.cloudflare.com https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com https://cdn.jsdelivr.net; "
                "font-src 'self' https://fonts.gstatic.com https://migaku-public-data.migaku.com; "
                "img-src 'self' data:; "
                "connect-src 'self'; "
                "frame-ancestors 'none'; "
                "object-src 'none'; "
                "base-uri 'self';" 
        )

        else:
            print("Adding strict CSP headers for non-Swagger route: {request.path}")
            response.headers['Content-Security-Policy'] = "default-src 'self';"
            response.headers['Strict-Transport-Security'] = 'max-age=31536000; includeSubDomains'
            response.headers['X-Content-Type-Options'] = 'nosniff'
            response.headers['X-Frame-Options'] = 'DENY'

        return response

    return talisman

