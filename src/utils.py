from urllib.parse import urlparse, urlunparse


def get_cdn_link(original_link: str, cdn_host: str) -> str:
    """
    Изменить оригинальную ссылку на ссылку на CDN
    :param original_link: оригинальная ссылка
    :param cdn_host: cdn host
    :return:
    """
    parsed_url = urlparse(original_link)
    cluster_server = parsed_url.hostname.split('.')[0]
    cdn_link_parts = (parsed_url.scheme, cdn_host, f'{cluster_server}{parsed_url.path}', '', '', '')
    return urlunparse(cdn_link_parts)
