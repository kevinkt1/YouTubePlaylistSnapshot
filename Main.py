"""Generate a text file containing the title of all the videos in a playlist.

To run this script:
  python -W ignore Main.py
"""

# External modules
from os import mkdir
from os.path import isdir, join
from pyyoutube import Api
from time import localtime, strftime

# Internal modules that are kept secret
import MyConfigurations

# Should be disabled by default
DEBUG_MODE = False
TRACE_MODE = False

def isVideoBlocked(countryCode: str, video) -> bool:
  """Determine whether the video is blocked in the user's country.

  :param countryCode: ISO 3166-1 alpha-2 code
  :param video: A video object. See https://developers.google.com/youtube/v3/docs/videos

  Note from the developer:
    Through trial and error with various different videos, I discovered there isn't a common standard
    that RegionRestriction adheres to, so I wrote this goofy function based off my observations.
    Correctness not guaranteed.
  """
  regionRestriction = video.contentDetails.regionRestriction

  if TRACE_MODE:
    print(f'\n\nRegionRestriction of {video.snippet.title}: {regionRestriction}')

  if not regionRestriction:
    return False
  else:
    # NOTE: I have seen both blocked and unblocked videos when this value is None. Example: RegionRestriction(allowed=None)
    if regionRestriction.allowed == None:
      if DEBUG_MODE:
        print(f'\n\nRegionRestriction(allowed=None): {video.snippet.title}: {regionRestriction}')
      return False

    elif countryCode in regionRestriction.allowed:
      return False

    elif not countryCode in regionRestriction.blocked:
      return False

    elif countryCode in regionRestriction.blocked:
      print(f'\n\n{video.snippet.title} is blocked in the {countryCode} region')
      return True

    else:
      print(f'\n\nUnhandled case for RegionRestriction of {video.snippet.title}: {regionRestriction}')
      return True

if __name__ == '__main__':
  api = Api(api_key=MyConfigurations.API_KEY)

  countryCode = MyConfigurations.COUNTRY_CODE
  playlistIDs = MyConfigurations.PLAYLIST_IDS
  displayUploader = MyConfigurations.DISPLAY_UPLOADER

  # Create this folder from the project root
  if not isdir('output'):
    mkdir('output')

  # Then create another nested folder. Example: output/output-2020-09-14T173551
  outputFolderPath = join('output', 'output-' + strftime('%Y-%m-%dT%H%M%S', localtime()))
  mkdir(outputFolderPath)

  # Remember to comment out the individual playlist keys from MyConfigurations if you don't want to loop through them all
  for key in playlistIDs:
    playlistVideoItems = api.get_playlist_items(playlist_id=playlistIDs[key], count=None).items

    currentTimestamp = strftime(' %Y-%m-%dT%H%M%S', localtime())
    outputFileName = key + currentTimestamp + '.out'
    outputFilePath = join(outputFolderPath, outputFileName)

    with open(outputFilePath, 'w', encoding='utf8') as outfile:
      for index, playlistVideo in enumerate(playlistVideoItems):

        try:
          video = api.get_video_by_id(video_id=playlistVideo.contentDetails.videoId).items[0]

          if not isVideoBlocked(countryCode, video):
            outfile.write(video.snippet.title + '\n')
            if displayUploader:
              outfile.write(f'{video.snippet.channelTitle}\n\n')

        except Exception as e:
          print(f'\n\nException occurred on "{playlistVideo.snippet.title}" within playlist {key} at index {index}: {e}')

