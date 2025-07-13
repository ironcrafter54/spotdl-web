#!/usr/bin/env python3
import asyncio

async def run_spotdl(url: str, manager, state):
    """Test script to capture spotdl output and analyze the format"""

    print("Testing spotdl output format...")
    print(f"URL: {url}")
    print("-" * 50)

    try:
        # Run spotdl with verbose output
        process = await asyncio.create_subprocess_exec(
            'spotdl', 'download', url, '--format', 'mp3', '--bitrate', '320k',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        total_songs = 0
        songs_downloaded = 0
        buffer = ""



        print("Capturing output...")

        while True:
            if process.stdout is None:
                break

            chunk = await process.stdout.read(100)
            if not chunk:
                break

            decoded_chunk = chunk.decode('utf-8', errors='ignore')
            buffer += decoded_chunk

            lines = buffer.splitlines(keepends=True)

            for line in lines:
                if not line.endswith('\n'):
                    buffer += line
                    continue

                stripped_line = line.strip()
                print(f"LINE: {repr(stripped_line)}")

                if "Found" in stripped_line:
                    total_songs = int(stripped_line[6])
                    print("total songs are" ,total_songs)
                    progress = {
                        "type": "progress",
                        "current": 0,
                        "total": total_songs,
                        "track": "Starting download..."
                    }
                    state.progress = progress
                    await manager.broadcast_json(progress)
                    await manager.broadcast(f"Found {total_songs} songs to download.")
                    break


                if "Downloaded" in stripped_line:
                    songs_downloaded += 1
                    print("download detected")
                    progress = {
                        "type": "progress",
                        "current": songs_downloaded,
                        "total": total_songs,
                        "track": stripped_line
                    }
                    state.progress = progress
                    await manager.broadcast_json(progress)
                    await manager.broadcast(f"Downloaded: {stripped_line}")

                if "Skipping" in stripped_line:
                    print("duplicate detected")

                if "LookupError" in stripped_line:
                    print("lookup error detected")

        await process.wait()
        print(f"\nFinal count - Total: {total_songs}, Downloaded: {songs_downloaded}")
        final_progress = {
            "type": "progress",
            "current": songs_downloaded,
            "total": total_songs,
            "track": "Download complete!"
        }
        state.progress = final_progress
        await manager.broadcast_json(final_progress)
        await manager.broadcast(f"Download completed! Downloaded {songs_downloaded} out of {total_songs} songs.")

    except Exception as e:
        print(f"Error: {e}")
