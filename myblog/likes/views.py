from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from likes.models import *
# Create your views here.


def errorResponse(code, message):
    data = {}
    data['status'] = 'error'
    data['code'] = code
    data['message'] = message
    return JsonResponse(data)

def successResponse(like_num):
    data = {}
    data['status'] = 'success'
    data['like_num'] = like_num
    return JsonResponse(data)


def like_change(request):
    user = request.user
    if not user.is_authenticated:
        return errorResponse(400, '你没有登录')

    content_type = request.GET.get('content_type')
    object_id = request.GET.get('object_id')

    try:
        content_type = ContentType.objects.get(model=content_type)
        model_class = content_type.model_class()
        model_obj = model_class.objects.get(pk=object_id)
    except ObjectDoesNotExist:
        return errorResponse(401,'对象不存在')
    is_like = request.GET.get('is_like')

    if is_like == 'true':
        # 点赞
        like_record, created = LikeRecord.objects.get_or_create(content_type=content_type, object_id=object_id, user=user)
        # 第一次点赞
        if created:
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)
            like_count.like_num += 1
            like_count.save()
            return successResponse(like_count.like_num)
        else:
            # 已点赞过 不能重复点赞
            return errorResponse(402, '已经点赞过')

    else:
        # 取消点赞
        if LikeRecord.objects.filter(content_type=content_type, object_id=object_id, user=user).exists():
            # 有点赞过 取消
            like_record = LikeRecord.objects.get(content_type=content_type, object_id=object_id, user=user)
            like_record.delete()
            like_count, created = LikeCount.objects.get_or_create(content_type=content_type, object_id=object_id)

            if not created:
                like_count.like_num -= 1
                like_count.save()
                return successResponse(like_count.like_num)
            else:
                return errorResponse(404, 'data error')
        else:
            # 没有点赞过 不能取消
            return errorResponse(403, '没有点赞过不能取消')
