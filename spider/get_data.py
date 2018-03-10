from .models import AddUrlsInTable, AddMainUrls


def filter_data():
    urls = AddMainUrls.objects.all()
    data = AddUrlsInTable
    for i in urls:
        p = data.objects.filter(out=i.url).count()
        k = data.objects.filter(inn=i.url).count()
        print(i.url + " | " + str(p) + " | " + str(k))