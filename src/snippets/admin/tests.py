from django.test import tag

from core.testcases import AdminTestCase


class SnippetsAppAdminTestCase(AdminTestCase):
    app_name = "snippets"


@tag("admin", "snippet")
class SnippetAdminTest(SnippetsAppAdminTestCase):
    model_name = "snippet"
