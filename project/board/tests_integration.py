from django.test import TestCase
from django.test import Client
from http.cookies import SimpleCookie

from .tests_utils import *

import string
import random

meta = {
    'HTTP_USER_AGENT': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0',
    'HTTP_HOST': '127.0.0.1',
    'REMOTE_ADDR': random_ip(),
    'HTTP_X_FORWARDED_FOR': False
}

class MainRequest(TestCase):
    def setUp(self):
        self.categoryDB, self.boardDB, self.threadDB, self.postDB = randomDB()
    
    def test_post_thread(self):
        c = Client()
        b = random.choice(self.boardDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
            'subject': random_string(),
        }
        response = c.post('/' + b.link + '/', data=payload, **meta)
        query = response.headers['location'].split('/')
        p = self.postDB.objects.get(number='001', thread=query[-1])
        t = self.threadDB.objects.get(id=query[-1])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(p.name, payload['name'])
        self.assertEquals(p.text, payload['text'])
        self.assertEquals(t.title, payload['subject'])
        
        payload = {
            'name': random_string() * 7,
            'text': random_string() * 1600,
            'subject': random_string() * 7,
        }
        response = c.post('/' + b.link + '/', data=payload, **meta)
        query = response.headers['location'].split('/')
        p = self.postDB.objects.get(number='001', thread=query[-1])
        t = self.threadDB.objects.get(id=query[-1])
        self.assertEquals(response.status_code, 302)
        self.assertEquals(p.name, payload['name'][:64])
        self.assertEquals(p.text, payload['text'][:15000])
        self.assertEquals(t.title, payload['subject'][:64])
    
    def test_post_post(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        query = response.headers['location'].split('/')
        p = self.postDB.objects.get(number=query[-1].split('-')[-1], thread=t.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(p.name, payload['name'])
        self.assertEquals(p.text, payload['text'])
        
        payload = {
            'name': random_string() * 7,
            'text': random_string() * 1600,
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        query = response.headers['location'].split('/')
        p = self.postDB.objects.get(number=query[-1].split('-')[-1], thread=t.id)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(p.name, payload['name'][:64])
        self.assertEquals(p.text, payload['text'][:15000])
    
    def test_board(self):
        c = Client()
        b = random.choice(self.boardDB.objects.all())
        response = c.get('/' + b.link + '/', **meta)
        self.assertEquals(response.status_code, 200)
        response = c.get('/' + random_string() * 2 + '/', **meta)
        self.assertEquals(response.status_code, 404)
    
    def test_thread(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        response = c.get('/' + t.board.link + '/thread/' + str(t.id), **meta)
        self.assertEquals(response.status_code, 200)
        response = c.get('/' + random_string() * 2 + '/thread/' + str(t.id), **meta)
        self.assertEquals(response.status_code, 404)
    
    def test_mobile(self):
        c = Client()
        old_ua = meta['HTTP_USER_AGENT']
        meta['HTTP_USER_AGENT'] = 'Mozilla/5.0 (Android; Mobile; rv:38.0) Gecko/38.0 Firefox/38.0'
        response = c.get('/', **meta)
        self.assertTrue(response.content.decode().find('_m.css'))
        meta['HTTP_USER_AGENT'] = old_ua
        response = c.get('/', **meta)
        self.assertEquals(response.content.decode().find('_m.css'), -1)
    
    def test_theme(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        response = c.get('/' + t.board.link + '/thread/' + str(t.id), **meta)
        self.assertEquals(c.cookies.get('style').value, 'atch')
        self.assertEquals(c.cookies.get('highlight_style').value, 'monokai')
    
    def test_theme_cookie(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        style = random.choice(('makaba', 'umnochan', 'burichan'))
        highlight_style = random.choice(('native', 'tango', 'manni'))
        c.cookies = SimpleCookie({
            'style': style,
            'highlight_style': highlight_style,
        })
        response = c.get('/' + t.board.link + '/thread/' + str(t.id), **meta)
        self.assertTrue(response.content.decode().find('%s.css' % style))
        self.assertTrue(response.content.decode().find('%s.css' % highlight_style))
    
    def test_ip_redirect(self):
        c = Client()
        meta['REMOTE_ADDR'] = random.choice(('188.254.110.166', '185.93.182.254'))
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        self.assertEquals(response.status_code, 302)
        self.assertEquals(response.url, 'https://www.youtube.com/watch?v=3_-GudYC22E')
        meta['REMOTE_ADDR'] = random_ip()
    
    def test_garbage_block(self):
        c = Client()
        response = c.get('/', data={random_string: random_string()}, **meta)
        self.assertEquals(response.status_code, 401)
        
    def test_tripcode_consistent(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string() + '#test',
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        trip = content.find(payload['name'].split('#')[0]) + len(payload['name'].split('#')[0])
        trip = content[trip + 1:content.find('<', trip)]
        
        payload['text'] = random_string()
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        ctrip = content.find(payload['name'].split('#')[0]) + len(payload['name'].split('#')[0])
        ctrip = content[ctrip + 1:content.find('<', ctrip)]
        self.assertEquals(trip, ctrip)
    
    def test_tripcode_different(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string() + '#test',
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        trip = content.find(payload['name'].split('#')[0])
        trip = content[trip + 1:content.find('<', trip)]
        
        payload = {
            'name': random_string() + '!' + trip,
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        ctrip = content.find(payload['name'].split('!')[0]) + len(payload['name'].split('!')[0])
        ctrip = content[ctrip + 2:content.find('<', ctrip)]
        self.assertNotEquals(trip, ctrip)
        
    def test_id_consistent(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        id = content.find('ID', content.find(payload['name']))
        id = content[id + 3:content.find('<', id)]
        
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        cid = content.find('ID', content.find(payload['name']))
        cid = content[cid + 3:content.find('<', cid)]
        
        self.assertEquals(id, cid)
        
    def test_id_different(self):
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        id = content.find('ID', content.find(payload['name']))
        id = content[id + 3:content.find('<', id)]
        
        c = Client()
        t = random.choice(self.threadDB.objects.all())
        payload = {
            'name': random_string(),
            'text': random_string(),
        }
        response = c.post('/' + t.board.link + '/thread/' + str(t.id) + '/', data=payload, **meta)
        response = c.get(response.url, **meta)
        content = response.content.decode()
        cid = content.find('ID', content.find(payload['name']))
        cid = content[cid + 3:content.find('<', cid)]
        
        self.assertNotEquals(id, cid)
