# -*- coding: utf-8 -*-
from django import forms
from django.conf import settings
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _

from .models import Comment


class CommentForm(forms.ModelForm):
    rating = forms.IntegerField(widget=forms.RadioSelect(choices=Comment.CHOICES_RATING), required=True)
    text = forms.CharField(widget=forms.Textarea(attrs={'placeholder': ''}), label=_("Comment text"),
                           help_text=_("Tell us your point of view. Would you recommend it? Why?"), )

    content_type = forms.CharField(widget=forms.HiddenInput, required=False)
    object_id = forms.CharField(widget=forms.HiddenInput)

    class Meta:
        model = Comment
        fields = ['text', 'rating', 'object_id']

    def __init__(self, data=None, target_object=None, initial=None, *args, **kwargs):
        if target_object:
            initial = dict(
                content_type=target_object._meta,
                object_id=force_text(target_object._get_pk_val()),
                site_id=getattr(settings, "SITE_ID", None),
            )
        super(CommentForm, self).__init__(data, initial=initial, *args, **kwargs)

        for key, value in self.fields.items():
            self.fields[key].widget.attrs['placeholder'] = self.fields[key].help_text or None
            self.fields[key].widget.attrs['class'] = "mlc"
