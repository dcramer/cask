from django.conf import settings
from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from cask.views import EnhancedGraphQLView

urlpatterns = [
    path("graphql/", csrf_exempt(EnhancedGraphQLView.as_view(graphiql=settings.DEBUG)))
]
