from django.shortcuts import redirect,render
from django.contrib.contenttypes.models import ContentType
from django.utils import timezone
from django.core.cache import cache
from read_statistics.utils import *
from blog.models import Blog


def get_7_days_hot_blogs():
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects.filter(read_details__date__lt=today, read_details__date__gte=date)\
                        .values('id', 'title')\
                        .annotate(read_num_sum=Sum('read_details__read_num'))\
                        .order_by('-read_num_sum')
    return blogs[:7]


def index(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    today_hot_data = get_today_hot_data(blog_content_type)
    yesterday_hot_data = get_yesterday_hot_data(blog_content_type)
    # 获取7天热门数据的缓存
    seven_hot_data = cache.get('seven_hot_data')
    if seven_hot_data is None:
        seven_hot_data = get_7_days_hot_blogs()
        cache.set('seven_hot_data', seven_hot_data, 3600)
    return render(request, 'index.html', locals())


