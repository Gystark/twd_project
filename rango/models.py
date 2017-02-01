from __future__ import unicode_literals

from datetime import datetime
from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    name = models.CharField(max_length=128, unique=True)
    views = models.IntegerField(default=0)
    likes = models.IntegerField(default=0)
    slug = models.SlugField(unique=True)

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)

        if self.views < 0:
            self.views = 0

        if self.likes < 0:
            self.likes = 0

        super(Category, self).save(*args, **kwargs)

    class Meta:
        verbose_name_plural = "Categories"


class Page(models.Model):
    category = models.ForeignKey(Category)
    title = models.CharField(max_length=128)
    url = models.URLField()
    views = models.IntegerField(default=0)
    last_visit = models.DateTimeField(default=datetime.now)
    first_visit = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return self.title

    def save(self, *args, **kwargs):
        """
        Custom save method to make Chapter 8 tests pass.
        """

        if self.last_visit > datetime.now():
            self.last_visit = datetime.now()

        if self.first_visit > datetime.now():
            self.first_visit = datetime.now()

        if self.last_visit < self.first_visit:
            self.last_visit = datetime.now()

        super(Page, self).save(*args, **kwargs)

