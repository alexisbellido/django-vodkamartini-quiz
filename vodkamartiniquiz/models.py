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
        permissions = (
                ('view_quiz', 'View quiz'),
                ('take_quiz', 'Can take quiz'),
        )

class Question(models.Model):
    weight = models.IntegerField(default=0)
    question = models.TextField()
    quiz = models.ForeignKey(Quiz)
    enabled = models.BooleanField(default=True)
    #voted_up_by = models.ManyToManyField(User, blank=True, related_name='answers_voted_up') # Users who voted up this answer

    def __unicode__(self):
        return "%s..." % (self.question[:50],)

class Answer(models.Model):
    answer_letter = models.CharField(max_length=1)
    answer = models.TextField()
    question = models.ForeignKey(Question)
    points = models.IntegerField(default=0)

    def __unicode__(self):
        return "%s..." % (self.answer[:50],)

class UserQuizAnswer(models.Model):
    user = models.ForeignKey(User)
    quiz = models.ForeignKey(Quiz)
    answer = models.ForeignKey(Answer)

class QuizResult(models.Model):
    """
    Defines criteria for quiz results.
    """
    answer_letter = models.CharField(max_length=1)
    quiz = models.ForeignKey(Quiz)
    description = models.TextField()
    min_points = models.IntegerField(default=0)
    max_points = models.IntegerField(default=0)
