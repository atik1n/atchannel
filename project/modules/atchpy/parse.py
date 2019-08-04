from board.models import Post as postDB
from board.models import Thread as threadDB
from board.models import Board as boardDB
from board.models import Category as categoryDB
from django.http import Http404
import cgi
import markdown
import md

def destroyEnters(text):
    done = False
    while not done:
        i = 0
        if text[0] == " ":
            text = text[1:]
        else:
            i += 1
        if text[0:2] == "\n":
            text = text[2:]
        else:
            i += 1
        if text[-2:] == "\n":
            text = text[:-2]
        else:
            i += 1
        if text[-1:] == " ":
            text = text[:-1]
        else:
            i += 1
        if i == 4:
            done = True
    return text

def parseDB(db, parent):
	posts = db.objects.filter(thread=parent)[::-1]

	for post in posts:
		if post.name.find('[sage]') == 0:
			post.name = '<p class="name-sage">%s</p>' % post.name
		else:
			post.name = '<p class="name">%s</p>' % post.name
    
		post.text = markdown.markdown(post.text, extensions=['markdown.extensions.codehilite', 'markdown.extensions.fenced_code', 'markdown.extensions.nl2br', 'markdown.extensions.smarty', 'md.atchmd.atchmd'])
		#int('cakscnaska')
	return posts

def parseBoard(boardLink):
	try:
		b = boardDB.objects.get(link=boardLink)
	except boardDB.DoesNotExist:
		raise Http404

	return b

def parseThread(boardLink, threadNumber):
	try:
		t = threadDB.objects.get(id=threadNumber, board__link = boardLink)
	except threadDB.DoesNotExist:
		raise Http404

	return t

def parseChan(curBoard):
	result = {}
	c = categoryDB.objects.all()
	for cat in c:
		tmp = []
		b = boardDB.objects.filter(category=cat)
		for board in b:
			tmp.append([board.link, board.link == curBoard and 'selected="selected"' or ''])
		result[cat.name] = tmp

	return result.items()
