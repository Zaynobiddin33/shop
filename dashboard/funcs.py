from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

def search(request):
    result = {}
    for k,v in request.GET.items():
        if v:
            if k == 'name':
                k = 'name__icontains'
            if k != 'page':
                result[k] = v
    return result

def page_generate(list, num, request):
    paginator = Paginator(list, num)
    page  = request.GET.get('page')
    try:
        list = paginator.page('page')
    except PageNotAnInteger:
        list = paginator.page(1)
    except EmptyPage:
        list = paginator.page(paginator.num_pages)
    return list