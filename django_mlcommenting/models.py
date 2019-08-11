# -*- coding: utf-8 -*-
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.db import models
from django.db.models import Avg
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _

COMMENT_MAX_LENGTH = 3000
COMMENT_MAX_RATING = 5


class Comment(models.Model):
    CHOICES_RATING = (
        (5, 'very good'),
        (4, 'good'),
        (3, 'ok'),
        (2, 'poor'),
        (1, 'pretty poor'),
    )

    # Generic foreign key
    content_type = models.ForeignKey(ContentType, verbose_name=_('content type'),
                                     related_name="content_type_set_for_%(class)s",
                                     on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    user = models.ForeignKey(User, verbose_name=_('user'),
                             related_name="%(class)s_comments", null=True, blank=True,
                             on_delete=models.CASCADE)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    is_removed = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    text = models.CharField(max_length=COMMENT_MAX_LENGTH, blank=True, null=True)
    rating = models.IntegerField(verbose_name=_('comment rating'), choices=CHOICES_RATING)

    site = models.ForeignKey(Site, on_delete=models.CASCADE, null=True, blank=True)

    ip_address = models.GenericIPAddressField(null=True, blank=True)

    @property
    def name(self):
        return self.text

    @property
    def username(self):
        if self.user:
            return self.user
        return "None"

    @property
    def get_rating(self):
        return float(self.rating)

    @property
    def rating_html(self):
        html = ""
        for _ in range(0, self.rating):
            html += render_to_string('django_mlcommenting/comment_rating_element_active.html')
        stars_inactive = COMMENT_MAX_RATING - self.rating
        for _ in range(0, stars_inactive):
            html += render_to_string('django_mlcommenting/comment_rating_element_inactive.html', )
        return html

    def liked(self, user):
        return CommentVote.objects.filter(comment=self, user=user).first()

    def get_absolute_url(self):
        return reverse('django_mlcommenting:detail', kwargs={'pk': self.id})

    def __str__(self):
        return "%s - %.1f - %s..." % (self.username, self.rating, self.name[:50],)

    @property
    def get_content_type_app_label(self):
        return self.content_type.app_label

    @property
    def get_content_type_model(self):
        return self.content_type.model

    @staticmethod
    def get_avg_rating(generic_relation):
        return generic_relation.all().aggregate(Avg('rating'))


class CommentVote(models.Model):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return "%s - %s" % (self.user.username, self.comment.text[:10])
