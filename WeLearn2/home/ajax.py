from django.http import JsonResponse,HttpResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404,redirect
from django.core.exceptions import PermissionDenied
from .models import Pack,Notification,Comment,Reply
from django.contrib.auth.models import User
import json

@require_POST
@csrf_exempt
def like(request):
    pack = get_object_or_404(Pack, pk=json.loads(request.body).get('pk'))
    if request.user in pack.likes.all():
        pack.likes.remove(request.user)
        pack.save()
        if request.user != pack.author:
            notification = Notification(unliked=True,from_user=request.user,to_user=pack.author,pack=pack)
            notification.save()
        return JsonResponse({'liked':False})
    else:
        pack.likes.add(request.user)
        pack.save()
        if request.user != pack.author:
            notification = Notification(liked=True,from_user=request.user,to_user=pack.author,pack=pack)
            notification.save()
        return JsonResponse({'liked':True})

@require_POST
@csrf_exempt
def book(request):
    pack = get_object_or_404(Pack,pk=json.loads(request.body).get('pk'))
    if pack in request.user.profile.bookmarks.all():
        request.user.profile.bookmarks.remove(pack)
        request.user.save()
        return JsonResponse({'marked':False})
    else:
        request.user.profile.bookmarks.add(pack)
        request.user.save()
        return JsonResponse({'marked':True})

@require_POST
@csrf_exempt
def follow(request):
    re_user = get_object_or_404(User, pk=json.loads(request.body).get('pk'))

    if re_user.pk == request.user.pk:
        return JsonResponse({'following':'Invalid'})   

    if request.user in re_user.profile.followers.all():
        re_user.profile.followers.remove(request.user)
        re_user.save()
        notification = Notification(unfollowed=True,from_user=request.user,to_user=re_user)
        notification.save()
        return JsonResponse({'following':False})
    else:
        re_user.profile.followers.add(request.user)
        re_user.save()
        notification = Notification(followed=True,from_user=request.user,to_user=re_user)
        notification.save()
        return JsonResponse({'following':True})

@require_POST
@csrf_exempt
def remove_notif(request):
    notif = get_object_or_404(Notification,pk=json.loads(request.body).get('pk'))
    if notif.to_user != request.user:
        return JsonResponse({'removed':'Invalid'})
    notif.delete()
    return JsonResponse({'removed':True})

@require_POST
@csrf_exempt
def remove_all(request):
    request.user.to_user_set.all().delete()
    return JsonResponse({'removed':True})

@require_POST
@csrf_exempt
def comment_like(request):
    comment = get_object_or_404(Comment, pk=json.loads(request.body).get('pk'))
    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
        comment.save()
        return JsonResponse({'liked':False})
    else:
        comment.likes.add(request.user)
        comment.save()
        return JsonResponse({'liked':True})

@require_POST
@csrf_exempt
def reply_like(request):
    reply = get_object_or_404(Reply,pk=json.loads(request.body).get('pk'))
    if request.user in reply.likes.all():
        reply.likes.remove(request.user)
        reply.save()
        return JsonResponse({'liked':False})
    else:
        reply.likes.add(request.user)
        reply.save()
        return JsonResponse({'liked':True})

@require_POST
@csrf_exempt
def create_comment(request):
    data = json.loads(request.body)
    pack = get_object_or_404(Pack,pk=data.get('pack'))
    comment = Comment(pack=pack,author=request.user,content=data.get('content'))
    comment.save()
    return JsonResponse({'added':True,'pk':comment.pk})

@require_POST
@csrf_exempt
def create_reply(request):
    data = json.loads(request.body)
    comment = get_object_or_404(Comment,pk=data.get('comment'))
    reply = Reply(comment=comment,author=request.user,content=data.get('content'))
    reply.save()
    return JsonResponse({'added':True,'pk':reply.pk})

@require_POST
@csrf_exempt
def comment_edit(request):
    data = json.loads(request.body)
    comment = get_object_or_404(Comment,pk=data.get('comment'))
    if request.user.pk == comment.author.pk:
        comment.content = data.get('content')
        comment.edited = True
        comment.save()
        return JsonResponse({'added':True})
    else:
        raise PermissionDenied

@require_POST
@csrf_exempt
def reply_edit(request):
    data = json.loads(request.body)
    reply = get_object_or_404(Reply, pk=data.get('reply'))
    if request.user.pk == reply.author.pk:
        reply.content = data.get('content')
        reply.edited = True
        reply.save()
        return JsonResponse({'added':True})
    else:
        raise PermissionDenied

@require_POST
@csrf_exempt
def comment_delete(request):
    comment = get_object_or_404(Comment, pk=json.loads(request.body).get('pk'))
    if comment.author.pk == request.user.pk:
        comment.delete()
        return JsonResponse({'deleted':True})
    else:
        raise PermissionDenied

@require_POST
@csrf_exempt
def reply_delete(request):
    reply = get_object_or_404(Reply, pk=json.loads(request.body).get('pk'))
    if reply.author.pk == request.user.pk:
        reply.delete()
        return JsonResponse({'deleted':True})
    else:
        raise PermissionDenied