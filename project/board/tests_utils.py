from django.test import TestCase
from django.utils import timezone

from .models import Post as postDB
from .models import Thread as threadDB
from .models import Board as boardDB
from .models import Category as categoryDB

import random
import string

random_string = lambda: ''.join(random.choices(
    string.ascii_uppercase + string.ascii_lowercase + string.digits, k=10
))

random_ip = lambda: '{}.{}.{}.{}'.format(
    random.randint(0, 255), random.randint(0, 255),
    random.randint(0, 255), random.randint(0, 255)
)

def randomDB():
    for _ in range(5):
            categoryDB.objects.create(name=random_string())
        
    for c in categoryDB.objects.all():
        for _ in range(5):
            boardDB.objects.create(
                link=random_string(),
                name=random_string(),
                category=c
            )
        
    for b in boardDB.objects.all():
        for _ in range(5):
            threadDB.objects.create(
                title=random_string(),
                updateTime=timezone.now(),
                board=b,
                postCount=0
            )
    
    for t in threadDB.objects.all():
        for _ in range(5):
            t.updateTime = timezone.now()
            t.postCount += 1
            t.save()
            postDB.objects.create(
                name=t.board.defAnon,
                text=random_string(),
                number=str(t.postCount).zfill(3),
                thread=t,
                authorID=random_string()
            )
    
    return (categoryDB, boardDB, threadDB, postDB)

class requestDummy():
    class sessionDummy():
        session_key = ''
        def save(self):
            self.session_key = random_string()
        
    def __init__(self):
        self.POST = {}
        self.GET = {}
        self.COOKIES = {
            'highlight_style': '',
            'style': '',
        }
        self.path = ''
        self.method = 'GET'
        self.META = {
            'HTTP_HOST': '127.0.0.1',
            'REMOTE_ADDR': random_ip(),
            'HTTP_X_FORWARDED_FOR': False,
            'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
        }
        self.session = self.sessionDummy()