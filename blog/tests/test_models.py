from django.test import TestCase
from django.contrib.auth.models import User
# Create your tests here.

from blog.models import Article, Comment, Tag


class ModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        tag = Tag.objects.create(name=set('Fruit',))
        tag.save()
        user = User()
        user.save()
        article = Article( title='New article')
        article.(tag, user,)
        article.save()
        Comment.objects.create(user=User, email='nik.vag199@mail.ru', name='Nik', text='Some text', article='New article')

    def test_title_label(self):
        tag = Tag.objects.get(id=1)
        tag_label = tag._meta.get_field('name').verbose_name
        self.assertEqual(tag_label, 'Тэг')
