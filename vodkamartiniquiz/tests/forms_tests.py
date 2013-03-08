from django.test import TestCase

#class QuizForms(TestCase):
#
#    def setUp(self):
#        """
#        Create group editor and corresponding permissions to do everything with quizzes, then create a user assigned to that group.
#        Create one user without any special permissions who can can just view and take quizzes.
#        """
#
#        cache.clear()
#        self.regular = User.objects.create_user(username='bill_normal', password='secret')
#        self.editor = User.objects.create_user(username='mark_editor', password='secret')
#
#        self.perms = {
#            'add_quiz': Permission.objects.get(codename='add_quiz', content_type__app_label='vodkamartiniquiz'),
#            'change_quiz': Permission.objects.get(codename='change_quiz', content_type__app_label='vodkamartiniquiz'),
#            'delete_quiz': Permission.objects.get(codename='delete_quiz', content_type__app_label='vodkamartiniquiz'),
#            'view_quiz': Permission.objects.get(codename='view_quiz', content_type__app_label='vodkamartiniquiz'),
#            'take_quiz': Permission.objects.get(codename='take_quiz', content_type__app_label='vodkamartiniquiz'),
#
#            'add_question': Permission.objects.get(codename='add_question', content_type__app_label='vodkamartiniquiz'),
#            'change_question': Permission.objects.get(codename='change_question', content_type__app_label='vodkamartiniquiz'),
#            'delete_question': Permission.objects.get(codename='delete_question', content_type__app_label='vodkamartiniquiz'),
#
#            'add_answer': Permission.objects.get(codename='add_answer', content_type__app_label='vodkamartiniquiz'),
#            'change_answer': Permission.objects.get(codename='change_answer', content_type__app_label='vodkamartiniquiz'),
#            'delete_answer': Permission.objects.get(codename='delete_answer', content_type__app_label='vodkamartiniquiz'),
#
#            'add_userquizanswer': Permission.objects.get(codename='add_userquizanswer', content_type__app_label='vodkamartiniquiz'),
#            'change_userquizanswer': Permission.objects.get(codename='change_userquizanswer', content_type__app_label='vodkamartiniquiz'),
#            'delete_userquizanswer': Permission.objects.get(codename='delete_userquizanswer', content_type__app_label='vodkamartiniquiz'),
#
#            'add_quizresult': Permission.objects.get(codename='add_quizresult', content_type__app_label='vodkamartiniquiz'),
#            'change_quizresult': Permission.objects.get(codename='change_quizresult', content_type__app_label='vodkamartiniquiz'),
#            'delete_quizresult': Permission.objects.get(codename='delete_quizresult', content_type__app_label='vodkamartiniquiz'),
#        }
#
#        self.group_editor = Group.objects.create(name='editor')
#        self.group_editor.permissions.add(
#                                            self.perms['add_quiz'], 
#                                            self.perms['change_quiz'], 
#                                            self.perms['delete_quiz'],
#                                            self.perms['view_quiz'],
#                                            self.perms['take_quiz'],
#
#                                            self.perms['add_question'], 
#                                            self.perms['change_question'], 
#                                            self.perms['delete_question'],
#
#                                            self.perms['add_answer'], 
#                                            self.perms['change_answer'], 
#                                            self.perms['delete_answer'],
#
#                                            self.perms['add_userquizanswer'], 
#                                            self.perms['change_userquizanswer'], 
#                                            self.perms['delete_userquizanswer'],
#
#                                            self.perms['add_quizresult'], 
#                                            self.perms['change_quizresult'], 
#                                            self.perms['delete_quizresult'],
#                                         )
#
#        self.editor.groups.add(self.group_editor)
#
#    def setUp(self):
#        """
#        Create one question marked as normal and one question marked as answered by expert.
#        Notice the normal question has "Keyword" in the title, which is used for testing the basic search view.
#        django.test.client.Client gets confused with templates when using the cache, that's why we need to clear it.
#        """
#        cache.clear()
#        author = User.objects.create_user(username='joe', password='qwerty')
#        self.normal_title='Normal Question With Keyword In Title'
#        self.normal_hidden_title='Normal Hidden Question'
#        self.expert_title='Question With Expert Answer'
#
#        self.question = Question(
#                                 title=self.normal_title,
#                                 body='This is a normal question, with no answers by experts', 
#                                 author=author, 
#                                 status=Question.LIVE_STATUS,
#                                )
#        self.question.save()
#
#        self.expert_question = Question(
#                                 title=self.expert_title,
#                                 body='This is a question with at least one answer by experts', 
#                                 author=author, 
#                                 status=Question.LIVE_STATUS,
#                                 has_expert_answer=True,
#                                )
#        self.expert_question.save()
#
#        self.hidden_question = Question(
#                                 title=self.normal_hidden_title,
#                                 body='This is a normal hidden question', 
#                                 author=author, 
#                                 status=Question.HIDDEN_STATUS,
#                               )
#        self.hidden_question.save()
#
#
#    def tearDown(self):
#        self.client.logout()
#
#    def testAddQuiz(self):
#        """
#        There's a media directory below the tests directory where this file lives, and we use the file image.png there for posting an article.
#        """
#        logged_in = self.client.login(username='joe_author', password='secret')
#        self.assertEqual(logged_in, True, 'The user was not logged in.')
#        current_dir = os.path.dirname(os.path.abspath(__file__))
#        image_file = open("%s/media/image.png" % current_dir, "rb")
#        data = {'title': 'my title', 'teaser': 'my teaser', 'body': 'my body', 'image': image_file}
#        response = self.client.post(reverse('vodkamartiniarticle_article_add'), data, follow=True)
#        image_file.close()
#        try:
#            article = Article.objects.get(slug=slugify(data['title']))
#        except Article.DoesNotExist:
#            self.assertTrue(False, "The article was not created. Apparently the user did not have the correct permissions.")
#        self.assertTemplateUsed(response, 'vodkamartiniarticle/article_detail.html')
#        self.assertEqual(article.title, data['title'])
#
