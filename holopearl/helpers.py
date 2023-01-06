def find_urls_in_string(string_to_parse: str) -> list:
    return [
        i for i 
        in string_to_parse.split() 
        if i.startswith("https:") or i.startswith("http:")
    ]