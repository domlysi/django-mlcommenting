# -*- coding: utf-8 -*-

from django.apps import apps
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.http import HttpResponseNotAllowed, HttpResponseBadRequest, JsonResponse
from django.shortcuts import redirect, render, get_object_or_404
from django.template.loader import render_to_string
from django.utils.html import escape
from django.utils.translation import gettext_lazy as _
from django.views import generic
from django.views.decorators.http import require_POST

from .forms import CommentForm
from .models import Comment, CommentVote


class CommentDetailView(generic.DetailView):
    model = Comment


class CommentListView(generic.ListView):
    model = Comment

    def get_context_data(self, **kwargs):
        context = super(CommentListView, self).get_context_data(**kwargs)
        return context


class CommentCreateView(generic.CreateView):
    model = Comment
    # fields = ("text", "rating", )
    form_class = CommentForm


class CommentUpdateView(generic.UpdateView):
    model = Comment
    fields = ['text', ]


def comment_delete(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You need to log in")
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return HttpResponseNotAllowed("You are not the owner")

    if not request.POST.get('sure', None):
        html = render_to_string(request=request,
                                template_name='django_mlcommenting/comment_delete_confirm.html',
                                context={'comment': comment})
        return JsonResponse({
            'html': html,
            'status': 'confirm'
        })
    else:

        try:
            comment.delete()
        except Exception as e:
            html = render_to_string(
                template_name='django_mlcommenting/msgs/comment_msg.html',
                context={
                    'msg': e,
                    'status': 'error'
                }
            )
            return JsonResponse({
                'html': html,
                'status': ''
            }, status=400)

        html = render_to_string(template_name='django_mlcommenting/msgs/comment_msg.html',
                                context={
                                    'status': 'info',
                                    'msg': _("Your comment has been deleted")
                                })
        return JsonResponse({
            'html': html,
            'status': 'deleted'
        })


def comment_edit(request, pk):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("You need to log in")
    comment = get_object_or_404(Comment, pk=pk)

    if comment.user != request.user:
        return HttpResponseNotAllowed("You are not the owner")

    comment.text = request.POST.get('comment_text')
    comment.save()

    return JsonResponse({
        'status': 'edited'
    })


@require_POST
def post_comment(request, next=None, using=None):
    data = request.POST.copy()
    post_anonymously = getattr(settings, 'MLC_POST_ANONYMOUSLY', False)

    # check if user needs to be authenticated
    if not post_anonymously:
        if not request.user.is_authenticated:
            return HttpResponseBadRequest('You need to be authenticated to post comments')

    # Look up the object we're trying to comment about
    ctype = data.get("content_type")
    object_id = data.get("object_id")

    if ctype is None or object_id is None:
        return HttpResponseBadRequest("Missing content_type or object_id field.")
    try:
        model = apps.get_model(ctype)
        target = model._default_manager.using(using).get(pk=object_id)

    except TypeError:
        return HttpResponseBadRequest(
            "Invalid content_type value: %r" % escape(ctype))
    except AttributeError:
        return HttpResponseBadRequest(
            "The given content-type %r does not resolve to a valid model." % escape(ctype))
    except ObjectDoesNotExist:
        return HttpResponseBadRequest(
            "No object matching content-type %r and object PK %r exists." % (
                escape(ctype), escape(object_id)))
    except (ValueError, ValidationError) as e:
        return HttpResponseBadRequest(
            "Attempting go get content-type %r and object PK %r exists raised %s" % (
                escape(ctype), escape(object_id), e.__class__.__name__))

    form = CommentForm(data)

    # TODO: Decide for every instance if multiple postings possible
    # check if multiple posting enabled - quick and dirty way
    s_user_mutliple_posting = getattr(settings, 'MLC_USER_ALLOW_MULTIPLE_COMMENTS', False)
    if not s_user_mutliple_posting:
        if post_anonymously and request.user.is_anonymous:
            test_obj = Comment.objects.filter(
                object_id=target.id,
                user=None,
                content_type__model=target.comments.content_type.model,
                ip_address=request.META.get('REMOTE_ADDR'))
        else:
            test_obj = Comment.objects.filter(
                object_id=target.id,
                content_type__model=target.comments.content_type.model,
                user=request.user)

        if test_obj.exists():
            return HttpResponseBadRequest(_("You already posted a comment."))

    if form.is_valid():
        comment = form.save(commit=False)
        comment.content_object = target
        comment.site_id = getattr(settings, 'SITE_ID', None)
        comment.is_active = getattr(settings, 'MLC_COMMENT_DEFAULT_ACTIVE', True)
        comment.ip_address = request.META.get('REMOTE_ADDR')
        if request.user.is_authenticated:
            comment.user = request.user
        comment.save()

        if request.is_ajax():
            return render(request, 'django_mlcommenting/comment_detail.html', context={
                'comment': comment,
                'comment_message': {
                    'value': _("Your comment was added."),
                    'type': 'success'
                }
            })

        return redirect(data.get('r', '/'))

    else:
        if request.is_ajax():
            test = str(form.errors)
            return HttpResponseBadRequest(test)

        return render(request, 'django_mlcommenting/comment_form.html', context={'form': form})


@login_required
def comment_like(request):
    if not request.is_ajax():
        return HttpResponseBadRequest("Not ajax")

    if not request.user.is_authenticated:
        return HttpResponseNotAllowed("Not logged in")

    comment_id = request.POST.get('comment_id', None)
    comment = get_object_or_404(Comment, pk=comment_id)

    comment_vote = CommentVote.objects.filter(comment=comment, user=request.user)
    if comment_vote.exists():
        comment_vote.delete()
        liked = False
    else:
        comment_vote = CommentVote(
            comment=comment,
            user=request.user
        ).save()
        liked = True

    return JsonResponse({
        'status': 'ok',
        'liked': liked,
        'likes': CommentVote.objects.filter(comment=comment).count(),
    })


def comment_detail_ajax(request):
    if not request.is_ajax():
        return HttpResponseBadRequest("not ajax")

    comment_id = request.GET.get('comment_id', None)
    comment = get_object_or_404(Comment, pk=comment_id)

    return JsonResponse({
        'status': 'ok',
        'html': render_to_string('django_mlcommenting/comment_detail.html',
                                 context={'comment': comment}, request=request)
    })


def comment_preview(request):
    return render(request, 'django_mlcommenting/comment_preview.html', context={})


def comment_load_more(request):
    if not request.is_ajax():
        return HttpResponseBadRequest("not ajax")
    s_comments_show = getattr(settings, 'MLC_COMMENTS_SHOW', 5)

    content_type_app_label = request.GET.get('ctypeapplabel', '')
    content_type_model = request.GET.get('ctypemodel', '')

    object_id = request.GET.get('oid', None)
    current_show = int(request.GET.get('s', 0))

    if not content_type_app_label or not object_id or not content_type_model:
        return HttpResponseBadRequest("Bad request. Parameter invalid")

    comments = Comment.objects.filter(
        content_type__app_label=content_type_app_label,
        content_type__model=content_type_model,
        object_id=object_id).order_by('-id')
    comments_filtered = comments[current_show:current_show + s_comments_show]

    return JsonResponse({
        'status': 'ok',
        'comments': list(comments_filtered.values_list('id', flat=True)),
        'html': render_to_string('django_mlcommenting/comment_list_ajax.html',
                                 context={
                                     'comment_list': comments_filtered,
                                     'show_more': True if comments[current_show:].count() > s_comments_show else False
                                 },
                                 request=request),
        'more': True if comments[current_show:].count() > s_comments_show else False
    })
