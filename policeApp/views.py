from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
import datetime
from mainApp.models import PoliceDetail , PoliceStation , FIR , UserDeatil , UserProfile ,Evidence , ActionList

from textblob import TextBlob
import random
from textblob import Word
import uuid
from django.utils import timezone

# Create your views here.
@login_required
def phome(request):
    return render(request,'phome.html')


def dob(inp):
    if inp.replace('-','').isdigit():
        return inp
    else:
        inp=inp.replace(' ',',')
        return datetime.datetime.strptime(inp, '%b,%d,,%Y').strftime('%Y-%m-%d')

@login_required
def policedetails(request):
    obj = PoliceDetail.objects.get(user = request.user)
    pobj = PoliceStation.objects.all()
    if request.method == 'POST':
        fullname = request.POST['fullname']
        gender = request.POST['gender']
        dateofbirth = request.POST['dateofbirth']
        post = request.POST['status']
        pstat = request.POST['pstat']
        maritialstatus = request.POST['maritialstatus']
        mobile = request.POST['mobile']
        laddress = request.POST['laddress']
        paddress = request.POST['paddress']
        dateofbirth=dob(dateofbirth)

        if(pstat == 'None' or post == 'None'):
            return render(request,'policedetails.html',{'obj':obj,'pobj':pobj})

        print(post,pstat)
        qpsobj = PoliceStation.objects.get(pname = pstat)
        qobj = PoliceDetail.objects.filter(user = request.user)
        qobj.update(fullname=fullname,gender=gender,dateofbirth=dateofbirth,post=post,pid=qpsobj,maritialstatus=maritialstatus,mobile=mobile,laddress=laddress,paddress=paddress)
        qxobj = PoliceDetail.objects.get(user = request.user)
        return render(request,'policedetails.html',{'obj':qxobj,'pobj':pobj})
    return render(request,'policedetails.html',{'obj':obj,'pobj':pobj})


def uservalidfir(obj):
    lis = []
    for i in obj:
        if i.status != 'Deleted':
            lis.append(i)
    return lis

@login_required
def policefirview(request):
    uobj = PoliceDetail.objects.get(user = request.user)
    obj = FIR.objects.filter(policestation = uobj.pid).order_by('-submissiondate')
    return render(request,'policefirview.html',{'obj':uservalidfir(obj)})


def sentimentalAnalysis(text):
    blob = TextBlob(text)
    nouns = list()
    about = list()
    for word, tag in blob.tags:
        if tag == 'NN':
            nouns.append(word.lemmatize())
    for item in random.sample(nouns, 10):
        word = Word(item)
        about.append(word.pluralize())
    return about,blob.sentiment

@login_required
def viewfir(request,id):
    nalobj = ActionList.objects.all()
    obj = FIR.objects.get(id = id)
    qobj = FIR.objects.filter(id = id)
    acid = ''
    while True:
        t = str(uuid.uuid4())
        if t not in nalobj:
            acid = t
            break
    if request.method == 'POST':
        police =PoliceDetail.objects.get(user = request.user)
        content = request.POST['action']
        qobj.update(status='last acted on {}'.format(timezone.now()))
        alobj = ActionList(actionid=acid,fid=obj,police=police,content=content,status='Acted',actdate=timezone.now())
        alobj.save()
        print('hi')
        return redirect('/policeapp/viewfir/{}/'.format(id))
    if obj.status == 'Filed':
        qobj.update(status='Seen')
    adh = UserProfile.objects.get(user = obj.userdetailobj.user)
    about,sentiment = sentimentalAnalysis(obj.content)
    eobj = Evidence.objects.filter(fid = obj)
    act = ActionList.objects.filter(fid = obj).order_by('-actdate')
    print('hello')
    return render(request,'viewfir.html',{'obj':obj,'adh':adh,'about':about,'polarity':sentiment[0],'subjectivity':sentiment[1],'zero':0,'eobj':eobj,'act':act,'id':id})
