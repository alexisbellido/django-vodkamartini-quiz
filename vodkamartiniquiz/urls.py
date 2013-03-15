from django.conf.urls.defaults import patterns, url
from .views import QuizHome, QuizDetail, QuestionDetail
#from .views import QuizCreate

urlpatterns = patterns('vodkamartiniquiz.views',
    url(r'^$', QuizHome.as_view(), name='vodkamartiniquiz_quiz_home'),
    #url(r'^add/$', QuizCreate.as_view(), name='vodkamartiniquiz_quiz_create'),
    url(r'^(?P<slug>[-\w]+)/question/(?P<pk>\d+)/$', QuestionDetail.as_view(), name='vodkamartiniquiz_question_detail'),
    url(r'^(?P<slug>[-\w]+)/$', QuizDetail.as_view(), name='vodkamartiniquiz_quiz_detail'),
)
