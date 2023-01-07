from yt_dlp import YoutubeDL

def find_urls_in_string(string_to_parse: str) -> list:
    return [
        i for i 
        in string_to_parse.split() 
        if i.startswith("https:") or i.startswith("http:")
    ]

def yt_download(urls: list, file_path: str = None):
    if file_path:
        with YoutubeDL({'paths':{'home':file_path}}) as ydl:
            ydl.download(urls)
    else:
        with YoutubeDL() as ydl:
            ydl.download(urls)
