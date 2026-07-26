"""Privacy and filtering guarantees for Garda's structured traffic events."""

from garda.traffic import build_page_view_event, normalize_ip, visitor_key

_UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) Safari/605.1.15"


def _event(**changes):
    values = {
        "method": "GET",
        "status_code": 200,
        "content_type": "text/html; charset=utf-8",
        "user_agent": _UA,
        "path": "/go/sca",
        "host": "garda.simon-stieber.de",
        "client_ip": "84.151.20.7",
        "hash_secret": "unit-test-secret",
    }
    values.update(changes)
    return build_page_view_event(**values)


def test_normalize_ip_and_hmac_are_stable_without_exposing_ip():
    assert normalize_ip("84.151.20.7") == "84.151.20.7"
    assert normalize_ip("2001:a61:1:2:aaaa:bbbb:cccc:dddd") == "2001:a61:1:2::/64"
    assert visitor_key("84.151.20.7", "secret") == visitor_key("84.151.20.7", "secret")
    assert visitor_key("84.151.20.7", "secret") != visitor_key("84.151.20.8", "secret")
    assert "84.151.20.7" not in visitor_key("84.151.20.7", "secret")


def test_page_view_event_contains_only_pseudonymous_fields():
    event = _event()
    assert event == {
        "event": "garda_page_view",
        "visitor": visitor_key("84.151.20.7", "unit-test-secret"),
        "host": "garda.simon-stieber.de",
        "path": "/go/sca",
    }
    assert "client_ip" not in event
    assert "user_agent" not in event


def test_page_view_event_filters_non_pages_bots_and_scanners():
    assert _event(method="POST") is None
    assert _event(status_code=404) is None
    assert _event(content_type="application/json") is None
    assert _event(user_agent="curl/8.0") is None
    assert _event(user_agent=f"{_UA} Google-Read-Aloud") is None
    assert _event(path="/wp-admin/setup.php") is None
    assert _event(client_ip="") is None
    assert _event(hash_secret="") is None
