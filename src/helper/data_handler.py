import os

import pandas as pd
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()

SCOPE = """user-library-read user-library-modify
            user-read-playback-position
            playlist-modify-private"""

SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.environ.get("SPOTIPY_REDIRECT_URI")

SP: spotipy.Spotify = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope=SCOPE,
        client_secret=SPOTIPY_CLIENT_SECRET,
        client_id=SPOTIPY_CLIENT_ID,
        redirect_uri=SPOTIPY_REDIRECT_URI,
    )
)
CACHE_DIR = os.path.join(os.path.abspath(os.pardir), ".cache")
os.makedirs(CACHE_DIR, exist_ok=True)
CACHE_FILE = os.path.join(CACHE_DIR, "cache.pkl")

def get_your_saved_episodes(skip_cache=True) -> pd.DataFrame:
    # check if cache exists
    if not skip_cache and os.path.exists(CACHE_FILE):
        print("Reading from cache, to refresh cache set cli flag -sc")
        return pd.read_pickle(CACHE_FILE)
    offset = 0
    limit = 50
    saved_ep = []
    while True:
        ep_list = SP.current_user_saved_episodes(offset=offset, limit=limit)
        if not ep_list["items"]:
            break
        ep_list = [ep.get("episode") for ep in ep_list["items"]]
        saved_ep.extend([ep for ep in ep_list])
        offset += limit

    df = pd.DataFrame(saved_ep)
    # convert release_date to datetime
    df["release_date"] = pd.to_datetime(df["release_date"], format="%Y-%m-%d")
    # save to cache
    df.to_pickle(CACHE_FILE)
    return df

def delete_from_your_episodes(df : pd.DataFrame) -> bool:
    ids = df["id"].tolist()
    # make chunks of 50 ids to delete
    still_in = []
    for i in range(0, len(ids), 50):
        SP.current_user_saved_episodes_delete(ids[i:i+50])
        # check if episodes are deleted and return the result
        still_in.extend(SP.current_user_saved_episodes_contains(ids[i:i+50]))
    check = not any(still_in)
    if not check:
        invalid_ids = [ids[i] for i in range(len(ids)) if still_in[i]]
        print(f"Failed to delete {len(invalid_ids)} of {len(ids)} episodes with the following ids: {invalid_ids}")
    else:
        print(f"successfully deleted {len(ids)} from your episodes")
    return check
