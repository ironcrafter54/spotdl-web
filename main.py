from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse
from spotdl_runner import run_spotdl
from add_to_playlist import add_to_playlist
import asyncio

app = FastAPI()

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
async def get():
    with open("frontend/index.html") as f:
        return HTMLResponse(f.read())

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
