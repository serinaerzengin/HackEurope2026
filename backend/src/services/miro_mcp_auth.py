"""
OAuth 2.1 authentication for the official Miro MCP server (https://mcp.miro.com/).

Flow:
1. Dynamic client registration (one-time)
2. Authorization code flow with PKCE (browser opens, user logs in)
3. Token exchange and caching to disk
4. Refresh token support for subsequent uses
"""

import json
import hashlib
import secrets
import asyncio
import webbrowser
from pathlib import Path
from urllib.parse import urlencode

import httpx

MCP_BASE = "https://mcp.miro.com"
TOKEN_CACHE_FILE = Path(__file__).parent.parent.parent / ".miro_mcp_tokens.json"
CLIENT_CACHE_FILE = Path(__file__).parent.parent.parent / ".miro_mcp_client.json"
CALLBACK_PORT = 9876
REDIRECT_URI = f"http://localhost:{CALLBACK_PORT}/callback"


def _load_json(path: Path) -> dict | None:
    if path.exists():
        return json.loads(path.read_text())
    return None


def _save_json(path: Path, data: dict):
    path.write_text(json.dumps(data, indent=2))


async def _register_client() -> dict:
    """Dynamic client registration with the Miro MCP server."""
    cached = _load_json(CLIENT_CACHE_FILE)
    if cached and cached.get("client_id"):
        return cached

    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{MCP_BASE}/register",
            json={
                "client_name": "SystemInterviewAgent",
                "redirect_uris": [REDIRECT_URI],
                "grant_types": ["authorization_code", "refresh_token"],
                "response_types": ["code"],
                "token_endpoint_auth_method": "client_secret_post",
                "scope": "boards:read",
            },
            timeout=15,
        )
        r.raise_for_status()
        data = r.json()
        _save_json(CLIENT_CACHE_FILE, data)
        return data


async def _exchange_code(client_info: dict, code: str, code_verifier: str) -> dict:
    """Exchange authorization code for tokens."""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{MCP_BASE}/token",
            data={
                "grant_type": "authorization_code",
                "code": code,
                "redirect_uri": REDIRECT_URI,
                "client_id": client_info["client_id"],
                "client_secret": client_info["client_secret"],
                "code_verifier": code_verifier,
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        r.raise_for_status()
        tokens = r.json()
        _save_json(TOKEN_CACHE_FILE, tokens)
        return tokens


async def _refresh_tokens(client_info: dict, refresh_token: str) -> dict:
    """Refresh the access token using the refresh token."""
    async with httpx.AsyncClient() as client:
        r = await client.post(
            f"{MCP_BASE}/token",
            data={
                "grant_type": "refresh_token",
                "refresh_token": refresh_token,
                "client_id": client_info["client_id"],
                "client_secret": client_info["client_secret"],
            },
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            timeout=15,
        )
        if r.is_success:
            tokens = r.json()
            _save_json(TOKEN_CACHE_FILE, tokens)
            return tokens
        else:
            print(f"[miro_mcp_auth] Refresh failed: {r.status_code} {r.text}")
            return {}


async def _run_auth_flow(client_info: dict) -> dict:
    """
    Run the full OAuth authorization code flow with PKCE.
    Opens a browser for the user to log in, captures the callback.
    """
    # Generate PKCE values
    code_verifier = secrets.token_urlsafe(64)
    code_challenge = hashlib.sha256(code_verifier.encode()).digest()
    import base64

    code_challenge_b64 = base64.urlsafe_b64encode(code_challenge).rstrip(b"=").decode()

    state = secrets.token_urlsafe(32)

    # Build authorization URL
    auth_params = {
        "response_type": "code",
        "client_id": client_info["client_id"],
        "redirect_uri": REDIRECT_URI,
        "scope": "boards:read",
        "state": state,
        "code_challenge": code_challenge_b64,
        "code_challenge_method": "S256",
    }
    auth_url = f"{MCP_BASE}/authorize?{urlencode(auth_params)}"

    # Start a tiny HTTP server to capture the callback
    captured_code = None
    captured_error = None

    from aiohttp import web

    async def handle_callback(request):
        nonlocal captured_code, captured_error
        returned_state = request.query.get("state")
        if returned_state != state:
            captured_error = "State mismatch"
            return web.Response(
                text="Error: state mismatch. Close this tab.", status=400
            )

        error = request.query.get("error")
        if error:
            captured_error = f"{error}: {request.query.get('error_description', '')}"
            return web.Response(
                text=f"Error: {captured_error}. Close this tab.", status=400
            )

        captured_code = request.query.get("code")
        if not captured_code:
            captured_error = "No code in callback"
            return web.Response(
                text="Error: no authorization code. Close this tab.", status=400
            )

        return web.Response(
            text="<html><body><h2>Miro MCP authorized! You can close this tab.</h2></body></html>",
            content_type="text/html",
        )

    app = web.Application()
    app.router.add_get("/callback", handle_callback)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "localhost", CALLBACK_PORT)
    await site.start()

    print("[miro_mcp_auth] Opening browser for Miro authorization...")
    print(f"[miro_mcp_auth] If the browser doesn't open, visit: {auth_url}")
    webbrowser.open(auth_url)

    # Wait for callback (up to 120 seconds)
    for _ in range(240):
        if captured_code or captured_error:
            break
        await asyncio.sleep(0.5)

    await runner.cleanup()

    if captured_error:
        raise RuntimeError(f"Miro OAuth failed: {captured_error}")
    if not captured_code:
        raise RuntimeError("Miro OAuth timed out (120s). Please try again.")

    # Exchange code for tokens
    tokens = await _exchange_code(client_info, captured_code, code_verifier)
    print("[miro_mcp_auth] Successfully obtained Miro MCP tokens")
    return tokens


async def get_miro_mcp_access_token() -> str:
    """
    Get a valid access token for the Miro MCP server.
    Uses cached tokens if available, refreshes if expired, or runs full auth flow.
    """
    client_info = await _register_client()

    # Try cached tokens
    cached = _load_json(TOKEN_CACHE_FILE)
    if cached and cached.get("access_token"):
        # Try the token — if it works, great
        async with httpx.AsyncClient() as client:
            r = await client.post(
                f"{MCP_BASE}/",
                headers={
                    "Authorization": f"Bearer {cached['access_token']}",
                    "Content-Type": "application/json",
                },
                json={
                    "jsonrpc": "2.0",
                    "method": "initialize",
                    "id": 1,
                    "params": {
                        "protocolVersion": "2025-03-26",
                        "capabilities": {},
                        "clientInfo": {
                            "name": "SystemInterviewAgent",
                            "version": "1.0",
                        },
                    },
                },
                timeout=15,
            )
            if r.is_success:
                return cached["access_token"]

        # Token expired, try refresh
        if cached.get("refresh_token"):
            refreshed = await _refresh_tokens(client_info, cached["refresh_token"])
            if refreshed.get("access_token"):
                return refreshed["access_token"]

    # No valid tokens — run full auth flow
    tokens = await _run_auth_flow(client_info)
    return tokens["access_token"]
