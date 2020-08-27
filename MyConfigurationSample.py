# To run the script: python -W ignore Main.py
# Rename this sample file to MyConfigurations.py

API_KEY = 'Your Google Project API Key'

# Used for determining whether a video is blocked in that country.
# Defaulted to United States of America.
# Set your country code so that the script can display that a video is region-locked.
#
# The YouTube Data API uses this list of country codes:
#   https://www.wikiwand.com/en/ISO_3166-1_alpha-2#/Current_codes
COUNTRY_CODE = 'US'

# A list of your playlist IDs
# Example: https://www.youtube.com/playlist?list=PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw
# In the example URL, 'PLOU2XLYxmsIKpaV8h0AGE05so0fAwwfTw' is the playlist ID
PLAYLIST_IDS = {
  "Your Playlist Name" : "Your Playlist ID",
# "Another Playlist"   : "Another ID", # Comment out if you don't want to the script to see this playlist
}

# Whether to display the channel name of the video uploader
DISPLAY_UPLOADER = True

