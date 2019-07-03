"""
Tests for sync courses management command
"""
import mock

from django.core.management import call_command

from opaque_keys.edx.keys import CourseKey
from openedx.core.djangoapps.catalog.tests.factories import CourseRunFactory
from openedx.core.djangoapps.content.course_overviews.models import CourseOverview
from student.tests.factories import UserFactory
from xmodule.modulestore.django import modulestore
from xmodule.modulestore.tests.django_utils import ModuleStoreTestCase

COMMAND_MODULE = 'contentstore.management.commands.sync_courses'


@mock.patch(COMMAND_MODULE + '.get_course_runs')
class TestSyncCoursesCommand(ModuleStoreTestCase):
    """ Test sync_courses command """

    def setUp(self):
        super(TestSyncCoursesCommand, self).setUp()

        self.user = UserFactory(username='test', email='test@example.com')
        self.catalog_course_runs = [
            CourseRunFactory(),
            CourseRunFactory(),
        ]

    def test_courses_sync(self, mock_catalog_course_runs):
        mock_catalog_course_runs.return_value = self.catalog_course_runs

        call_command('sync_courses', self.user.email)

        for run in self.catalog_course_runs:
            course_key = CourseKey.from_string(run.get('key'))
            self.assertTrue(modulestore().has_course(course_key))
            CourseOverview.objects.get(id=run.get('key'))
