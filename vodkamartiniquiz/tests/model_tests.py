from django.test import TestCase
from django.core.cache import cache
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User
from vodkamartinicategory.models import Category
from vodkamartiniquiz.models import Quiz, Question, Answer, UserQuizAnswer, QuizResult

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
        self.editor = User.objects.create_user(username='mark_editor', password='secret')

        self.title = 'A Quiz Title'
        self.body = 'This is the body for the quiz test'
        self.slug='the-quiz'

    def testCreateQuizLive(self):
        """
        Verify quiz creation providing basic fields with LIVE_STATUS.
        """

        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, slug=self.slug, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.filter(status=Quiz.LIVE_STATUS).count(), 1)
        self.assertEqual(Quiz.objects.get(slug=self.slug).title, self.title)

    def testCreateQuizLiveAutomaticSlug(self):
        status = Quiz.LIVE_STATUS
        quiz = Quiz(title=self.title, body=self.body, author=self.editor, status=status)
        quiz.save()
        self.assertEqual(Quiz.objects.get(title=self.title).title, self.title)
        self.assertEqual(quiz.slug, slugify(self.title))

    def testCreateQuizLiveWithCategories(self):
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
