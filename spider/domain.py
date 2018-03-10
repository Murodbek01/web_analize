# Получение домена
from urllib.parse import urlparse
import re

# Get domain name (example.com)
def get_domain_name(url):
    try:
        results = get_sub_domain_name(url).split('.')
        return results[-2] + '.' + results[-1]
    except:
        return ''


# Get sub domain name (name.example.com)
def get_sub_domain_name(url):
    try:
        return urlparse(url).netloc
    except:
        return ''


def internal_links(url):
    if url.find("#") != -1:
        k = 0
    elif url.find(".jpg") != -1:
        k = 0
    elif url.find(".jpeg") != -1:
        k = 0
    elif url.find(".img") != -1:
        k = 0
    elif url.find(".png") != -1:
        k = 0
    elif url.find("?go=") != -1:
        k = 0
    else:
        k = 1
    if k == 1:
        return True
    else:
        return False

