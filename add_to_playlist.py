#!/usr/bin/env python3
import libsonic
import asyncio
import time
from config import settings

async def add_to_playlist(name, songs, manager):
    conn = libsonic.Connection(settings.URL, settings.NAVIDROME_USERNAME, settings.PASSWORD, settings.NAVIDROME_PORT)
    await manager.broadcast("Scanning Library for new songs")
    conn.startScan()
    time.sleep(5)
    await manager.broadcast("Scan Completed")
    print("started Scan")
    def get_playlist_id(name):
        print("getting Playlist name")
        playlist_exists = False
        playlist_id = ""
        try:
            playlists = conn.getPlaylists()["playlists"]["playlist"]
            for i in playlists:
                if i["name"] == name:
                    playlist_exists = True
                    playlist_id = i["id"]
                    break
        except:
            print("error fetching playlists there probably aren't any defined yet")
        if playlist_exists == False:
            log = conn.createPlaylist(name=name)
            playlist_id = log['playlist']['id']
            playlist_exists = True
        return playlist_id

    def song_id_grabber(titles):
        print("grabbing song id's")
        song_ids = []
        for i in titles:
            search_item = i.replace(" - "," ")
            result = conn.search2(query=search_item,artistCount=0,albumCount=0,songCount=1)
            if "song" in result["searchResult2"]:
                song_ids.append(result["searchResult2"]["song"][0]["id"])
            else:
                msg = str(i+" not found in navidrome")
                asyncio.create_task(manager.broadcast(msg))

        return song_ids

    def add_songs_to_playlist(song_names_list,playlist_name):
        print("adding Songs to playlist")
        ids = song_id_grabber(song_names_list)
        play_id = get_playlist_id(playlist_name)
        contents = conn.getPlaylist(pid=play_id)
        if "entry" in (contents["playlist"]):
            print("contains songs")
            songs_in_playlist = []
            contents = conn.getPlaylist(pid=play_id)
            for i in contents["playlist"]["entry"]:
                songs_in_playlist.append(i["id"])

            add = [item for item in ids if item not in songs_in_playlist]
            print(songs_in_playlist)
            print("adding ", add)
            conn.updatePlaylist(lid=play_id,songIdsToAdd=add)
        else:
            conn.updatePlaylist(lid=play_id,songIdsToAdd=ids)

    print("running base function")
    add_songs_to_playlist(songs,name)
