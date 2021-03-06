from django.conf.urls import patterns, url
from .views import QuizHome, QuizDetail, QuestionDetail, QuizResultDetail

urlpatterns = patterns('vodkamartiniquiz.views',
    url(r'^$', QuizHome.as_view(), name='vodkamartiniquiz_quiz_home'),
    #url(r'^add/$', QuizCreate.as_view(), name='vodkamartiniquiz_quiz_create'),
    url(r'^(?P<slug>[-\w]+)/question/(?P<pk>\d+)/$', QuestionDetail.as_view(), name='vodkamartiniquiz_question_detail'),
    url(r'^(?P<slug>[-\w]+)/result/$', QuizResultDetail.as_view(), name='vodkamartiniquiz_quizresult_detail'),
    url(r'^(?P<slug>[-\w]+)/$', QuizDetail.as_view(), name='vodkamartiniquiz_quiz_detail'),
)
