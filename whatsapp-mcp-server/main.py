from typing import List, Dict, Any, Optional, Union
from mcp.server.fastmcp import FastMCP
from whatsapp import (
    search_contacts as whatsapp_search_contacts,
    list_messages as whatsapp_list_messages,
    list_chats as whatsapp_list_chats,
    get_chat as whatsapp_get_chat,
    get_direct_chat_by_contact as whatsapp_get_direct_chat_by_contact,
    get_contact_chats as whatsapp_get_contact_chats,
    get_last_interaction as whatsapp_get_last_interaction,
    get_message_context as whatsapp_get_message_context,
    send_message as whatsapp_send_message,
    send_file as whatsapp_send_file,
    send_audio_message as whatsapp_audio_voice_message,
    download_media as whatsapp_download_media
)

# Initialize FastMCP server
mcp = FastMCP("whatsapp")

@mcp.tool()
def search_contacts(query: str) -> List[Dict[str, Any]]:
    """Search WhatsApp contacts by name or phone number.
    
    Args:
        query: Search term to match against contact names or phone numbers
    """
    contacts = whatsapp_search_contacts(query)
    return contacts

@mcp.tool()
def list_messages(
    after: Optional[str] = None,
    before: Optional[str] = None,
    sender_phone_number: Optional[str] = None,
    chat_jid: Optional[str] = None,
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_context: bool = True,
    context_before: int = 1,
    context_after: int = 1
) -> List[Dict[str, Any]]:
    """Get WhatsApp messages matching specified criteria with optional context.
    
    Args:
        after: Optional ISO-8601 formatted string to only return messages after this date
        before: Optional ISO-8601 formatted string to only return messages before this date
        sender_phone_number: Optional phone number to filter messages by sender
        chat_jid: Optional chat JID to filter messages by chat
        query: Optional search term to filter messages by content
        limit: Maximum number of messages to return (default 20)
        page: Page number for pagination (default 0)
        include_context: Whether to include messages before and after matches (default True)
        context_before: Number of messages to include before each match (default 1)
        context_after: Number of messages to include after each match (default 1)
    """
    messages = whatsapp_list_messages(
        after=after,
        before=before,
        sender_phone_number=sender_phone_number,
        chat_jid=chat_jid,
        query=query,
        limit=limit,
        page=page,
        include_context=include_context,
        context_before=context_before,
        context_after=context_after
    )
    return messages

@mcp.tool()
def list_chats(
    query: Optional[str] = None,
    limit: int = 20,
    page: int = 0,
    include_last_message: bool = True,
    sort_by: str = "last_active"
) -> List[Dict[str, Any]]:
    """Get WhatsApp chats matching specified criteria.
    
    Args:
        query: Optional search term to filter chats by name or JID
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
        include_last_message: Whether to include the last message in each chat (default True)
        sort_by: Field to sort results by, either "last_active" or "name" (default "last_active")
    """
    chats = whatsapp_list_chats(
        query=query,
        limit=limit,
        page=page,
        include_last_message=include_last_message,
        sort_by=sort_by
    )
    return chats

@mcp.tool()
def get_chat(chat_jid: str, include_last_message: bool = True) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by JID.
    
    Args:
        chat_jid: The JID of the chat to retrieve
        include_last_message: Whether to include the last message (default True)
    """
    chat = whatsapp_get_chat(chat_jid, include_last_message)
    return chat

@mcp.tool()
def get_direct_chat_by_contact(sender_phone_number: str) -> Dict[str, Any]:
    """Get WhatsApp chat metadata by sender phone number.
    
    Args:
        sender_phone_number: The phone number to search for
    """
    chat = whatsapp_get_direct_chat_by_contact(sender_phone_number)
    return chat

@mcp.tool()
def get_contact_chats(jid: str, limit: int = 20, page: int = 0) -> List[Dict[str, Any]]:
    """Get all WhatsApp chats involving the contact.
    
    Args:
        jid: The contact's JID to search for
        limit: Maximum number of chats to return (default 20)
        page: Page number for pagination (default 0)
    """
    chats = whatsapp_get_contact_chats(jid, limit, page)
    return chats

@mcp.tool()
def get_last_interaction(jid: str) -> Optional[Dict[str, Any]]:
    """Get most recent WhatsApp message involving the contact.
    
    Args:
        jid: The JID of the contact to search for
    """
    message = whatsapp_get_last_interaction(jid)
    return message

@mcp.tool()
def get_message_context(
    message_id: str,
    before: int = 5,
    after: int = 5
) -> Dict[str, Any]:
    """Get context around a specific WhatsApp message.
    
    Args:
        message_id: The ID of the message to get context for
        before: Number of messages to include before the target message (default 5)
        after: Number of messages to include after the target message (default 5)
    """
    context = whatsapp_get_message_context(message_id, before, after)
    return context

@mcp.tool()
def send_message(
    recipient: str,
    message: str
) -> Dict[str, Any]:
    """Send a WhatsApp message to a person or group. For group chats use the JID.

    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        message: The message text to send
    
    Returns:
        A dictionary containing success status and a status message
    """
    # Validate input
    if not recipient:
        return {
            "success": False,
            "message": "Recipient must be provided"
        }
    
    # Call the whatsapp_send_message function with the unified recipient parameter
    success, status_message = whatsapp_send_message(recipient, message)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_file(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send a file such as a picture, raw audio, video or document via WhatsApp to the specified recipient. For group messages use the JID.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the media file to send (image, video, document)
    
    Returns:
        A dictionary containing success status and a status message
    """
    
    # Call the whatsapp_send_file function
    success, status_message = whatsapp_send_file(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def send_audio_message(recipient: str, media_path: str) -> Dict[str, Any]:
    """Send any audio file as a WhatsApp audio message to the specified recipient. For group messages use the JID. If it errors due to ffmpeg not being installed, use send_file instead.
    
    Args:
        recipient: The recipient - either a phone number with country code but no + or other symbols,
                 or a JID (e.g., "123456789@s.whatsapp.net" or a group JID like "123456789@g.us")
        media_path: The absolute path to the audio file to send (will be converted to Opus .ogg if it's not a .ogg file)
    
    Returns:
        A dictionary containing success status and a status message
    """
    success, status_message = whatsapp_audio_voice_message(recipient, media_path)
    return {
        "success": success,
        "message": status_message
    }

@mcp.tool()
def download_media(message_id: str, chat_jid: str) -> Dict[str, Any]:
    """Download media from a WhatsApp message and get the local file path.
    
    Args:
        message_id: The ID of the message containing the media
        chat_jid: The JID of the chat containing the message
    
    Returns:
        A dictionary containing success status, a status message, and the file path if successful
    """
    file_path = whatsapp_download_media(message_id, chat_jid)
    
    if file_path:
        return {
            "success": True,
            "message": "Media downloaded successfully",
            "file_path": file_path
        }
    else:
        return {
            "success": False,
            "message": "Failed to download media"
        }

def _run_sse() -> None:
    import logging
    import os
    import time

    import httpx as _httpx
    import uvicorn
    from mcp.server.sse import SseServerTransport
    from starlette.applications import Starlette
    from starlette.middleware.base import BaseHTTPMiddleware
    from starlette.requests import Request
    from starlette.responses import Response
    from starlette.routing import Mount, Route

    # ------------------------------------------------------------------
    # Logging – LOG_LEVEL env var (debug|info|warning|error). Use DEBUG to
    # see every incoming request, the full auth decision path and the
    # SSE connection lifecycle.
    # ------------------------------------------------------------------
    _log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    _level_int = getattr(logging, _log_level, logging.INFO)
    # `force=True` is required because uvicorn / FastMCP install root
    # handlers before we get here, which would make a plain basicConfig()
    # silently a no-op (and DEBUG lines would never show up).
    logging.basicConfig(
        level=_level_int,
        format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
        force=True,
    )
    # Belt-and-braces: explicitly set our logger AND the root logger, so
    # logs from inside library callbacks honour the level too.
    logging.getLogger().setLevel(_level_int)
    log = logging.getLogger("whatsapp-mcp")
    log.setLevel(_level_int)
    # Make sure uvicorn's own loggers don't drown out / override us.
    for name in ("uvicorn", "uvicorn.error", "uvicorn.access"):
        logging.getLogger(name).setLevel(_level_int)

    mcp_api_key = os.getenv("MCP_API_KEY", "")
    oidc_introspection_url = os.getenv("OIDC_INTROSPECTION_URL", "")
    oidc_client_id = os.getenv("OIDC_CLIENT_ID", "")
    oidc_client_secret = os.getenv("OIDC_CLIENT_SECRET", "")

    auth_configured = bool(mcp_api_key) or all(
        (oidc_introspection_url, oidc_client_id, oidc_client_secret)
    )

    log.info(
        "[auth] config: MCP_API_KEY=%s OIDC_INTROSPECTION_URL=%s OIDC_CLIENT_ID=%s OIDC_CLIENT_SECRET=%s",
        f"set({len(mcp_api_key)} chars)" if mcp_api_key else "NOT SET",
        oidc_introspection_url or "NOT SET",
        oidc_client_id or "NOT SET",
        f"set({len(oidc_client_secret)} chars)" if oidc_client_secret else "NOT SET",
    )
    if not auth_configured:
        log.warning(
            "[auth] NEITHER static MCP_API_KEY NOR a complete OIDC triple is configured – ALL requests will pass unauthenticated."
        )

    def _auth_preview(auth: str) -> str:
        if not auth:
            return "(none)"
        return auth[:20] + ("…" if len(auth) > 20 else "")

    # Auth result: (ok, reason). reason ∈ {None, "no_header", "invalid_token"}.
    # Used by _unauthorized() to build the right WWW-Authenticate hint so
    # Claude.ai can distinguish "refresh your token" from "start over".
    async def _is_authorized(request: Request) -> tuple[bool, str | None]:
        tag = f"{request.method} {request.url.path}"
        auth = request.headers.get("Authorization", "")
        log.debug("[auth] %s – Authorization: %s", tag, _auth_preview(auth))

        if not mcp_api_key:
            log.debug("[auth] %s – no MCP_API_KEY configured, passing through", tag)
            return True, None
        if not auth:
            log.warning("[auth] %s – DENY: no Authorization header", tag)
            return False, "no_header"
        if auth == f"Bearer {mcp_api_key}":
            log.info("[auth] %s – OK: static MCP_API_KEY matched", tag)
            return True, None
        if not auth.startswith("Bearer "):
            log.warning("[auth] %s – DENY: Authorization is not a Bearer scheme", tag)
            return False, "invalid_token"
        if not (oidc_introspection_url and oidc_client_id and oidc_client_secret):
            log.warning(
                "[auth] %s – DENY: Bearer JWT presented but OIDC introspection not fully configured (url=%s id=%s secret=%s)",
                tag,
                "ok" if oidc_introspection_url else "MISSING",
                "ok" if oidc_client_id else "MISSING",
                "ok" if oidc_client_secret else "MISSING",
            )
            return False, "invalid_token"

        jwt_token = auth[7:]
        log.debug(
            "[auth] %s – introspecting token (len=%d) against %s",
            tag,
            len(jwt_token),
            oidc_introspection_url,
        )
        started = time.monotonic()
        try:
            async with _httpx.AsyncClient(timeout=5.0) as http:
                resp = await http.post(
                    oidc_introspection_url,
                    data={"token": jwt_token},
                    auth=(oidc_client_id, oidc_client_secret),
                )
                elapsed_ms = int((time.monotonic() - started) * 1000)
                body = resp.text
                log.debug(
                    "[auth] %s – introspection HTTP %s in %dms, body: %s",
                    tag,
                    resp.status_code,
                    elapsed_ms,
                    body[:300],
                )
                if resp.status_code != 200:
                    log.warning(
                        "[auth] %s – DENY: introspection returned non-200 (%s)",
                        tag,
                        resp.status_code,
                    )
                    return False, "invalid_token"
                data = resp.json()
                active = bool(data.get("active"))
                if active:
                    log.info(
                        "[auth] %s – OK: OIDC token active sub=%s scope=%s",
                        tag,
                        data.get("sub", "?"),
                        data.get("scope", "?"),
                    )
                    return True, None
                log.warning("[auth] %s – DENY: OIDC token not active", tag)
                return False, "invalid_token"
        except Exception as e:
            elapsed_ms = int((time.monotonic() - started) * 1000)
            log.error(
                "[auth] %s – introspection exception after %dms: %s",
                tag,
                elapsed_ms,
                e,
            )
            return False, "invalid_token"

    def _unauthorized(reason: str | None) -> Response:
        """Build a 401. With reason="invalid_token" we add an RFC 6750
        WWW-Authenticate hint so the OAuth client runs the silent
        refresh-token flow. With reason="no_header" we deliberately
        omit the header – sending `Bearer realm="..."` would
        short-circuit Claude.ai's OAuth discovery."""
        if reason == "invalid_token":
            www = (
                'Bearer realm="whatsapp-mcp", error="invalid_token", '
                'error_description="The access token expired or is invalid"'
            )
            return Response(
                "Unauthorized",
                status_code=401,
                headers={"WWW-Authenticate": www},
            )
        return Response("Unauthorized", status_code=401)

    class RequestLogMiddleware(BaseHTTPMiddleware):
        """Logs every request that hits the app, even ones that 404 in routing."""

        async def dispatch(self, request, call_next):  # type: ignore[override]
            t0 = time.monotonic()
            log.debug(
                "→ %s %s  ip=%s  ua=%s  auth=%s",
                request.method,
                request.url.path,
                request.client.host if request.client else "?",
                request.headers.get("user-agent", "?")[:60],
                _auth_preview(request.headers.get("Authorization", "")),
            )
            try:
                response = await call_next(request)
            except Exception:
                log.exception(
                    "← %s %s – handler raised", request.method, request.url.path
                )
                raise
            dt_ms = int((time.monotonic() - t0) * 1000)
            log.debug(
                "← %s %s → %d  in %dms",
                request.method,
                request.url.path,
                response.status_code,
                dt_ms,
            )
            return response

    sse = SseServerTransport("/messages/")
    _server = mcp._mcp_server

    # Modern Claude.ai connects with Streamable-HTTP semantics
    # (POST /sse with a real JSON-RPC payload, not a probe). We MUST
    # speak Streamable-HTTP on that path or the connector cannot
    # initialise. Mount the SDK's StreamableHTTPServerTransport in
    # stateless mode (one transport per request – fits FastMCP's
    # request-scoped tools).
    import anyio
    from mcp.server.streamable_http import StreamableHTTPServerTransport

    class _AlreadySent(Response):
        """No-op response for handlers that have already streamed their
        full response via the raw ASGI `send` callable. Returning a
        regular Response would make Starlette try to send a second one
        and crash with 'response already completed'."""

        def __init__(self) -> None:
            super().__init__(content=b"", status_code=200)

        async def __call__(self, scope, receive, send):  # noqa: D401
            return

    async def handle_streamable_http(request: Request):
        ok, reason = await _is_authorized(request)
        if not ok:
            log.warning("[/sse POST] denied (unauthenticated) reason=%s", reason)
            return _unauthorized(reason)
        log.info(
            "[/sse POST] streamable-http request from %s",
            request.client.host if request.client else "?",
        )

        # ASGI pattern: a Starlette endpoint must return a Response, but
        # StreamableHTTPServerTransport.handle_request writes the response
        # to the ASGI `send` callable directly. Using `request._send`
        # is the same trick we already use for SSE.
        transport = StreamableHTTPServerTransport(
            mcp_session_id=None, is_json_response_enabled=True
        )
        try:
            async with transport.connect() as streams:
                async with anyio.create_task_group() as tg:

                    async def _run_server():
                        try:
                            await _server.run(
                                streams[0],
                                streams[1],
                                _server.create_initialization_options(),
                            )
                        except Exception:
                            log.exception("[/sse POST] server.run crashed")

                    tg.start_soon(_run_server)
                    await transport.handle_request(
                        request.scope, request.receive, request._send
                    )
                    tg.cancel_scope.cancel()
        except Exception:
            log.exception("[/sse POST] streamable-http handler error")
            raise
        # Response already written via request._send – returning a normal
        # Response would crash with "response already completed".
        return _AlreadySent()

    sessions: dict[str, float] = {}

    async def handle_sse(request: Request):
        client_ip = request.client.host if request.client else "?"
        log.info("[/sse GET] new SSE connection from %s", client_ip)
        ok, reason = await _is_authorized(request)
        if not ok:
            log.warning("[/sse GET] denied (unauthenticated) from %s reason=%s", client_ip, reason)
            return _unauthorized(reason)
        opened = time.monotonic()
        try:
            async with sse.connect_sse(
                request.scope, request.receive, request._send
            ) as streams:
                # Track the live session for visibility.
                session_id = str(id(streams))
                sessions[session_id] = opened
                log.info(
                    "[/sse GET] stream open  session=%s  active_sessions=%d",
                    session_id,
                    len(sessions),
                )
                try:
                    await _server.run(
                        streams[0], streams[1], _server.create_initialization_options()
                    )
                finally:
                    duration = int(time.monotonic() - sessions.pop(session_id, opened))
                    log.info(
                        "[/sse GET] stream closed session=%s after %ds  remaining=%d",
                        session_id,
                        duration,
                        len(sessions),
                    )
        except Exception:
            log.exception("[/sse GET] handler crashed")
            raise
        # Must return Response() – otherwise Starlette calls None() on disconnect
        # and logs "Exception in ASGI application" (MCP SDK >= 1.6 requirement)
        return Response()

    # /messages/{session_id} – authenticate too, so we get logs on those POSTs.
    async def handle_messages(scope, receive, send):  # ASGI app wrapper
        from starlette.requests import Request as _Req

        req = _Req(scope, receive=receive)
        ok, reason = await _is_authorized(req)
        if not ok:
            response = _unauthorized(reason)
            await response(scope, receive, send)
            return
        log.debug(
            "[/messages POST] session_id=%s",
            req.query_params.get("session_id", "?"),
        )
        await sse.handle_post_message(scope, receive, send)

    from starlette.middleware import Middleware

    # Pass the middleware via the constructor (rather than add_middleware
    # afterwards) so it definitely wraps the routing layer – otherwise the
    # debug request log silently misses 4xx responses produced by Starlette
    # itself (e.g. method-not-allowed on POST /sse).
    app = Starlette(
        routes=[
            # Streamable-HTTP (current spec) – Claude.ai uses this first.
            Route("/sse", endpoint=handle_streamable_http, methods=["POST"]),
            Route("/mcp", endpoint=handle_streamable_http, methods=["POST"]),
            # Classic SSE transport – fallback for Claude Desktop / older clients.
            Route("/sse", endpoint=handle_sse, methods=["GET"]),
            Mount("/messages/", app=handle_messages),
        ],
        middleware=[Middleware(RequestLogMiddleware)],
    )

    port = int(os.getenv("PORT", "8000"))
    log.info("whatsapp-mcp listening on :%d (LOG_LEVEL=%s)", port, _log_level)
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    import os
    if os.getenv("MCP_TRANSPORT", "stdio") == "sse":
        _run_sse()
    else:
        mcp.run(transport='stdio')