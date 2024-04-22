import youtube_dl
from youtube_transcript_api import YouTubeTranscriptApi

# YouTube playlist URL
playlist_url = "https://www.youtube.com/@SoftWhiteUnderbelly/playlists"

def download_playlist_videos(playlist_url):
    ydl_opts = {
        'extract_flat': True,
        'quiet': True,
        'force_generic_extractor': True,
    }

    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        result = ydl.extract_info(playlist_url, download=False)
        video_urls = [entry['url'] for entry in result['entries']]

    return video_urls

def get_transcripts(video_urls):
    transcripts = {}
    for url in video_urls:
        video_id = url.split('=')[-1]
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            text = ' '.join([t['text'] for t in transcript])
            transcripts[url] = text
        except Exception as e:
            transcripts[url] = f"Transcript not available: {str(e)}"

    return transcripts

def save_transcripts(transcripts, output_file):
    with open(output_file, 'w', encoding='utf-8') as f:
        for url, text in transcripts.items():
            f.write(f"Video URL: {url}\n")
            f.write(text + '\n\n')

if __name__ == "__main__":
    video_urls = download_playlist_videos(playlist_url)
    transcripts = get_transcripts(video_urls)
    save_transcripts(transcripts, "transcripts.txt")
