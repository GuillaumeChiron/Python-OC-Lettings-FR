from django.test import Client, TestCase, override_settings
from django.urls import path

from oc_lettings_site.urls import urlpatterns as base_urlpatterns


def erroring_view(request):
    """Raise unconditionally to trigger Django's 500 error handler."""
    raise Exception("Forced exception for 500 page test")


# URLconf used only by the 500 test: the real urlpatterns plus a view that
# deliberately raises. The real patterns are kept because base.html resolves
# named routes (``index``, ``profiles:index``, ``lettings:index``) that must
# still exist for the 500 page itself to render.
urlpatterns = base_urlpatterns + [
    path("boom/", erroring_view, name="boom"),
]


class ErrorPagesTest(TestCase):
    """Verify the custom 404 and 500 templates are actually rendered."""

    def test_404_page_renders_custom_template(self):
        """An unknown URL should return 404 and render templates/404.html."""
        client = Client()
        response = client.get("/this-url-does-not-exist/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "404.html")

    @override_settings(ROOT_URLCONF=__name__, DEBUG=False)
    def test_500_page_renders_custom_template(self):
        """An unhandled exception should return 500 and render templates/500.html."""
        client = Client(raise_request_exception=False)
        response = client.get("/boom/")
        self.assertEqual(response.status_code, 500)
        self.assertTemplateUsed(response, "500.html")
