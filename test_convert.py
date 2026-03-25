"""Unit tests for convert.py — VLESS URI parsing and Stash proxy building."""

from convert import parse_vless_uri, build_stash_proxy


# ── parse_vless_uri ──────────────────────────────────────────────


def test_parse_basic_tcp():
    uri = "vless://uuid-1234@example.com:443?type=tcp&security=tls&sni=example.com#MyProxy"
    result = parse_vless_uri(uri)
    assert result is not None
    assert result["uuid"] == "uuid-1234"
    assert result["server"] == "example.com"
    assert result["port"] == 443
    assert result["name"] == "MyProxy"
    assert result["type"] == "tcp"
    assert result["security"] == "tls"
    assert result["sni"] == "example.com"


def test_parse_ipv6():
    uri = "vless://uuid-1234@[2001:db8::1]:8443?type=tcp&security=none#IPv6-Proxy"
    result = parse_vless_uri(uri)
    assert result is not None
    assert result["server"] == "2001:db8::1"
    assert result["port"] == 8443
    assert result["name"] == "IPv6-Proxy"


def test_parse_websocket_with_path():
    uri = "vless://uuid@host.com:443?type=ws&security=tls&path=%2Fws&host=cdn.com#WS"
    result = parse_vless_uri(uri)
    assert result is not None
    assert result["type"] == "ws"
    assert result["path"] == "/ws"
    assert result["host"] == "cdn.com"


def test_parse_no_fragment_gets_unnamed():
    uri = "vless://uuid@host.com:443?type=tcp"
    result = parse_vless_uri(uri)
    assert result is not None
    assert result["name"] == "unnamed"


def test_parse_empty_string():
    assert parse_vless_uri("") is None


def test_parse_non_vless_scheme():
    assert parse_vless_uri("vmess://something") is None


def test_parse_no_at_sign():
    assert parse_vless_uri("vless://no-at-sign") is None


def test_parse_no_port():
    assert parse_vless_uri("vless://uuid@host.com#NoPort") is None


def test_parse_invalid_port():
    assert parse_vless_uri("vless://uuid@host.com:abc#BadPort") is None


def test_parse_malformed_ipv6():
    assert parse_vless_uri("vless://uuid@[2001:db8::1:443#Broken") is None


# ── build_stash_proxy ────────────────────────────────────────────


def test_build_tcp_tls():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "tcp-tls",
        "type": "tcp",
        "security": "tls",
        "sni": "example.com",
        "fp": "chrome",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["type"] == "vless"
    assert proxy["tls"] is True
    assert proxy["sni"] == "example.com"
    assert proxy["client-fingerprint"] == "chrome"
    assert "network" not in proxy  # tcp is default, omitted


def test_build_websocket():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "ws-proxy",
        "type": "ws",
        "security": "tls",
        "path": "/ws",
        "host": "cdn.example.com",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["network"] == "ws"
    assert proxy["ws-opts"]["path"] == "/ws"
    assert proxy["ws-opts"]["headers"]["Host"] == "cdn.example.com"


def test_build_grpc():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "grpc-proxy",
        "type": "grpc",
        "security": "tls",
        "serviceName": "my-grpc",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["network"] == "grpc"
    assert proxy["grpc-opts"]["grpc-service-name"] == "my-grpc"


def test_build_h2():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "h2-proxy",
        "type": "h2",
        "security": "tls",
        "path": "/h2path",
        "host": "h2.example.com",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["network"] == "h2"
    assert proxy["h2-opts"]["path"] == "/h2path"
    assert proxy["h2-opts"]["host"] == ["h2.example.com"]


def test_build_reality():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "reality-proxy",
        "type": "tcp",
        "security": "reality",
        "pbk": "public-key-value",
        "sid": "short-id-value",
        "sni": "reality.example.com",
        "fp": "chrome",
        "flow": "xtls-rprx-vision",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["tls"] is True
    assert proxy["flow"] == "xtls-rprx-vision"
    assert proxy["reality-opts"]["public-key"] == "public-key-value"
    assert proxy["reality-opts"]["short-id"] == "short-id-value"


def test_build_alpn_split():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "alpn-proxy",
        "type": "tcp",
        "security": "tls",
        "alpn": "h2,http/1.1",
    }
    proxy = build_stash_proxy(parsed)
    assert proxy is not None
    assert proxy["alpn"] == ["h2", "http/1.1"]


def test_build_skips_xhttp():
    parsed = {
        "uuid": "test-uuid",
        "server": "1.2.3.4",
        "port": 443,
        "name": "xhttp-proxy",
        "type": "xhttp",
    }
    assert build_stash_proxy(parsed) is None
