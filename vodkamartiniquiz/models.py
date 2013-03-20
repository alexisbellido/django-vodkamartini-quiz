from datetime import timedelta
from django.utils.timezone import now
from django.db import models
from django.contrib.auth.models import User
from vodkamartiniarticle.models import BaseArticle

"""
There is a quiz, and then a quiz has multiple questions and each question has a set of
potential answers (a, b, c, d, etc).

Quizzes results for a user depend on what answers a user chose for the questions in a quiz and the score method.

The letters method is used for quizzes where "mostly As means this" and "mostly Bs means that."

The points method is used for quizzes where "from 10 to 20 points means this" and "from 21 to 30 points means that."

"""

class Quiz(BaseArticle):
    LETTERS_SCORING = 1
    POINTS_SCORING = 2
    SCORING = (
        (LETTERS_SCORING, 'Letters'),
        (POINTS_SCORING, 'Points'),
    )

    starts = models.DateTimeField(blank=True)
    ends = models.DateTimeField(blank=True)
    scoring = models.IntegerField(choices=SCORING, default=LETTERS_SCORING)

    @models.permalink
    def get_absolute_url(self):
        return ('vodkamartiniquiz_quiz_detail', (), {'slug': self.slug})

    class Meta(BaseArticle.Meta):
        verbose_name_plural = "Quizzes"
        permissions = (
                ('view_quiz', 'View quiz'),
                ('take_quiz', 'Can take quiz'),
        )

    def getFirstQuestionId(self):
        first_question_id = self.question_set.filter(enabled=True).order_by('weight', 'pk')[0].pk
        return first_question_id

    def save(self, *args, **kwargs):
        """
        Set starts to today's date and ends 30 days in the future.
        """
        if not self.pk and not self.starts:
            self.starts = now()

        if not self.pk and not self.ends:
            self.ends = now() + timedelta(days=30)

	#import pdb; pdb.set_trace()
        super(Quiz, self).save(*args, **kwargs)


class Question(models.Model):
    weight = models.IntegerField(default=0)
    question = models.TextField()
    quiz = models.ForeignKey(Quiz)
    enabled = models.BooleanField(default=True)

    def __unicode__(self):
        return "%s..." % (self.question[:50],)

    @models.permalink
    def get_absolute_url(self):
        return ('vodkamartiniquiz_question_detail', (), {'pk': self.pk})

    def getQuestionsPkList(self):
        """
        Gets a list of questions' pk ordered by weight and pk.
        This list will be used by getQuestionNextPk and getQuestionPreviousPk in vodkamartiniquiz.views
        and requires just one extra database query.
        """
        question_list = self.quiz.question_set.filter(enabled=True).order_by('weight', 'pk')
        pk_list = []
        for question in question_list:
            pk_list.append(question.pk)
        return pk_list


class Answer(models.Model):
    letter = models.CharField(max_length=1)
    answer = models.TextField()
    question = models.ForeignKey(Question)
    points = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s. %s" % (self.letter.upper(), self.answer)

class UserQuizAnswerManager(models.Manager):
    """
    Manager with additional methods.
    """

    def userquizanswers(self, quiz, user):
        """
        Returns all answers for a specific user and quiz.
        The letter most often used for answers for quizzes with letters scoring or
        the total points for quizzes using points scoring.
        """

        userquizanswers = self.model.objects.filter(quiz=quiz, user=user)
        return userquizanswers

class UserQuizAnswer(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    answer = models.ForeignKey(Answer)
    objects = UserQuizAnswerManager()

class QuizResultManager(models.Manager):
    """
    Manager with additional methods.
    """

    def userquizresult(self, quiz, user):
        """
        Returns result for a specific user and quiz.
        The letter most often used for answers for quizzes with letters scoring or
        the total points for quizzes using points scoring.
        """

        userquizanswers = UserQuizAnswer.objects.userquizanswers(quiz, user)
        print "userquizanswers from the manager method"
        print userquizanswers
        for x in userquizanswers:
            print x.answer
        if quiz.scoring == Quiz.LETTERS_SCORING:
            print "letters scoring"
            quizresult = None
        if quiz.scoring == Quiz.POINTS_SCORING:
            # TODO when we activate points scoring
            quizresult = None
        quizresult = None
        return quizresult

class QuizResult(models.Model):
    """
    Defines criteria for quiz results.
    """
    letter = models.CharField(max_length=1)
    quiz = models.ForeignKey(Quiz)
    description = models.TextField()
    min_points = models.IntegerField(default=0)
    max_points = models.IntegerField(default=0)
    objects = QuizResultManager()

    class Meta:
        ordering = ["-quiz", "letter", "max_points"]

    def __unicode__(self):
        return "%s: %s..." % (self.quiz.title, self.description[:40])
