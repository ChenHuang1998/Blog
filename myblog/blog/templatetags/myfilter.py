from django import template
import markdown
register = template.Library()


@register.filter()
def mk(obj):
    obj = markdown.markdown(obj,
                              extensions=[
                                 'markdown.extensions.extra',
                                 'markdown.extensions.codehilite',
                                 'markdown.extensions.toc',
                              ])
    return obj