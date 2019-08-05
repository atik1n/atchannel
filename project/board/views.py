from django.shortcuts import get_object_or_404, render, redirect
from django.http import Http404
from .models import Post as postDB
from .models import Thread as threadDB
from .models import Board as boardDB
from .models import Category as categoryDB
from django.http import HttpResponseRedirect, HttpResponse, HttpRequest
from django.utils import timezone
from django.template import Context, loader
from .forms import postForm

from modules.atchpy.mobile import test as mobileBrowser
from modules.atchpy.parse import *
from modules.atchpy.post import *
from modules.atchpy.trip import *

import re, glob

staticDir = "/home/pi/Amadeus/"
stylesCH = [re.findall(r'(?:-)(.*?)(?:.css)', s)[0] for s in glob.glob('%s/static/board/css/ch-*.css' % staticDir)]
styles = [re.findall(r'(?:-)(.*?)(?:.css)', s)[0] for s in glob.glob('%s/static/board/css/tb-*.css' % staticDir)]

def test(request):
	s = request.session
	sKey = mktripcode(s.session_key)[:5]

	return render(request, 'test.html', locals())

def random_header():
	import random
	image = random.choice(glob.glob('%s/static/board/img/headers/*.*' % staticDir)).replace(staticDir,"")
	link = '/%s/' % image.replace('/static/board/img/headers/', '').split('-')[0]
	return (image, link)

# Create your views here.
def board(request):
	reqQuery = request.path.strip('/').split('/')
	reqThread = False

	localBoards = boardDB.objects.all()

	curBoard = parseBoard(reqQuery[0])
	if len(reqQuery) == 2:
		raise Http404

	if len(reqQuery) == 3 and reqQuery[1] == 'thread':
		curThread = parseThread(curBoard, reqQuery[2])
		reqThread = True

	if len(reqQuery) == 3 and reqQuery[1] != 'thread':
		raise Http404

	if len(reqQuery) > 3:
		raise Http404

	localThreads = threadDB.objects.filter(board=curBoard).order_by('-updateTime')
	if reqThread:
		localPosts = parseDB(postDB, curThread)[::-1]
    
	dropList = parseChan(curBoard.link)

	isMobile = mobileBrowser(request)

	if request.method == "POST":
		def get_client_ip(request):
			x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
			if x_forwarded_for:
				ip = x_forwarded_for.split(',')[0]
			else:
				ip = request.META.get('REMOTE_ADDR')
			return ip

		if curBoard.readOnly and not reqThread:
			return HttpResponse('This board is read only', status=403)
		if get_client_ip(request) in ['188.254.110.166', '185.93.182.254']:
			return redirect('https://www.youtube.com/watch?v=3_-GudYC22E')

		if request.POST.get('subject'):
			t = postThread(request, curBoard, reqQuery)
		else:
			try:
				t = postPost(request, curThread, reqQuery)
			except:
				t = postThread(request, curBoard, reqQuery, False)

		return redirect(t)

	headerPath, headerLink = random_header()
  
	styleCH = request.COOKIES.get('highlight_style')
	if styleCH not in stylesCH:
		styleCH = 'monokai'
    
	style = request.COOKIES.get('style')
	if style not in styles:
		style = 'atch'

	dropThemes = parseThemes(style, styles)
	dropCodeThemes = parseThemes(styleCH, stylesCH)
	response = render(request, "board.html", locals())
	response.set_cookie('highlight_style', styleCH)
	response.set_cookie('style', style)

	return response

def index(request):
	isMobile = mobileBrowser(request)

	if list(request.GET.items()):
		return HttpResponse('SOSI HUI BYDLO', status=401)

	localBoards = boardDB.objects.all()
	allBoards = [[],[]]
	allBoards[0].extend(localBoards[:len(localBoards)//2+len(localBoards)%2])
	allBoards[1].extend(localBoards[len(localBoards)//2+len(localBoards)%2:])

	localBoards = []
	for h in allBoards:
		tmp = []
		for b in h:
			localThreads = threadDB.objects.filter(board=b).order_by('-updateTime')
			if len(localThreads) > 10:
				localThreads = localThreads[:10]
			tmp.append([b, localThreads])
		localBoards.append(tmp)


	recentThreads = threadDB.objects.all().order_by("-updateTime")
	if len(recentThreads) > 30:
		recentThreads = recentThreads[:30]

	return render(request, 'index.html', locals())
