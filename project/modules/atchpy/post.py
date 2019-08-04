from board.models import Post as postDB
from board.models import Thread as threadDB
from django.utils import timezone
from modules.atchpy.trip import *
import re

def postThread(request, curBoard, reqQuery, subj=True):
    post = request.POST
    postText = post.get('text')
    if postText != "":
        if subj:
            postSubject = post.get('subject')
        else:
            postSubject = postText
        postName = post.get('name')

        if postName.replace(' ', '') == "" or postName.replace('[sage]', '').replace(' ', '') == "":
            postName = "%s %s" % (postName.replace(' ', ''), curBoard.defAnon)

        postName = postName.replace('!', '//')
        try:
            trip = postName[postName.index('#'):]
            postName = postName.replace(trip, '!%s' % mktripcode(trip[1:]))
        except:
            pass

        if len(postName) > 64:
            postName = postName[:64]

        if len(postText) > 15000:
            postText = postText[:15000]

        #postText = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '[ссылка]', postText)
        
        t = threadDB(title=postSubject, updateTime=timezone.now(), board=curBoard, postCount=1)
        t.save()
        if not request.session.session_key:
        	request.session.save()
        aID = mkID(request.session.session_key, t.id)[:9]
        p = postDB(name=postName, text=postText, number="001", thread=t, publishionTime=timezone.now(), authorID=aID)
        p.save()
        return 'http://icst.salieri.me/%s/thread/%s' % ('/'.join(reqQuery), t.id)

def postPost(request, curThread, reqQuery):
    post = request.POST
    postText = post.get('text')
    if postText != "":
        postName = post.get('name')
        if not request.session.session_key:
        	request.session.save()
        aID = mkID(request.session.session_key, curThread.id)[:9]

        postName = postName.replace('!', '//')
        try:
            trip = postName[postName.index('#'):]
            postName = postName.replace(trip, '!%s' % mktripcode(trip[1:]))
        except:
            pass

        if postName.replace(' ', '') == "" or postName.replace('[sage]', '').replace(' ', '') == "":
            postName = "%s %s" % (postName.replace(' ', ''), curThread.board.defAnon)

        if postName.find('[sage]') != 0:
            curThread.updateTime = timezone.now()

        if len(postName) > 64:
            postName = postName[:64]

        if len(postText) > 15000:
            postText = postText[:15000]
            
        #postText = re.sub(r'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}     /)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?«»“”‘’]))', '', postText)

        curThread.postCount += 1

        postNumber = str(curThread.postCount).zfill(3)
        if postNumber == '999':
            curThread.closed = True

        curThread.save()

        p = postDB(name=postName, text=postText, number=postNumber, thread=curThread, authorID=aID)
        p.save()
        return 'http://icst.salieri.me/%s#post-%s' % ('/'.join(reqQuery), postNumber)
