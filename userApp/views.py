from django.shortcuts import render , redirect
from django.contrib.auth.decorators import login_required
from mainApp.models import UserDeatil , UserProfile ,PoliceStation , FIR , Evidence , ActionList
from django.contrib.auth.models import User
import datetime
import uuid
from django.utils import timezone
import math
# Create your views here.

@login_required
def uhome(request):
    return render(request,'uhome.html')

@login_required
def firformpage(request):
    obj = UserDeatil.objects.get(user = request.user)
    return render(request,'firformpage.html',{'obj':obj})

@login_required
def complaintformpage(request):
    return render(request,'complaintformpage.html')


def dob(inp):
    if inp.replace('-','').isdigit():
        return inp
    else:
        inp=inp.replace(' ',',')
        return datetime.datetime.strptime(inp, '%b,%d,,%Y').strftime('%Y-%m-%d')

@login_required
def userdetails(request):
    obj = UserDeatil.objects.get(user = request.user)
    if request.method == 'POST':
        fullname = request.POST['fullname']
        gender = request.POST['gender']
        dateofbirth = request.POST['dateofbirth']
        occupation = request.POST['occupation']
        maritialstatus = request.POST['maritialstatus']
        mobile = request.POST['mobile']
        laddress = request.POST['laddress']
        paddress = request.POST['paddress']
        dateofbirth=dob(dateofbirth)

        qobj = UserDeatil.objects.filter(user = request.user)
        qobj.update(fullname=fullname,gender=gender,dateofbirth=dateofbirth,occupation=occupation,maritialstatus=maritialstatus,mobile=mobile,laddress=laddress,paddress=paddress)
        qxobj = UserDeatil.objects.get(user = request.user)
        return render(request,'userdetails.html',{'obj':qxobj})
    return render(request,'userdetails.html',{'obj':obj})


def caldistance(l1,lo1,l2,lo2):
    R = 6373.0
    lat1 = math.radians(l1)
    lon1 = math.radians(lo1)
    lat2 = math.radians(l2)
    lon2 = math.radians(lo2)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return  R * c


def coordinates(lat,long):
    obj = PoliceStation.objects.all()
    mindist = 6373.0
    dummy = None
    for i in obj:
        if(mindist > caldistance(float(lat),float(long),float(i.latitude),float(i.longitude))):
            dummy = i
    return dummy

@login_required
def firsession(request):
    obj = ("Any further detail about subject of the allegation which you know?",'What was the date, time and duration of the incident or behavior?','Where did it happen?','What did you do in response to the incident or behavior?','What did you say in response to the incident or behavior?','How did the subject of the allegation react to your response?',"Did you tell anyone about the incident or behavior? Who? What did they say and do?","Do you know whether the subject of the allegation has been involved in any other incidents?","Do you know why the incident or behavior occurred?","Do you know anyone else who can shed light on this incident?","Is there anything else you want to tell me that I haven’t asked you?")
    cobj = FIR.objects.all()
    eobj = Evidence.objects.all()
    if request.method == 'POST':
        firid=''
        while True:
            s = str(uuid.uuid4())
            if s not in cobj:
                firid = s
                break
        content = request.POST['fstatement']
        evid=''
        while True:
            t = str(uuid.uuid4())
            if t not in eobj:
                evid = t
                break


        creationdate = timezone.now()
        submissiondate = timezone.now()
        policestation = PoliceStation.objects.get(pname = coordinates(float(request.POST['lat']),float( request.POST['long'])))
        uxobj = UserDeatil.objects.get(user = request.user)
        fobj = FIR(firid=firid,userdetailobj=uxobj,content=content,creationdate=creationdate,submissiondate=submissiondate,policestation=policestation,status='Filed')
        fobj.save()

        if request.FILES.getlist('files') != None:
            for i in request.FILES.getlist('files'):
                evidobj = Evidence(eid=evid,fid=fobj,efile=i)
                evidobj.save()
        return redirect('/userapp/userfirview/')
    return render(request,'firsession.html',{'obj':obj})


def uservalidfir(obj):
    lis = []
    for i in obj:
        if i.status != 'Deleted':
            lis.append(i)
    return lis

@login_required
def userfirview(request):
    obj = FIR.objects.filter(userdetailobj = UserDeatil.objects.get(user = request.user)).order_by('-submissiondate')
    return render(request,'userfirview.html',{'obj':uservalidfir(obj)})

@login_required
def deletefir(request,id):
    obj = FIR.objects.filter(id=id)
    obj.update(status='Deleted')
    nobj = FIR.objects.filter(userdetailobj = UserDeatil.objects.get(user = request.user)).order_by('-submissiondate')
    return render(request,'userfirview.html',{'obj':uservalidfir(nobj)})

@login_required
def uviewfir(request,id):
    obj = FIR.objects.get(id = id)
    eobj = Evidence.objects.filter(fid = obj)
    adh = UserProfile.objects.get(user = obj.userdetailobj.user)
    act = ActionList.objects.filter(fid = obj).order_by('-actdate')
    return render(request,'uviewfir.html',{'obj':obj,'adh':adh,'eobj':eobj,'act':act})
