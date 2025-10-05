Requirements

Selenium https://selenium-python.readthedocs.io 

chromedriver (or another driver for your browser) https://developer.chrome.com/docs/chromedriver

ffmpeg (must be installed and in your PATH) https://ffmpeg.org

BeautifulSoup4 (optional, for HTML parsing) https://pypi.org/project/beautifulsoup4


For YouTube Livestreams
You cannot reliably grab a direct stream URL from the video tag. 
You need to use a library that can extract the actual stream URL, like yt-dlp.

Here’s a robust solution:

Use yt-dlp to poll for livestream availability and get the stream URL.

Use ffmpeg to record once yt-dlp finds a live stream.

Instructions
Install yt-dlp:

pip install yt-dlp

Or download from yt-dlp releases.

https://github.com/yt-dlp/yt-dlp/releases

Install ffmpeg and ensure it’s in your PATH.

FFMPEG_PATH = r"C:\Users\{YOUR_DIRECTORY}\bin\ffmpeg.exe"


Run the script:
python_livestream_recorder.py

