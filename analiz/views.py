from django.http import HttpResponseRedirect
from django.shortcuts import render
from .forms import AddUrl
from django.core.urlresolvers import reverse
from spider.main import Spider
from spider.get_data import filter_data
from spider.models import AddUrlsInTable, AddMainUrls, MainTable


def home_list(request):
    q = AddMainUrls.objects.all()
    if q is not None:
        AddMainUrls.objects.all().delete()
        AddUrlsInTable.objects.all().delete()
        MainTable.objects.all().delete()

    if request.method == "POST":
        form = AddUrl(request.POST)
        if form.is_valid():
            base_url = form.cleaned_data['url']
            return HttpResponseRedirect(reverse("crawl", kwargs={"b_url": base_url}))
    else:
        form = AddUrl()
    return render(request, "analiz/home_list.html", {
        "form": form
    })


def error_list(request):
    return render(request, 'analiz/error_list.html')


def spider_list(request, b_url):

    Spider(b_url)
    rank = Spider.work()
    if isinstance(rank,str):
        return HttpResponseRedirect(reverse("error"))
    urls = AddMainUrls.objects.all()
    data = AddUrlsInTable
    brk_link = Spider.brokenLinks
    ex_link = Spider.externalLInks

    for pr, i in enumerate(urls):
        p = data.objects.filter(out=i.url).count()
        k = data.objects.filter(inn=i.url).count()
        print(i.url + " | " + str(p) + " | " + str(k))

        table = MainTable(url=i,in_count=p,out_count=k, rank=rank[pr])
        table.save()

    tbl = MainTable.objects.all()

    return render(request, 'analiz/spider_list.html',{"tbl":tbl, "brk_link": brk_link, "ex_link": ex_link})
