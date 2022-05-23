from django.test import TestCase

from .tests_utils import *

import string
import random

class MarkdownTestCase(TestCase):
    import markdown

    p = lambda self, s: '<p>%s</p>' % s
    ext = ['markdown.extensions.codehilite', 'markdown.extensions.fenced_code', 'markdown.extensions.nl2br', 'markdown.extensions.smarty', 'md.atchmd.atchmd']

    def check_tag(self, md, tag, prefix='', text=''):
        if not isinstance(md, tuple):
            md = (md, md)
        if not isinstance(tag, tuple):
            tag = (tag, tag)
        if not text:
            text = random_string()
        tag = list(tag)
        tag = [t.replace('{}', text) for t in tag]
        self.assertEqual(
            self.markdown.markdown("{0[0]}{1}{0[1]}".format(md, text), extensions=self.ext),
            self.p('<{0[0]}>{2}{1}</{0[1]}>'.format(tag, text, prefix))
        )
    
    def test_del(self):
        self.check_tag('~~', 'del')
    
    def test_ins(self):
        self.check_tag('__', 'ins')
    
    def test_spoil(self):
        self.check_tag('||', 'spoiler')
    
    def test_quote(self):
        self.check_tag(('>', ''), 'quote', '&gt;')
    
    def test_link(self):
        self.check_tag(
            ('>>', ''),
            ('a href="#post-{}" style="color:var(--link);"', 'a'),
            '&gt;&gt;',
            text=''.join(random.choices(string.digits, k=10))
        )
    
    def test_url(self):
        text = 'http://salieri.me/{}'.format(random_string())
        self.check_tag('', ('a href="{}" target="_blank"', 'a'), text=text)
    
    def test_mixed(self):
        all = [
            ('del', '~~', '~~', ''),
            ('ins', '__', '__', ''),
            ('spoiler', '||', '||', ''),
        ]
        random.shuffle(all)
        
        tags = []
        mds = []
        prefixes = []
        for tag in all:
            tags += [tag[0]]
            mds += [(tag[1], tag[2])]
            prefixes += [tag[3]]
            
        text = random_string()
        post = text
        for md in mds:
            post = "{0[0]}{1}{0[1]}".format(md, post)
        
        result = text
        for _, tag in enumerate(tags):
            result = '<{0}>{2}{1}</{0}>'.format(tag, result, prefixes[_])
        
        self.assertEqual(
            self.markdown.markdown(post, extensions=self.ext),
            self.p(result)
        )


class MobileTestCase(TestCase):
    uas = (
        'Mozilla/5.0 (Linux; Android 4.4.2; XMP-6250 Build/HAWK) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36 ADAPI/2.0 (UUID:9e7df0ed-2a5c-4a19-bec7-2cc54800f99d) RK3188-ADAPI/1.2.84.533 (MODEL:XMP-6250)',
        'Mozilla/5.0 (Linux; Android 7.1; Mi A1 Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.83 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; A37f Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/43.0.2357.93 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0.1; CPH1607 Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0.1; Redmi 4A Build/MMB29M; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/60.0.3112.116 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 6.0.1; zh-CN; F5121 Build/34.0.A.1.247) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.5.1.944 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; MYA-L22 Build/HUAWEIMYA-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; A1601 Build/LMY47I) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.98 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; TRT-LX2 Build/HUAWEITRT-LX2; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/59.0.3071.125 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 6.0; CAM-L21 Build/HUAWEICAM-L21; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.1.2; Redmi 4X Build/N2G47H) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1; HUAWEI CUN-L22 Build/HUAWEICUN-L22; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 5.1.1; A37fw Build/LMY47V) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.84 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.4.2; zh-CN; HUAWEI MT7-TL00 Build/HuaweiMT7-TL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/40.0.2214.89 UCBrowser/11.3.8.909 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.1.2; Redmi Note 5A Build/N2G47H; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; Redmi Note 4 Build/NRD90M) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.111 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.0; BLL-L22 Build/HUAWEIBLL-L22) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.91 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 7.1.1; CPH1723 Build/N6F26Q) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.98 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; Android 4.4.2; ASUS_T00J Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Safari/537.36',
        'Dalvik/1.6.0 (Linux; U; Android 4.0.4; opensign_x86 Build/IMM76L)',
        'Mozilla/5.0 (Android; Mobile; rv:38.0) Gecko/38.0 Firefox/38.0',
        'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SCH-I535 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SCH-I915 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
        'Dalvik/1.6.0 (Linux; U; Android 4.4.4; WT22M-FI Build/KTU84Q)',
        'Mozilla/5.0 (Linux; Android 4.4.2; en-us; SAMSUNG SCH-I545 Build/KOT49H) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SGH-T599N Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Mobile; LYF/F90M/LYF-F90M-000-02-28-130318; Android; rv:48.0) Gecko/48.0 Firefox/48.0 KAIOS/2.0',
        'Mozilla/5.0 (Linux; U; Android 2.3.5; en-in; Micromax A87 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I467 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; SCH-S738C Build/IMM76D) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.3.7; en-us; ZTE V768 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-US; B1-710 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.1 Safari/534.30',
        'Mozilla/5.0 (Linux; Android 5.0.1; SAMSUNG SCH-I545 4G Build/LRX22C) AppleWebKit/537.36 (KHTML, like Gecko) SamsungBrowser/2.1 Chrome/34.0.1847.76 Mobile Safari/537.36',
        'Mozilla/5.0 (Android; Mobile; rv:40.0) Gecko/40.0 Firefox/40.0',
        'Mozilla/5.0 (Linux; Android 4.4.4; en-us; SAMSUNG SGH-M919 Build/KTU84P) AppleWebKit/537.36 (KHTML, like Gecko) Version/1.5 Chrome/28.0.1500.94 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M830 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 2.3.5; en-us; SCH-I800 Build/GINGERBREAD) AppleWebKit/533.1 (KHTML, like Gecko) Version/4.0 Mobile Safari/533.1',
        'Mozilla/5.0 (Linux; U; Android 4.0.4; en-us; C5170 Build/IML77) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SAMSUNG-SGH-I747 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-M840 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; SPH-L710 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SAMSUNG-SGH-I497 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
        'Mozilla/5.0 (Linux; Android 4.4.2; 7040N Build/KVT49L) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.0.3; en-us; KFTT Build/IML74K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; Huawei Y301A1 Build/HuaweiY301A1) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.4.2; en-us; 0PCV1 Build/KOT49H) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; Android 4.4.2; MS5.V2 Build/MS5.V2) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/30.0.0.0 Mobile Safari/537.36',
        'Mozilla/5.0 (Linux; U; Android 4.3; en-us; SGH-T999L Build/JSS15J) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.1; en-us; EVO Build/JRO03C) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
        'Mozilla/5.0 (Linux; U; Android 4.1.2; en-us; SPH-L300 Build/JZO54K) AppleWebKit/534.30 (KHTML, like Gecko) Version/4.0 Mobile Safari/534.30',
    )
    
    def test_mobile(self):
        from modules.atchpy.mobile import test as mobileBrowser
        request = requestDummy()
        for ua in self.uas:
            request.META['HTTP_USER_AGENT'] = ua
            self.assertTrue(mobileBrowser(request))


class AtchTestCase(TestCase):
    def setUp(self):
        self.categoryDB, self.boardDB, self.threadDB, self.postDB = randomDB()
        self.themes = [random_string() for _ in range(5)]
    
    def test_enters(self):
        from modules.atchpy.parse import destroyEnters
    
        text = random_string()
        whitespace = (' ', '\n')
        post = text
        for _ in range(10):
            if random.choice((True, False)):
                post = post + random.choice(whitespace)
            else:
                post = random.choice(whitespace) + post
        
        self.assertEqual(
            destroyEnters(post),
            text
        )
    
    def test_posts(self):
        from modules.atchpy.parse import parseDB
        t = random.choice(self.threadDB.objects.all())
        result = parseDB(self.postDB, t)
        self.assertEqual(result, self.postDB.objects.filter(thread=t)[::-1])
    
    def test_thread(self):
        from modules.atchpy.parse import parseThread
        b = random.choice(self.boardDB.objects.all())
        ts = self.threadDB.objects.filter(board=b)
        t = random.choice(ts)
        result = parseThread(b, t.id)
        self.assertEqual(result, t)
    
    def test_board(self):
        from modules.atchpy.parse import parseBoard
        b = random.choice(self.boardDB.objects.all())
        self.assertEqual(parseBoard(b.link), b)
    
    def test_main(self):
        from modules.atchpy.parse import parseChan
        cb = random.choice(self.boardDB.objects.all())
        result = {c.name: 
            [[b.link, 'selected="selected"' if b.link == cb else ''] for b in self.boardDB.objects.filter(category=c)]
            for c in self.categoryDB.objects.all()
        }
        self.assertEqual(parseChan(self.boardDB), result.items())
    
    def test_themes(self):
        from modules.atchpy.parse import parseThemes
        ct = random.choice(self.themes)
        self.assertEqual(
            parseThemes(ct, self.themes),
            [[t, 'selected="selected"' if t == ct else ''] for t in self.themes]
        )
    
    def test_post_post(self):
        from modules.atchpy.post import postPost
        request = requestDummy()
        request.POST['text'] = random_string()
        request.POST['name'] = ''
        t = random.choice(self.threadDB.objects.all())
        query = [str(t.board.link), str(t.id)]
        redirect = postPost(request, t, query)
        postId = redirect.split('#')[1].replace('post-', '')
        p = self.postDB.objects.get(number=postId, thread=t)
        self.assertEqual(p.text, request.POST['text'])
    
    def test_post_thread(self):
        from modules.atchpy.post import postThread
        request = requestDummy()
        request.POST['text'] = random_string()
        request.POST['name'] = ''
        b = random.choice(self.boardDB.objects.all())
        query = [b.link,]
        redirect = postThread(request, b, query, False)
        threadId = int(redirect.split('/')[-1])
        t = self.threadDB.objects.get(id=threadId, board=b)
        p = self.postDB.objects.get(thread=t)
        self.assertEqual(p.text, request.POST['text'])
        
    def test_trip(self):
        from modules.atchpy.trip import mktripcode
        pw = random_string()
        self.assertEqual(mktripcode(pw), mktripcode(pw))
        spw = random_string()
        while spw == pw:
            spw = random_string()
        self.assertNotEqual(mktripcode(pw), mktripcode(spw))
    
    def test_userID(self):
        from modules.atchpy.trip import mkID
        sKey = random_string() + random_string() + random_string() + random_string()
        t = random.choice(self.threadDB.objects.all())
        self.assertEqual(mkID(sKey, t.id), mkID(sKey, t.id))
        ssKey = random_string() + random_string() + random_string() + random_string()
        while ssKey == sKey:
            ssKey = random_string() + random_string()
        self.assertNotEqual(mkID(sKey, t.id), mkID(ssKey, t.id))
        
    def test_view_board_bad(self):
        from django.http import Http404
        from board.views import board
        request = requestDummy()
        request.path = random_string()
        with self.assertRaises(Http404):
            board(request)
        request.path += '/' + random_string()
        with self.assertRaises(Http404):
            board(request)
        request.path += '/' + random_string()
        with self.assertRaises(Http404):
            board(request)
        request.path += '/' + random_string()
        with self.assertRaises(Http404):
            board(request)
    
    def test_view_board_threads(self):
        from django.http import Http404
        from board.views import board
        request = requestDummy()
        for b in self.boardDB.objects.all():
            request.path = b.link
            board(request)
            for t in self.threadDB.objects.filter(board=b):
                request.path = b.link + '/thread/' + str(t.id)
                board(request)
    
    def test_index(self):
        from board.views import index
        request = requestDummy()
        index(request)
        request.GET[random_string()] = random_string()
        response = index(request)
        self.assertEqual(response.status_code, 401)
