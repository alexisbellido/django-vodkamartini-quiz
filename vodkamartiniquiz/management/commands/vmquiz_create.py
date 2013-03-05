from django.core.management.base import BaseCommand, CommandError
from optparse import make_option

class Command(BaseCommand):
    args = '<quiz_title quiz_title ...>'
    option_list = BaseCommand.option_list + (
        make_option('--category_id', dest='category_id', default=None,
            help='Specifies the category id to use for new quizzes.'),
    )
    help = 'Creates quizzes.'

    def handle(self, *args, **options):
        pass

    def create_quiz(self, title, c):
        pass
