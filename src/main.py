from sanic import Sanic
from sanic.response import json, redirect
from sanic_redis import SanicRedis

from .conf import settings
from .log import get_logger
from .utils import get_cdn_link

logger = get_logger('app')
app = Sanic("Balancer")
app.config.update(
    {'REDIS': settings.REDIS_URL,}
)
redis = SanicRedis()
redis.init_app(app)


@app.route('/')
async def balancer(request):
    """
    1. Каждый 10й запрос, формата описанного выше, отправляем в оригинальный урл(query arg video) 301 редиректом.
    2. Остальные отправляем на http://$CDN_HOST/s1/video/1488/xcg2djHckad.m3u8, где:
    :param request:
    :return:
    """
    video_resource = request.args.get('video')
    if not video_resource:
        return json({"detail": "video query parameter is required"}, status=400)

    counter_key = settings.COUNTER_KEY
    async with redis.conn as r:
        await r.incr(counter_key)
        counter = await r.get(counter_key)

    counter_value = int(counter.decode('utf-8'))
    # редиректим на оригинальную ссылку
    if counter_value % 10 == 0:
        redirect_to = video_resource
    # в остальному случае на CDN
    else:
        redirect_to = get_cdn_link(video_resource, settings.CDN_HOST)
    logger.info(f'{counter_value=} -> {redirect_to=}')
    return redirect(to=redirect_to, status=301)


if __name__ == '__main__':
    app.run(host=settings.APP_HOST, port=settings.APP_PORT, debug=settings.DEBUG)
