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
        o = webdriver.ChromeOptions()
        o.add_argument('--headless')
        o.add_argument('--no-sandbox')
        o.add_argument('--disable-dev-shm-usage')
        c = webdriver.Chrome(chrome_options=o)
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
    
    def test_load(self):
        @TSF_Client
        def _post(c, board):
            time.sleep(random.random() * 3)
            self.TSF_find_board_index(c, board)
            self.TSF_create_thread(c)
            for _ in range(10):
                time.sleep(1 + random.random() * 3)
                while True:
                    t = 1 + random.random() * 3
                    c = 0
                    try:
                        time.sleep(t)
                        self.TSF_create_post(c)
                        break
                    except:
                        c += 1
                        if c > 5:
                            raise
                        t *= 2
        self.TSF_threading(_post, 10, board=self.random_board())
        print('Execution time:', end - start)
    
    def test_stab(self):
        @TSF_Client
        def _post(c, board):
            time.sleep(random.random() * 3)
            self.TSF_find_board_index(c, board)
            self.TSF_create_thread(c)
            for _ in range(3):
                for _ in range(10):
                    while True:
                        t = 1 + random.random() * 3
                        c = 0
                        try:
                            time.sleep(t)
                            self.TSF_create_post(c)
                            break
                        except:
                            c += 1
                            if c > 5:
                                raise
                            t *= 2
                time.sleep(10)
                for _ in range(50):
                    self.TSF_create_post(c)
        self.TSF_threading(_post, 10, board=self.random_board())
        print('Execution time:', end - start)
    
    def test_ddos(self): # God, save my CPU
        @TSF_Client
        def _post(c, board):
            time.sleep(random.random() * 3)
            self.TSF_find_board_index(c, board)
            self.TSF_create_thread(c)
            for _ in range(10):
                while True:
                    t = 1 + random.random() * 3
                    c = 0
                    try:
                        time.sleep(t)
                        self.TSF_create_post(c)
                        break
                    except:
                        c += 1
                        if c > 5:
                            raise
                        t *= 2
        self.TSF_threading(_post, 25, board=self.random_board())
        print('Execution time:', end - start)