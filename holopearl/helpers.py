from yt_dlp import YoutubeDL

def find_urls_in_string(string_to_parse: str) -> list:
    return [
        i for i 
        in string_to_parse.split() 
        if i.startswith("https:") or i.startswith("http:")
    ]

def yt_download(urls: list, file_path: str = None, progress_hooks: list = None):
    settings_dict = {}
    if file_path:
        settings_dict['paths'] = {'home': file_path}

    if progress_hooks:
        settings_dict['progress_hooks'] = progress_hooks

    with YoutubeDL(settings_dict) as ydl:
        ydl.download(urls)
