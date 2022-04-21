from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
import threading

from .tests_utils import *

import string
import random
import time

def TSF_Client(test):
    def wrapper(*args, **kwargs):
        c = webdriver.Chrome()
        c.implicitly_wait(5)
        test(c=c, *args, **kwargs)
        c.quit()
    return wrapper

class SystemTests(StaticLiveServerTestCase):
    fixtures = [
        'board/fixtures/categories.json',
        'board/fixtures/boards.json'
    ]
    
    boards = {'b': 'Бред', 'math': 'Математика', 'sci': 'Наука', 'anime': 'Японская анимация'}
    random_board = lambda self: random.choice(list(self.boards.values()))
    styles = ('makaba', 'umnochan', 'burichan')
    highlight_styles = ('native', 'tango', 'manni')
    exceptions = []
    selenium = None
        
    def TSF_Exceptions(self, args):
        self.exceptions += [args]
        
    def TSF_find_board_index(self, c, board_name=None):
        board_name = self.random_board() if board_name is None else board_name
        c.get(self.live_server_url)
        boards = c.find_elements_by_class_name('other-header')
        for board in boards:
            if board.text == board_name:
                board.click()
                break
        c.implicitly_wait(5)
        
    def TSF_create_thread(self, c, subject=None, text=None):
        c.find_element_by_id('new-top').click()
        subjectInput = c.find_element_by_id('subject')
        subjectInput.send_keys(random_string() if subject is None else subject)
        nameInput = c.find_element_by_id('name-top')
        nameInput.send_keys(random_string())
        textInput = c.find_element_by_id('text-top')
        postText = random_string() if text is None else text
        textInput.send_keys(postText)
        c.find_element_by_id('post-top').click()
        c.implicitly_wait(5)
        self.assertTrue(c.page_source.find(postText))
    
    def TSF_create_post(self, c, text=None, pos=None):
        pos = random.choice(('top', 'bottom')) if pos is None else pos
        c.find_element_by_id('new-' + pos).click()
        nameInput = c.find_element_by_id('name-' + pos)
        nameInput.send_keys(random_string())
        textInput = c.find_element_by_id('text-' + pos)
        postText = random_string() if text is None else text
        textInput.send_keys(postText)
        c.find_element_by_id('post-' + pos).click()
        c.implicitly_wait(5)
        self.assertTrue(c.page_source.find(postText))
    
    def TSF_change_theme(self, c, theme=None, type='theme'):
        if not theme:
            if type == 'theme':
                theme = random.choice(self.styles)
            elif type == 'code_theme':
                theme = random.choice(self.highlight_styles)
            else:
                raise "Type can be either theme or code_theme"
        dropdown = Select(c.find_element_by_id(type))
        dropdown.select_by_visible_text(theme)
        c.implicitly_wait(5)
        self.assertTrue(c.page_source.find(theme + '.css'))
    
    def TSF_navigate_board(self, c, board=None):
        board = self.random_board() if board is None else board
        navigation = c.find_elements_by_id('nav-board')
        for nav in navigation:
            if nav.text == board:
                nav.click()
                break
        c.implicitly_wait(5)
    
    def TSF_navigate_thread(self, c):
        threads = c.find_elements_by_id('thread')
        thread = random.choice(threads)
        thread.click()
        c.implicitly_wait(5)
    
    def TSF_navigate_banner(self, c):
        banner = c.find_element_by_class_name('headerImg')
        banner.click()
        c.implicitly_wait(5)
        
    def TSF_threading(self, func, n, *args, **kwargs):
        self.exceptions = []
        threading.excepthook = self.TSF_Exceptions
        threads = []
        for _ in range(n):
            threads += [threading.Thread(target=func, args=args, kwargs=kwargs)]
        for thread in threads:
            thread.start()
        start = time.time()
        for thread in threads:
            thread.join()
        end = time.time()
        for e in self.exceptions:
            print(e)
        self.assertFalse(self.exceptions)
        return (start, end)
    
    @TSF_Client
    def test_create_thread(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
    
    @TSF_Client
    def test_create_post(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_create_post(c)
    
    @TSF_Client
    def test_create_post_link(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_create_post(c)
        self.TSF_create_post(c, '>>1\n' + random_string())
        self.assertTrue(c.page_source.find('/1'))
        self.assertTrue(c.page_source.find('color:var(--link);'))
    
    @TSF_Client
    def test_create_post_quote(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_create_post(c)
        self.TSF_create_post(c, '>' + random_string())
        self.assertTrue(c.page_source.find('<quote>'))
    
    @TSF_Client
    def test_create_post_md(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_create_post(c)
        self.TSF_create_post(c, '~~__||' + random_string() + '||__~~')
        self.assertTrue(c.page_source.find('<del><ins><spoiler>'))
        
    @TSF_Client
    def test_sync_post_fields(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        c.find_element_by_id('new-top').click()
        c.find_element_by_id('new-bottom').click()
        textTop = c.find_element_by_id('text-top')
        textBottom = c.find_element_by_id('text-bottom')
        textTop.send_keys(random_string())
        time.sleep(1)
        self.assertEquals(textTop.get_attribute("value"), textBottom.get_attribute("value"))
        textBottom.send_keys(random_string())
        time.sleep(1)
        self.assertEquals(textTop.get_attribute("value"), textBottom.get_attribute("value"))
    
    @TSF_Client
    def test_index_render(self, c):
        template = '<a href="{}" class="other-header">{}</a>'
        c.get(self.live_server_url)
        for key, value in self.boards.items():
            self.assertTrue(c.page_source.find(template.format(key, value)))
    
    @TSF_Client
    def test_board_render(self, c):
        b = self.random_board()
        threads = []
        for _ in range(5):
            self.TSF_find_board_index(c, b)
            threads += [random_string()]
            self.TSF_create_thread(c, subject=threads[-1])
        self.TSF_find_board_index(c, b)
        template = '<p class="text">{}(1)</p>'
        for thread in threads:
            self.assertTrue(c.page_source.find(template.format(thread)))
        
    @TSF_Client
    def test_thread_render(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        posts = []
        for _ in range(5):
            posts += [random_string()]
            self.TSF_create_post(c, text=posts[-1])
        self.assertEquals(len(c.find_elements_by_class_name('post')), len(posts) + 1)
        template = '<div class="postText"><p>{}</p></div>'
        for post in posts:
            self.assertTrue(c.page_source.find(template.format(post)))
    
    @TSF_Client
    def test_change_theme(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_change_theme(c, type='theme')
    
    @TSF_Client
    def test_change_code_theme(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_change_theme(c, type='code_theme')
    
    @TSF_Client
    def test_bump_all_boards(self, c):
        for board in list(self.boards.values()):
            self.TSF_find_board_index(c, board)
            self.TSF_create_thread(c)
            for _ in range(5):
                self.TSF_create_post(c)
            self.assertEquals(len(c.find_elements_by_class_name('post')), 6)
    
    @TSF_Client
    def test_boards_navigation(self, c):
        self.TSF_find_board_index(c)
        for board in list(self.boards.values()):
            self.TSF_navigate_board(c, board)
    
    @TSF_Client
    def test_banner(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        self.TSF_navigate_banner(c)
    
    @TSF_Client
    def test_random_navigation(self, c):
        loc = 0
        for _ in range(20):
            if loc == 0:
                self.TSF_find_board_index(c)
                loc == 1
            elif loc == 1:
                i = random.int(1, 10)
                if i < 3:
                    nav = c.find_element_by_id('nav-main')
                    nav.click()
                    loc == 0
                elif i < 7:
                    i = random.int(1, 10)
                    if i < 6:
                        self.TSF_navigate_board(c)
                    else:
                        self.TSF_navigate_banner(c)
                else:
                    self.TSF_navigate_thread(c)
                    loc == 2
            elif loc == 2:
                i = random.int(1, 10)
                if i < 6:
                    nav = c.find_element_by_id('nav-main')
                    nav.click()
                    loc == 0
                else:
                    i = random.int(1, 10)
                    if i < 6:
                        self.TSF_navigate_board(c)
                    else:
                        self.TSF_navigate_banner(c)
                    loc == 1
    
    @TSF_Client
    def test_volume_posts(self, c):
        self.TSF_find_board_index(c)
        self.TSF_create_thread(c)
        max_time = 0
        for _ in range(50):
            start = time.time()
            self.TSF_create_post(c, pos='top')
            end = time.time()
            if end - start > max_time:
                max_time = end - start
        print('Maximum load time:', max_time)
    
    @TSF_Client
    def test_volume_threads(self, c):
        max_time = 0
        board = self.random_board()
        for _ in range(50):
            start = time.time()
            self.TSF_find_board_index(c, board)
            self.TSF_create_thread(c)
            end = time.time()
            if end - start > max_time:
                max_time = end - start
        print('Maximum load time:', max_time)
    