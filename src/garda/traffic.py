"""Privacy-safe server-side page-view events for the proxied Garda host.

Cloud Run's standard request log sees a Cloudflare edge address for
``garda.simon-stieber.de``. The application therefore turns Cloudflare's
authenticated client-IP header into a stable HMAC before writing one
structured event. The raw address is never written by this module.

``garda.s1st.de`` bypasses Cloudflare and already has the real remote address
in Cloud Run's standard request log, so it deliberately does not emit a second
application event. The private stats dashboard combines both sources.
"""
from __future__ import annotations

import hashlib
import hmac
import ipaddress
import json
import re

BOT_RX = re.compile(
    r"bot|crawler|spider|HeadlessChrome|GoogleHC|kube-probe|UptimeRobot|"
    r"googlebot|bingbot|yandex|baidu|ahrefs|semrush|pingdom|datadog|monitis|"
    r"python-requests|curl|wget|Go-http-client|okhttp|libwww|Java/|"
    r"Read-Aloud",
    re.I,
)
EXPLOIT_RX = re.compile(
    r"\.(php|git|env|aspx?)|/admin|/wp-|/xmlrpc|/setup|/login\.|/owa|"
    r"/manager|/phpunit|credentials|parameters\.yml|settings\.py|"
    r"config\.json|config/application",
)


def normalize_ip(ip: str) -> str:
    """Return IPv4 unchanged and collapse IPv6 privacy addresses to /64."""
    if not ip:
        return ""
    try:
        address = ipaddress.ip_address(ip)
    except ValueError:
        return ""
    if address.version == 6:
        network = ipaddress.IPv6Network((int(address) & ((1 << 128) - (1 << 64)), 64))
        return f"{network.network_address}/64"
    return str(address)


def visitor_key(ip: str, secret: str) -> str:
    """Return a non-reversible stable identifier for one normalized address."""
    normalized = normalize_ip(ip)
    if not normalized or not secret:
        return ""
    digest = hmac.new(secret.encode(), normalized.encode(), hashlib.sha256).hexdigest()
    return digest[:32]


def build_page_view_event(
    *,
    method: str,
    status_code: int,
    content_type: str,
    user_agent: str,
    path: str,
    host: str,
    client_ip: str,
    hash_secret: str,
) -> dict[str, str] | None:
    """Build one structured event, or ``None`` for non-human/non-page traffic."""
    if method != "GET" or status_code >= 400:
        return None
    if not content_type.lower().startswith("text/html"):
        return None
    if not user_agent.startswith("Mozilla/") or BOT_RX.search(user_agent):
        return None
    if EXPLOIT_RX.search(path):
        return None
    visitor = visitor_key(client_ip, hash_secret)
    if not visitor:
        return None
    return {
        "event": "garda_page_view",
        "visitor": visitor,
        "host": host,
        "path": path,
    }


def emit_page_view(**values: str | int) -> None:
    """Write one JSON line so Cloud Logging stores it as ``jsonPayload``."""
    event = build_page_view_event(**values)  # type: ignore[arg-type]
    if event is not None:
        print(json.dumps(event, separators=(",", ":"), sort_keys=True), flush=True)
