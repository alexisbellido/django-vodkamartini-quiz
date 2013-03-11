from django.test import TestCase
from django.core.cache import cache
from django.contrib.auth.models import User

class BasicViews(TestCase):
    def setUp(self):
        """
        Create editor user and some data to use for creating quiz related objects.
        """

        cache.clear()
        self.regular_user = User.objects.create_user(username='joe', password='secret')
        self.editor = User.objects.create_user(username='mark_editor', password='secret')
        self.title = 'A Quiz Title'
        self.body = 'This is the body for the quiz test'
        self.slug='the-quiz'

        #status = Quiz.LIVE_STATUS
        #quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        #quiz.save()

        #question = Question(question='Choose your color', quiz=quiz)
        #question.save()

        #answer = Answer(letter='a', answer='Blue', question=question, points=5)
        #answer.save()

        #user_quiz_answer = UserQuizAnswer(user=self.regular_user , quiz=quiz, answer=answer)
        #user_quiz_answer.save()

        #quiz_result = QuizResult(letter='a', quiz=quiz, description='Description of this quiz result')
        #quiz_result.save()


    def testTwo(self):
        two = 2
        self.assertEqual(two, 2),
