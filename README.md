# Script to delete episodes from your spotify "Your Episodes"-Playlist

## Why?
This script is for everyone who is lazy and does not want to remove each episode stuck in the "Your Episodes"-Playlist forever.

I had over 300 episodes of podcasts piled up, listened to most of them until the credits came on. Stopping the podcast at this point makes Spotify think you have not completed your episode, thus the automatic deletion built into the app does not trigger after your set time period.

## How-To

1. Register on [Spotify Developer](https://developer.spotify.com/) and create an app
    - set the redirect URL to http://127.0.0.1:8080 (or whatever port is free)
2. create a .env file with the following contents:
    - `SPOTIPY_CLIENT_ID = "YOUR-CLIENT-ID"`
    - `SPOTIPY_CLIENT_SECRET = "YOUR-CLIENT-SECRET"`
    - `SPOTIPY_REDIRECT_URI = "http://127.0.0.1:8080"` (or whatever you did in Step 1.)
3. create a virtual environment, activate it and run `pip install -r requirements.txt`
4. go into `/src` and use `python delete_your_episodes.py --help` for further instructions
    - your browser should prompt you to authorize your app (Don't worry, I have no access to anything, it's all yours)
5. ???
6. Enjoy your cleaned up Spotify