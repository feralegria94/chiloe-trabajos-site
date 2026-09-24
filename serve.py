#!/usr/bin/env python3
"""Servidor local endurecido para Chiloé Trabajos :8100 — solo archivos estáticos + headers de seguridad."""
import http.server
import functools

DOCROOT = "/var/www/dev/chiloe-trabajos"
PORT = 8100

SECURITY_HEADERS = {
    "X-Content-Type-Options": "nosniff",
    "X-Frame-Options": "SAMEORIGIN",
    "Referrer-Policy": "strict-origin-when-cross-origin",
    "Permissions-Policy": "camera=(), microphone=(), geolocation=()",
    "Content-Security-Policy": (
        "default-src 'self'; "
        "style-src 'self' 'unsafe-inline'; "
        "script-src 'self' 'unsafe-inline'; "
        "img-src 'self' data:; "
        "media-src 'self'; "
        "font-src 'self'; "
        "connect-src 'self'; "
        "frame-ancestors 'self'; "
        "form-action 'none'; "
        "base-uri 'self'"
    ),
    "Cache-Control": "public, max-age=3600",
}


class SecureHandler(http.server.SimpleHTTPRequestHandler):
    def end_headers(self):
        for k, v in SECURITY_HEADERS.items():
            self.send_header(k, v)
        super().end_headers()

    def log_message(self, *args):
        pass


if __name__ == "__main__":
    srv = http.server.ThreadingHTTPServer(
        ("0.0.0.0", PORT),
        functools.partial(SecureHandler, directory=DOCROOT),
    )
    srv.serve_forever()
