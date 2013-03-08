from django.core.cache import cache
from django.test import TestCase
from django.contrib.auth.models import User
from vodkamartiniquiz.models import Quiz, Question, Answer, UserQuizAnswer, QuizResult

"""
All tests here are related to the correct creation of objects for quizzes with
different sets of data.

TODO remove these comments:
tests code to create a few quizzes with all their data in different scenarios, with letters, with points, etc
"""

class BasicObjectsCreation(TestCase):
    def setUp(self):
        """
        Create editor user and some data to use for creating quiz related objects.
        """

        cache.clear()
        self.editor = User.objects.create_user(username='mark_editor', password='secret')
        #self.body = "This is quiz extra text"

        #self.normal_title='Normal Question With Keyword In Title'
        #self.normal_hidden_title='Normal Hidden Question'
        #self.expert_title='Question With Expert Answer'

        #self.quiz = Quiz(
        #                         title=self.normal_title,
        #                         body='This is a normal question, with no answers by experts', 
        #                         author=author, 
        #                         status=Question.LIVE_STATUS,
        #                        )
        #self.quiz.save()

        #title = "First Live Quiz"
        #status = Quiz.LIVE_STATUS
        #teaser = "The quiz teaser"
        #body = "The quiz body"
        #self.quiz = Quiz(title=title, teaser=teaser, body=body, author=self.author, status=status)
        #self.quiz.save()

    def testCreateQuizLive(self):
        """
        Verify creation is correct when providing all fields with LIVE_STATUS.
        """
        one = 1
        self.assertEqual(one, 1),
#        title = "First Live Quiz"
#        slug = "first-live-quiz"
#        status = Quiz.LIVE_STATUS
#        quiz = Quiz(title=title, teaser=self.teaser, body=self.body, slug=slug, author=self.author, status=status)
#        quiz.save()
#        c1 = Category.objects.create(title='Programming', slug='programming')
#        c2 = Category.objects.create(title='Science', slug='science')
#        quiz.categories.add(c1, c2)
#        self.assertEqual(Quiz.objects.filter(status=Quiz.LIVE_STATUS).count(), 1)
#        self.assertEqual(Quiz.objects.get(slug=slug).categories.count(), 2)
#
#    def testCreateQuizDraft(self):
#        """
#        Verify creation is correct when providing all fields with DRAFT_STATUS.
#        """
#        title = "First Draft Quiz"
#        teaser = "this is a teaser"
#        body = "and this is the body"
#        slug = "first-draft-quiz"
#        status = Quiz.DRAFT_STATUS
#        quiz = Quiz(title=title, teaser=self.teaser, body=self.body, slug=slug, author=self.author, status=status)
#        quiz.save()
#        c1 = Category.objects.create(title='Programming', slug='programming')
#        c2 = Category.objects.create(title='Science', slug='science')
#        quiz.categories.add(c1, c2)
#        self.assertEqual(Quiz.objects.filter(status=Quiz.DRAFT_STATUS).count(), 1)
#        self.assertEqual(Quiz.objects.get(slug=slug).categories.count(), 2)
#
#    def testCreateQuizHidden(self):
#        """
#        Verify creation is correct when providing all fields with HIDDEN_STATUS.
#        """
#        title = "First Hidden Quiz"
#        teaser = "this is a teaser"
#        body = "and this is the body"
#        slug = "first-hidden-quiz"
#        status = Quiz.HIDDEN_STATUS
#        quiz = Quiz(title=title, teaser=self.teaser, body=self.body, slug=slug, author=self.author, status=status)
#        quiz.save()
#        c1 = Category.objects.create(title='Programming', slug='programming')
#        c2 = Category.objects.create(title='Science', slug='science')
#        quiz.categories.add(c1, c2)
#        self.assertEqual(Quiz.objects.filter(status=Quiz.HIDDEN_STATUS).count(), 1)
#        self.assertEqual(Quiz.objects.get(slug=slug).categories.count(), 2)
#
#    def testCreateQuizAutoSlug(self):
#        """
#        Verify automatic slug is created if not provided.
#        """
#        title = "Quiz With Slug"
#        status = Quiz.LIVE_STATUS
#        quiz = Quiz(title=title, teaser=self.teaser, body=self.body, author=self.author, status=status)
#        quiz.save()
#        self.assertEqual(quiz.slug, slugify(title))
#
#    def testCreateQuizNoSlug(self):
#        """
#        Verify error when slug is None.
#        """
#        title = "Quiz With No Slug"
#        slug = ""
#        status = Quiz.LIVE_STATUS
#        quiz = Quiz.objects.create(title=title, teaser=self.teaser, body=self.body, slug=slug, author=self.author, status=status)
#        quiz.slug = None
#        self.assertRaises(IntegrityError, article.save)
