import time
import subprocess
import sys

# ---------------------------------------------------
# CONFIGURATION SECTION
# ---------------------------------------------------
# Set the URL of the livestream page you want to monitor.
# For YouTube livestreams, use the channel's /live page.
# Example: "https://www.youtube.com/@NASA/live"
PAGE_URL = ""

# How often (in seconds) should the script check the page for a livestream?
CHECK_INTERVAL = 30  # Try 30 seconds, increase for less frequent checks

# The filename to save the recorded stream.
OUTPUT_FILE = "recorded_stream.mp4"

# Full path to your ffmpeg executable.
# Edit this if you move ffmpeg elsewhere!
FFMPEG_PATH = r"C:\Users{YOUR_DIRECTORY}\bin\ffmpeg.exe"
# ---------------------------------------------------
# ADVANCED: yt-dlp OPTIONS (optional)
# ---------------------------------------------------
# If you need to customize yt-dlp (like cookies, user agent), add extra args to this list.
YT_DLP_EXTRA_ARGS = []  # Example: ["--cookies", "cookies.txt"]

# ---------------------------------------------------
# FUNCTION: Get the livestream direct URL
# ---------------------------------------------------
def get_live_stream_url(page_url):
    """
    Uses yt-dlp to fetch the direct stream URL if live.
    Returns the stream URL, or None if not live.

    To customize:
    - If your stream requires login/cookies, add --cookies arguments in YT_DLP_EXTRA_ARGS.
    - For other sites, consult yt-dlp documentation for extra options.
    """
    try:
        # Build yt-dlp command; -g gets the direct video/audio URL
        cmd = ["yt-dlp", "--no-warnings", "--no-playlist", "-g"] + YT_DLP_EXTRA_ARGS + [page_url]
        result = subprocess.run(cmd, capture_output=True, text=True)
        url = result.stdout.strip()
        # If yt-dlp finds a stream, stdout is a URL
        if url and url.startswith("http"):
            return url
        else:
            return None
    except Exception as e:
        print(f"yt-dlp error: {e}")
        return None

# ---------------------------------------------------
# FUNCTION: Wait until livestream starts
# ---------------------------------------------------
def watch_for_stream(page_url):
    """
    Keeps checking the livestream page until a stream is available.
    Edits:
    - Change CHECK_INTERVAL to make checks faster/slower.
    - Consider adding a timeout or max attempts if you don't want to wait forever.
    """
    print(f"Watching page: {page_url}")
    stream_url = None
    while not stream_url:
        print("Checking for livestream...")
        stream_url = get_live_stream_url(page_url)
        if stream_url:
            print(f"Livestream detected! URL: {stream_url}")
            break
        else:
            print(f"No livestream yet. Checking again in {CHECK_INTERVAL} seconds.")
            time.sleep(CHECK_INTERVAL)
    return stream_url

# ---------------------------------------------------
# FUNCTION: Record the livestream using ffmpeg
# ---------------------------------------------------
def record_stream(stream_url, output_file):
    """
    Uses ffmpeg to record the stream until it ends.
    Edits:
    - If you want to change the video format, adjust the ffmpeg arguments.
    - For advanced ffmpeg options, see ffmpeg documentation.
    """
    print(f"Starting recording to {output_file}...")
    cmd = [
        FFMPEG_PATH,     # Use your custom ffmpeg path here
        "-y",            # Overwrite output file without asking
        "-i", stream_url,
        "-c", "copy",    # Copy codecs (fast, lossless)
        output_file
    ]
    try:
        process = subprocess.Popen(cmd)
        process.wait()
    except FileNotFoundError:
        print(f"ERROR: ffmpeg not found at {FFMPEG_PATH}. Please check the path.")
    except KeyboardInterrupt:
        print("\nRecording interrupted by user. Stopping...")
        process.terminate()

# ---------------------------------------------------
# MAIN SCRIPT LOGIC
# ---------------------------------------------------
def main():
    """
    Entry point for this script.
    Edits:
    - Change PAGE_URL and OUTPUT_FILE above to match your needs.
    - Make sure yt-dlp and ffmpeg are installed.
    - FFMPEG_PATH should be correct for your system.
    """
    stream_url = watch_for_stream(PAGE_URL)
    record_stream(stream_url, OUTPUT_FILE)
    print(f"Recording ended. File saved as {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
