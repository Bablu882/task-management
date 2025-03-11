import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = get_asgi_application()

from core.routing import ws_urlpatterns

application = ProtocolTypeRouter({
    'http': app,
    'websocket': AllowedHostsOriginValidator(URLRouter(ws_urlpatterns))
})
