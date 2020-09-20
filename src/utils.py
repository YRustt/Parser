from urllib.parse import urlencode


def make_url(url, **kwargs):
    get_args = urlencode(kwargs) if kwargs else None

    if url.startswith("http"):
        pass
    elif url.startswith("//"):
        url = f"https:{url}"
    else:
        url = f"https://{url}"

    if get_args is not None:
        return f"{url}?{get_args}"

    return url
