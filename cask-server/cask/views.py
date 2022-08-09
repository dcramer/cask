import logging

import sentry_sdk
from graphene_django.views import GraphQLView

logger = logging.getLogger("cask")


class EnhancedGraphQLView(GraphQLView):
    # https://github.com/graphql-python/graphene-django/issues/124
    def execute_graphql_request(self, *args, **kwargs):
        """Extract any exceptions and send them to Sentry"""

        result = super().execute_graphql_request(*args, **kwargs)
        if result and result.errors:
            for error in result.errors:
                if hasattr(error, "original_error"):
                    try:
                        raise error.original_error
                    except Exception as e:
                        logger.exception(e)
                        sentry_sdk.capture_exception(e)
                else:
                    logger.error(error)
        return result
