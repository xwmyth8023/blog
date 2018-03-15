from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.six import python_2_unicode_compatible
from django.utils.html import strip_tags
import markdown

# Define category model
@python_2_unicode_compatible
class Category(models.Model):
    # Define category name
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

# Define Tag model
@python_2_unicode_compatible
class Tag(models.Model):
    # Define tag name
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Post(models.Model):
    # article's title
    title = models.CharField(max_length=70)
    # artilcle's body
    body = models.TextField()
    # article's created time
    createdTime = models.DateTimeField()
    # article's modified time
    modifiedTime = models.DateField()
    # article's excerpt
    excerpt = models.CharField(max_length=200,blank=True)
    # article's category; 一对多
    category = models.ForeignKey(Category)
    # article's tag; 多对多
    tags = models.ManyToManyField(Tag)
    # article's author; 一对多
    author = models.ForeignKey(User)
    # article's views;
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:detail',kwargs={'pk':self.pk})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views']) 

    def save(self,*args,**kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions = ['markdown.extensions.extra','markdown.extensions.codehilite'])
            self.excerpt = strip_tags(md.convert(self.body))[:54]
        super(Post,self).save(*args,**kwargs)

    class Meta():
        ordering = ['-createdTime']

