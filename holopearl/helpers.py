from yt_dlp import YoutubeDL

def find_urls_in_string(string_to_parse: str) -> list:
    return [
        i for i 
        in string_to_parse.split() 
        if i.startswith("https:") or i.startswith("http:")
    ]

def yt_download(urls: list, file_path: str = None, quiet: bool = False):
    settings_dict = {
        'noprogress': True,
        'quiet': quiet
        }
    if file_path:
        settings_dict['paths'] = {
            'home': file_path,
            'temp': './'
        }

    with YoutubeDL(settings_dict) as ydl:
        ydl.download(urls)
