import json
from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django_fake_model import models as f

class Address(models.Model):
	street = models.CharField(max_length=255)  
	suite = models.CharField(max_length=255) 
	city = models.CharField(max_length=255)
	zipcode = models.CharField(max_length=255)

	@classmethod
	def save_from_json(cls, street, suite, city, zipcode, *args, **kwargs):
		return cls.objects.create(street=street, suite=suite, city=city, zipcode=zipcode)

class User(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	address = models.OneToOneField('Address', related_name='user', on_delete=models.CASCADE)
	
	def __str__(self):
		return '%s - %s' % (self.email, self.name)

	@property	
	def total_posts(self):
		return self.posts.count()

	@property	
	def total_comments(self):
		total = sum(list(map(lambda x: x.total_comments, list(self.posts.all()))))
		return total

	@classmethod
	def save_from_json(cls, id, name, email, address, *args, **kwargs):
		return cls.objects.create(pk=id, name=name, email=email, address=Address.save_from_json(**address))

class Post(models.Model):
	title = models.CharField(max_length=255)
	body = models.CharField(max_length=255)
	user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='posts')
	
	def __str__(self):
		return '%s - %s' % (self.pk, self.title)

	@property	
	def total_comments(self):
		return self.comments.count()

	@classmethod
	def save_from_json(cls, userId, id, title, body, *args, **kwargs):
		return cls.objects.create(pk=id, title=title, body=body, user=User.objects.get(pk=userId))

class Comment(models.Model):
	name = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	body = models.CharField(max_length=255)
	post = models.ForeignKey('Post', on_delete=models.CASCADE, related_name='comments')
	
	def __str__(self):
		return '%s - %s' % (self.pk, self.name)

	@classmethod
	def save_from_json(cls, postId, id, name, email, body, *args, **kwargs):
		return cls.objects.create(pk=id, name=name, email=email, body=body, post=Post.objects.get(pk=postId))

# Fake Model:
class File(f.FakeModel):
	file = models.FileField(blank=False, null=False)
	timestamp = models.DateTimeField(auto_now_add=True)