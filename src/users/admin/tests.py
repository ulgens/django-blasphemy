from django.test import tag

from core.testcases import AdminTestCase


class UsersAppAdminTestCase(AdminTestCase):
    app_name = "users"


@tag("admin", "user")
class UserAdminTest(UsersAppAdminTestCase):
    model_name = "user"
