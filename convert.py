#!/usr/bin/env python3
"""Converts VLESS URI lists from zieng2/wl to Stash-compatible YAML proxy provider format."""

import os
import sys
from typing import Optional
from urllib.parse import parse_qs, unquote
from urllib.request import urlopen
from urllib.error import URLError

import yaml

SOURCES = {
    "output/stash_lite.yaml": "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_lite.txt",
    "output/stash_universal.yaml": "https://raw.githubusercontent.com/zieng2/wl/refs/heads/main/vless_universal.txt",
}


def parse_vless_uri(uri: str) -> Optional[dict]:
    """Parse a single vless:// URI into a dict of components."""
    uri = uri.strip()
    if not uri or not uri.startswith("vless://"):
        return None

    # Split fragment (proxy name) from the rest
    if "#" in uri:
        main_part, fragment = uri.rsplit("#", 1)
        name = unquote(fragment).strip()
    else:
        main_part = uri
        name = "unnamed"

    # Remove scheme
    rest = main_part[len("vless://"):]

    # Split UUID from address+params
    if "@" not in rest:
        print(f"WARNING: No '@' in URI, skipping: {name}", file=sys.stderr)
        return None

    uuid_part, addr_part = rest.split("@", 1)

    # Split address from query string
    if "?" in addr_part:
        host_port, query_string = addr_part.split("?", 1)
    else:
        host_port = addr_part
        query_string = ""

    # Parse host:port (handle IPv6 [addr]:port)
    if host_port.startswith("["):
        bracket_end = host_port.find("]")
        if bracket_end == -1:
            print(f"WARNING: Malformed IPv6, skipping: {name}", file=sys.stderr)
            return None
        server = host_port[1:bracket_end]
        port_str = host_port[bracket_end + 2:]  # skip ]:
    else:
        if ":" not in host_port:
            print(f"WARNING: No port in URI, skipping: {name}", file=sys.stderr)
            return None
        server, port_str = host_port.rsplit(":", 1)

    try:
        port = int(port_str)
    except ValueError:
        print(f"WARNING: Invalid port '{port_str}', skipping: {name}", file=sys.stderr)
        return None

    # Parse query parameters
    params = {}
    if query_string:
        qs = parse_qs(query_string, keep_blank_values=True)
        for key, values in qs.items():
            params[key] = unquote(values[0])

    return {
        "uuid": uuid_part,
        "server": server,
        "port": port,
        "name": name,
        **params,
    }


def build_stash_proxy(parsed: dict) -> Optional[dict]:
    """Convert parsed VLESS URI dict into a Stash proxy config dict."""
    transport = parsed.get("type", "tcp")

    # Skip unsupported transports
    if transport == "xhttp":
        print(f"WARNING: Skipping unsupported transport 'xhttp': {parsed['name']}", file=sys.stderr)
        return None

    # Base fields
    proxy = {
        "name": parsed["name"],
        "type": "vless",
        "server": parsed["server"],
        "port": parsed["port"],
        "uuid": parsed["uuid"],
    }

    # Network (tcp is default, omit it)
    if transport in ("ws", "grpc", "h2"):
        proxy["network"] = transport

    # Security / TLS
    security = parsed.get("security", "none")
    if security in ("tls", "reality"):
        proxy["tls"] = True

    # Flow (XTLS)
    flow = parsed.get("flow")
    if flow:
        proxy["flow"] = flow

    # SNI
    sni = parsed.get("sni")
    if sni:
        proxy["sni"] = sni

    # Client fingerprint
    fp = parsed.get("fp")
    if fp:
        proxy["client-fingerprint"] = fp

    # ALPN
    alpn = parsed.get("alpn")
    if alpn:
        proxy["alpn"] = [a.strip() for a in alpn.split(",") if a.strip()]

    # Transport-specific options
    if transport == "ws":
        ws_opts = {}
        path = parsed.get("path")
        if path:
            ws_opts["path"] = path
        host = parsed.get("host")
        if host:
            ws_opts["headers"] = {"Host": host}
        if ws_opts:
            proxy["ws-opts"] = ws_opts

    elif transport == "grpc":
        service_name = parsed.get("serviceName")
        if service_name:
            proxy["grpc-opts"] = {"grpc-service-name": service_name}

    elif transport == "h2":
        h2_opts = {}
        path = parsed.get("path")
        if path:
            h2_opts["path"] = path
        host = parsed.get("host")
        if host:
            h2_opts["host"] = [host]
        if h2_opts:
            proxy["h2-opts"] = h2_opts

    # Reality options
    if security == "reality":
        reality = {}
        pbk = parsed.get("pbk")
        if pbk:
            reality["public-key"] = pbk
        sid = parsed.get("sid")
        if sid:
            reality["short-id"] = sid
        if reality:
            proxy["reality-opts"] = reality

    return proxy


def fetch_and_convert(url: str) -> list[dict]:
    """Fetch a VLESS text file and convert all entries to Stash proxy dicts."""
    print(f"Fetching {url} ...", file=sys.stderr)
    response = urlopen(url, timeout=30)
    text = response.read().decode("utf-8")
    lines = text.splitlines()

    proxies = []
    skipped = 0
    for line in lines:
        parsed = parse_vless_uri(line)
        if parsed is None:
            continue
        proxy = build_stash_proxy(parsed)
        if proxy is None:
            skipped += 1
            continue
        proxies.append(proxy)

    print(f"  Lines: {len(lines)}, Converted: {len(proxies)}, Skipped: {skipped}", file=sys.stderr)
    return proxies


def main():
    os.makedirs("output", exist_ok=True)

    total_converted = 0

    for output_file, source_url in SOURCES.items():
        try:
            proxies = fetch_and_convert(source_url)
        except (URLError, OSError) as e:
            print(f"ERROR: Failed to fetch {source_url}: {e}", file=sys.stderr)
            sys.exit(1)

        if not proxies:
            print(f"ERROR: 0 proxies converted from {source_url}", file=sys.stderr)
            sys.exit(1)

        data = {"proxies": proxies}
        with open(output_file, "w", encoding="utf-8") as f:
            yaml.dump(data, f, default_flow_style=False, allow_unicode=True, sort_keys=False, width=1000)

        total_converted += len(proxies)
        print(f"Written {len(proxies)} proxies to {output_file}", file=sys.stderr)

    print(f"\nDone. Total proxies converted: {total_converted}", file=sys.stderr)


if __name__ == "__main__":
    main()
