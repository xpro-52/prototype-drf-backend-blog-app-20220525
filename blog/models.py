from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from django.contrib.auth import get_user_model


class Author(models.Model):
    name = models.CharField(_("name"), max_length=50)
    dob = models.DateField(_("date of birth"), blank=True)
    text = models.TextField(_("text"), blank=True)
    user = models.OneToOneField(to=get_user_model(), verbose_name=_("user"), on_delete=models.CASCADE)
    
    def __str__(self) -> str:
        return "<Author:name=%s>" % (self.name)


class Post(models.Model):
    title = models.CharField(_("title"), max_length=150)
    body = models.TextField(_("body"))
    created_date = models.DateTimeField(_("created date"), default=timezone.now)
    updated_date = models.DateTimeField(_("updated date"), blank=True, null=True)
    author = models.ForeignKey("blog.Author", verbose_name=_("author"), on_delete=models.CASCADE)

    def __str__(self) -> str:
        return "<Post:title=%s, author=%s>" % (
            self.title, self.author
        )
