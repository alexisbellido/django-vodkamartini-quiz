# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Quiz'
        db.create_table('vodkamartiniquiz_quiz', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('title', self.gf('django.db.models.fields.CharField')(max_length=200)),
            ('teaser', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body', self.gf('django.db.models.fields.TextField')()),
            ('image', self.gf('django.db.models.fields.files.ImageField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('updated', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, blank=True)),
            ('teaser_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('body_html', self.gf('django.db.models.fields.TextField')(blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=128)),
            ('author', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('status', self.gf('django.db.models.fields.IntegerField')(default=2)),
            ('enable_comments', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('featured', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('starts', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('ends', self.gf('django.db.models.fields.DateTimeField')(blank=True)),
            ('scoring', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('vodkamartiniquiz', ['Quiz'])

        # Adding M2M table for field categories on 'Quiz'
        db.create_table('vodkamartiniquiz_quiz_categories', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('quiz', models.ForeignKey(orm['vodkamartiniquiz.quiz'], null=False)),
            ('category', models.ForeignKey(orm['vodkamartinicategory.category'], null=False))
        ))
        db.create_unique('vodkamartiniquiz_quiz_categories', ['quiz_id', 'category_id'])

        # Adding model 'Question'
        db.create_table('vodkamartiniquiz_question', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('weight', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('question', self.gf('django.db.models.fields.TextField')()),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vodkamartiniquiz.Quiz'])),
            ('enabled', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('vodkamartiniquiz', ['Question'])

        # Adding model 'Answer'
        db.create_table('vodkamartiniquiz_answer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('answer', self.gf('django.db.models.fields.TextField')()),
            ('question', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vodkamartiniquiz.Question'])),
            ('points', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('vodkamartiniquiz', ['Answer'])

        # Adding model 'UserQuizAnswer'
        db.create_table('vodkamartiniquiz_userquizanswer', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vodkamartiniquiz.Quiz'])),
            ('answer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vodkamartiniquiz.Answer'])),
        ))
        db.send_create_signal('vodkamartiniquiz', ['UserQuizAnswer'])

        # Adding model 'QuizResult'
        db.create_table('vodkamartiniquiz_quizresult', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('letter', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('quiz', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['vodkamartiniquiz.Quiz'])),
            ('description', self.gf('django.db.models.fields.TextField')()),
            ('min_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('max_points', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('vodkamartiniquiz', ['QuizResult'])


    def backwards(self, orm):
        # Deleting model 'Quiz'
        db.delete_table('vodkamartiniquiz_quiz')

        # Removing M2M table for field categories on 'Quiz'
        db.delete_table('vodkamartiniquiz_quiz_categories')

        # Deleting model 'Question'
        db.delete_table('vodkamartiniquiz_question')

        # Deleting model 'Answer'
        db.delete_table('vodkamartiniquiz_answer')

        # Deleting model 'UserQuizAnswer'
        db.delete_table('vodkamartiniquiz_userquizanswer')

        # Deleting model 'QuizResult'
        db.delete_table('vodkamartiniquiz_quizresult')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'vodkamartinicategory.category': {
            'Meta': {'ordering': "['title']", 'object_name': 'Category'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '50'}),
            'summary': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '250'})
        },
        'vodkamartiniquiz.answer': {
            'Meta': {'object_name': 'Answer'},
            'answer': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'question': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vodkamartiniquiz.Question']"})
        },
        'vodkamartiniquiz.question': {
            'Meta': {'object_name': 'Question'},
            'enabled': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'question': ('django.db.models.fields.TextField', [], {}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vodkamartiniquiz.Quiz']"}),
            'weight': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'vodkamartiniquiz.quiz': {
            'Meta': {'ordering': "['-created']", 'object_name': 'Quiz'},
            'author': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'body': ('django.db.models.fields.TextField', [], {}),
            'body_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'categories': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['vodkamartinicategory.Category']", 'symmetrical': 'False', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'enable_comments': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'ends': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'featured': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'blank': 'True'}),
            'scoring': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '128'}),
            'starts': ('django.db.models.fields.DateTimeField', [], {'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '2'}),
            'teaser': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'teaser_html': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '200'}),
            'updated': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'blank': 'True'})
        },
        'vodkamartiniquiz.quizresult': {
            'Meta': {'object_name': 'QuizResult'},
            'description': ('django.db.models.fields.TextField', [], {}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'letter': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'max_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'min_points': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vodkamartiniquiz.Quiz']"})
        },
        'vodkamartiniquiz.userquizanswer': {
            'Meta': {'object_name': 'UserQuizAnswer'},
            'answer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vodkamartiniquiz.Answer']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'quiz': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['vodkamartiniquiz.Quiz']"}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"})
        }
    }

    complete_apps = ['vodkamartiniquiz']