from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request, HTTPException, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from spotdl_runner import run_spotdl
from add_to_playlist import add_to_playlist
from config import settings
import asyncio
import hashlib
import secrets
from typing import Dict

app = FastAPI()

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Simple session storage (in production, use Redis or database)
active_sessions: Dict[str, bool] = {}

def create_session_token() -> str:
    """Create a secure session token"""
    return secrets.token_urlsafe(32)

def verify_pin(pin: str) -> bool:
    """Verify if the provided PIN is correct"""
    return pin == settings.PIN

def get_session_token(request: Request) -> str:
    """Get session token from cookies"""
    token = request.cookies.get("session_token", "")
    print(f"🍪 Retrieved session token: '{token[:20] if token else 'None'}...'")
    return token

def is_authenticated(request: Request) -> bool:
    """Check if the request is authenticated"""
    session_token = get_session_token(request)
    print(f"🔍 Checking authentication: token='{session_token[:20] if session_token else 'None'}...'")

    if not session_token:
        print("❌ No session token found")
        return False

    if session_token not in active_sessions:
        print(f"❌ Session token not in active sessions. Available: {list(active_sessions.keys())}")
        return False

    if not active_sessions[session_token]:
        print("❌ Session token exists but not authenticated")
        return False

    print("✅ Session is valid and authenticated")
    return True

class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        if not self.active_connections:
            return
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception as e:
                print(f"Error broadcasting message: {e}")
                # Remove broken connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

    async def broadcast_json(self, data: dict):
        if not self.active_connections:
            return
        for connection in self.active_connections:
            try:
                await connection.send_json(data)
            except Exception as e:
                print(f"Error broadcasting JSON: {e}")
                # Remove broken connections
                if connection in self.active_connections:
                    self.active_connections.remove(connection)

manager = ConnectionManager()

class State:
    def __init__(self):
        self.is_downloading = False
        self.logs = []
        self.progress = {}

    def reset(self):
        self.is_downloading = False
        self.logs = []
        self.progress = {}

state = State()

@app.get("/")
async def get(request: Request):
    session_token = get_session_token(request)
    print(f"🌐 Main page access attempt: session_token='{session_token[:20] if session_token else 'None'}...'")
    print(f"🍪 All cookies: {request.cookies}")
    print(f"🔑 Active sessions: {list(active_sessions.keys())}")

    if not is_authenticated(request):
        print("❌ Not authenticated, redirecting to login")
        return RedirectResponse(url="/login")

    print("✅ Authenticated, serving main page")
    with open("frontend/index.html") as f:
        return HTMLResponse(f.read())

@app.get("/login")
async def login_page():
    print("🔑 Login page requested")
    with open("frontend/login.html") as f:
        return HTMLResponse(f.read())


@app.post("/login")
async def login(request: Request, pin: str = Form(...)):
    print(f"🔐 PIN authentication attempt: PIN='{pin}', Expected='{settings.PIN}'")
    print(f"🌐 Request host: {request.headers.get('host')}")
    print(f"🌐 Request URL: {request.url}")

    if verify_pin(pin):
        session_token = create_session_token()
        active_sessions[session_token] = True
        print(f"✅ Authentication successful, session token: {session_token[:20]}...")
        print(f"🔑 Total active sessions: {len(active_sessions)}")

        response = RedirectResponse(url="/", status_code=302)
        response.set_cookie(
            key="session_token",
            value=session_token,
            max_age=3600 * 24,  # 24 hours
            httponly=False,  # Set to False for debugging - can see in browser dev tools
            secure=False,  # Must be False for HTTP
            samesite="lax",
            path="/"  # Ensure cookie is available for all paths
        )
        print(f"🍪 Setting cookie: session_token={session_token[:20]}...")
        return response
    else:
        print(f"❌ Authentication failed: Invalid PIN")
        # Return login page with error
        with open("frontend/login.html") as f:
            return HTMLResponse(f.read())


@app.get("/debug")
async def debug_session(request: Request):
    """Debug endpoint to check session state"""
    session_token = get_session_token(request)
    return {
        "session_token": session_token[:20] + "..." if session_token else None,
        "has_session": bool(session_token),
        "is_authenticated": is_authenticated(request),
        "active_sessions_count": len(active_sessions),
        "cookies": dict(request.cookies),
        "headers": dict(request.headers)
    }

@app.post("/logout")
async def logout(request: Request):
    session_token = get_session_token(request)
    print(f"🚪 Logout attempt with token: {session_token[:20] if session_token else 'None'}...")
    if session_token in active_sessions:
        del active_sessions[session_token]
        print(f"✅ Session removed from active sessions")

    response = RedirectResponse(url="/login", status_code=302)
    response.delete_cookie("session_token", path="/")
    return response

async def download_task(url: str):
    try:
        state.is_downloading = True
        parts = url.split("---")
        if parts[1] != "":
            message = str("Adding songs to Playlist " + parts[1] + " When Complete")
            await manager.broadcast(message)
        # await manager.broadcast("Starting download...")
        songs_to_add = []
        songs_to_add = await run_spotdl(parts[0], manager, state)
        print("songs to add",songs_to_add)

        if parts[1] != "":
            message = str("Download complete now adding songs to playlist " + parts[1])
            await manager.broadcast(message)
            await add_to_playlist(parts[1],songs_to_add,manager)
            await manager.broadcast(f"{len(songs_to_add)} songs added to {parts[1]}")




        state.is_downloading = False
        state.logs.append("[DONE]")
        await manager.broadcast("[DONE]")

    except Exception as e:
        error_msg = f"Download failed: {str(e)}"
        print(f"Download task error: {e}")
        state.is_downloading = False
        state.logs.append(error_msg)
        await manager.broadcast(error_msg)
        await manager.broadcast("[DONE]")

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Check authentication via query parameter for WebSocket
    session_token = websocket.query_params.get("session_token", "")
    if not session_token or session_token not in active_sessions:
        await websocket.close(code=4001, reason="Authentication required")
        return

    await manager.connect(websocket)
    try:
        # Send current state to the newly connected client
        for log in state.logs:
            await websocket.send_text(log)
        if state.progress:
            await websocket.send_json(state.progress)

        while True:
            url = await websocket.receive_text()
            print(url)
            if not state.is_downloading:
                state.reset()
                asyncio.create_task(download_task(url))
            else:
                await websocket.send_text("A download is already in progress.")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception as e:
        print(f"WebSocket error: {e}")
        manager.disconnect(websocket)
