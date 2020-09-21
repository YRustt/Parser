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
        if "?" in url:
            return f"{url}&{get_args}"
        else:
            return f"{url}?{get_args}"

    return url


def get_product_id_from_url(url):
    return url.split("/")[-1].split(".")[0]
