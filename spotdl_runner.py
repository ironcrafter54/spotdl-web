#!/usr/bin/env python3
import asyncio
import re

async def run_spotdl(url: str, manager, state):

    try:
        # Run spotdl with verbose output
        process = await asyncio.create_subprocess_exec(
            'spotdl', 'download', url, '--format', 'mp3', '--bitrate', '320k', '--output', './downloads',
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.STDOUT
        )

        songs_downloaded = []
        songs_skipped = []
        songs_lookup_failed = []
        total_songs_to_download = ""

        def print_progress():
            if total_songs_to_download != "":
                print("Downloaded/Skipped/failed/total")
                print(len(songs_downloaded),"/",len(songs_skipped),"/",len(songs_lookup_failed),"/",total_songs_to_download)

        print("Capturing output...")

        while True:
            if process.stdout is None:
                break

            chunk = await process.stdout.read(32768)
            if not chunk:
                break

            decoded_chunk = chunk.decode('utf-8', errors='ignore')
            stripped_chunk = decoded_chunk.strip()

            # print("stripped chunk is:",stripped_chunk,"end of stripped chunk")

            if stripped_chunk == "":

                end_message = "Completed"

                # list failed songs
                if not(len(songs_lookup_failed) == 0):
                    print("failed to find")
                    for i in songs_lookup_failed:
                        print(i)
                    print(len(songs_lookup_failed),"Songs not found")
                    end_message += (" " + str(len(songs_lookup_failed)) + " Song/s not found")

                # list already present songs
                if len(songs_skipped) != 0:
                    print("already present")
                    for i in songs_skipped:
                        print(i)
                    print("end songs skipped")
                end_message += (" " + str(len(songs_skipped)) + " Song/s alredy present")


                progress = {
                    "type": "progress",
                    "current": len(songs_downloaded),
                    "total": total_songs_to_download,
                    "track": end_message
                }
                state.progress = progress
                asyncio.create_task(manager.broadcast_json(progress))
                break

            # find total songs
            if "F" in stripped_chunk[0] and total_songs_to_download == "":
                index = 6
                while stripped_chunk[index].isdigit():
                    if stripped_chunk[index].isdigit():
                        total_songs_to_download += stripped_chunk[index]
                        index += 1
                print("Total Songs:", total_songs_to_download)

                progress = {
                    "type": "progress",
                    "current": 0,
                    "total": total_songs_to_download,
                    "track": "Starting download..."
                }
                state.progress = progress
                asyncio.create_task(manager.broadcast_json(progress))
                asyncio.create_task(manager.broadcast(f"Found {total_songs_to_download} songs to download."))

            #identify skipped tracks
            if "S" in stripped_chunk[0]:
                skipped_track_name = stripped_chunk[9:]
                skipped_track_name = skipped_track_name.replace("\n","")
                skipped_track_name = ' '.join(skipped_track_name.split())
                skipped_track_name = skipped_track_name.replace("(file already exists) (duplicate)","")
                skipped_track_name = skipped_track_name.replace("(file already exists)(duplicate)","")
                skipped_track_name = skipped_track_name.replace("(filealready exists) (duplicate)","")
                skipped_track_name = skipped_track_name.strip()
                songs_skipped.append(skipped_track_name)
                print("Skipped:",skipped_track_name)
                asyncio.create_task(manager.broadcast(f"Skipped: {skipped_track_name}"))


            #identify downloaded tracks
            if "D" in stripped_chunk[0]:
                downloaded_track_name = stripped_chunk[12:]
                downloaded_track_name = re.sub(r'https?://\S+', '', downloaded_track_name).strip()
                downloaded_track_name = downloaded_track_name.strip(' "\':\n\r\t')
                songs_downloaded.append(downloaded_track_name)
                print("Downloaded:", downloaded_track_name)
                progress = {
                    "type": "progress",
                    "current": len(songs_downloaded),
                    "total": total_songs_to_download,
                    "track": downloaded_track_name
                }
                state.progress = progress
                asyncio.create_task(manager.broadcast_json(progress))
                asyncio.create_task(manager.broadcast(f"Downloaded: {downloaded_track_name}"))

            #identify failed lookups
            if "L" in stripped_chunk[0]:
                errored_track_name = stripped_chunk[40:]
                songs_lookup_failed.append(errored_track_name)
                print("Failed:", errored_track_name)
                asyncio.create_task(manager.broadcast(f"Failed to lookup song: {errored_track_name}"))

            print_progress()

            for i in songs_downloaded:
                print(i)
        return songs_downloaded + songs_skipped


    except Exception as e:
        print(f"Error: {e}")
