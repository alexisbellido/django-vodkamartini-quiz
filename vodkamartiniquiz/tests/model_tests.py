from datetime import datetime, timedelta
from django.test import TestCase
from django.core.cache import cache
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from vodkamartinicategory.models import Category
from vodkamartiniquiz.models import Quiz, Question, Answer, UserQuizAnswer, QuizResult
from django.utils.timezone import now, get_current_timezone

"""
All tests here are related to the correct creation of objects for quizzes with
different sets of data.
"""

class BasicObjectsCreation(TestCase):
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

    def testCreateQuizLive(self):
        """
        Create quiz providing basic fields with LIVE_STATUS and slug.
        """
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.filter(status=status).count(), 1)
        self.assertEqual(Quiz.objects.get(slug=self.slug).title, self.title)

    def testCreateQuizLiveAutomaticSlug(self):
        """
        Create quiz providing basic fields with LIVE_STATUS and no slug so it will be created automatically.
        """
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=None, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.get(title=self.title).title, self.title)
        self.assertEqual(quiz.slug, slugify(self.title))

    def testCreateQuizLiveWithCategories(self):
        """
        Create quiz providing basic fields with LIVE_STATUS and two categories.
        """
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        c1 = Category.objects.create(title='Programming', slug='programming')
        c2 = Category.objects.create(title='Science', slug='science')
        quiz.categories.add(c1, c2)
        categories = Quiz.objects.get(slug=self.slug).categories.all()
        self.assertEqual(Quiz.objects.get(slug=self.slug).categories.count(), 2)
        self.assertEqual(categories[0], c1)
        self.assertEqual(categories[1], c2)

    def testCreateQuizDraft(self):
        """
        Create quiz providing basic fields with DRAFT_STATUS.
        """

        status = Quiz.DRAFT_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.filter(status=status).count(), 1)
        self.assertEqual(Quiz.objects.get(slug=self.slug).title, self.title)

    def testCreateQuizHidden(self):
        """
        Create quiz providing basic fields with HIDDEN_STATUS.
        """

        status = Quiz.HIDDEN_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.filter(status=status).count(), 1)
        self.assertEqual(Quiz.objects.get(slug=self.slug).title, self.title)

    def testCreateQuizWithoutStartsEnds(self):
        """
        Create quiz without providing opens and closes.
        Closes automatically set to 30 days after opens.
        """

        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        default_starts = now()
        default_ends = now() + timedelta(days=30)
        current_tz = get_current_timezone()

        self.assertEqual(quiz.starts.day, default_starts.day)
        self.assertEqual(quiz.starts.month, default_starts.month)
        self.assertEqual(quiz.starts.year, default_starts.year)
        self.assertEqual(quiz.starts.hour, default_starts.hour)
        self.assertEqual(quiz.starts.minute, default_starts.minute)
        self.assertEqual(quiz.starts.tzinfo, default_starts.tzinfo)

        self.assertEqual(quiz.ends.day, default_ends.day)
        self.assertEqual(quiz.ends.month, default_ends.month)
        self.assertEqual(quiz.ends.year, default_ends.year)
        self.assertEqual(quiz.ends.hour, default_ends.hour)
        self.assertEqual(quiz.ends.minute, default_ends.minute)
        self.assertEqual(quiz.ends.tzinfo, default_ends.tzinfo)

    def testCreateQuizWithStartsEnds(self):
        """
        Create quiz providing opens and closes. We set closes to 15 days after opens.
        """
        status = Quiz.LIVE_STATUS
        starts = now()
        ends = now() + timedelta(days=15)
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status, starts=starts, ends=ends)
        quiz.save()

        current_tz = get_current_timezone()

        self.assertEqual(quiz.starts.day, starts.day)
        self.assertEqual(quiz.starts.month, starts.month)
        self.assertEqual(quiz.starts.year, starts.year)
        self.assertEqual(quiz.starts.hour, starts.hour)
        self.assertEqual(quiz.starts.minute, starts.minute)
        self.assertEqual(quiz.starts.tzinfo, starts.tzinfo)

        self.assertEqual(quiz.ends.day, ends.day)
        self.assertEqual(quiz.ends.month, ends.month)
        self.assertEqual(quiz.ends.year, ends.year)
        self.assertEqual(quiz.ends.hour, ends.hour)
        self.assertEqual(quiz.ends.minute, ends.minute)
        self.assertEqual(quiz.ends.tzinfo, ends.tzinfo)

    def testCreateQuestion(self):
        """
        Create two questions for one quiz, then retrieve the quiz and count its questions.
        """
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()

        question_1 = Question(question='Choose your color', quiz=quiz)
        question_1.save()

        question_2 = Question(question='Choose your month', quiz=quiz)
        question_2.save()

        self.assertEqual(Quiz.objects.get(slug=self.slug).question_set.count(), 2)

    def testCreateAnswer(self):
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()

        question = Question(question='Choose your color', quiz=quiz)
        question.save()

        answer = Answer(letter='a', answer='Blue', question=question, points=5)
        answer.save()

        self.assertEqual(Quiz.objects.get(slug=self.slug).question_set.all()[0].answer_set.count(), 1)

    def testCreateUserQuizAnswer(self):
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()

        question = Question(question='Choose your color', quiz=quiz)
        question.save()

        answer = Answer(letter='a', answer='Blue', question=question, points=5)
        answer.save()

        user_quiz_answer = UserQuizAnswer(user=self.regular_user , quiz=quiz, answer=answer)
        user_quiz_answer.save()

        self.assertEqual(self.regular_user.userquizanswer_set.count(), 1)

    def testCreateQuizResult(self):
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()

        quiz_result = QuizResult(letter='a', quiz=quiz, description='Description of this quiz result')
        quiz_result.save()

        self.assertEqual(Quiz.objects.get(slug=self.slug).quizresult_set.count(), 1)
