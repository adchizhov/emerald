from src.conf import settings
from src.utils import get_cdn_link


def test_get_cdn_link():
    """
    Тест на формирование правильной ссылки на CDN
    :return:
    """
    original_link = 'http://s1.origin-cluster/video/1488/xcg2djHckad.m3u8'
    prepared_cdn_link = f'http://{settings.CDN_HOST}/s1/video/1488/xcg2djHckad.m3u8'

    assert get_cdn_link(original_link, cdn_host=settings.CDN_HOST) == prepared_cdn_link
