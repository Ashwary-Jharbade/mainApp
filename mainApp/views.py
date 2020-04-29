from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

from .models import UserProfile , UserDeatil , PoliceDetail
from django.contrib.auth.models import User

def signin(request):
    if request.method == 'POST':
        username = request.POST['usernm']
        password = request.POST['passwd']
        selecteduser = authenticate(username = username,password = password)
        if selecteduser:
            if selecteduser.is_active:
                login(request,selecteduser)
                udata = UserProfile.objects.get(user__username=request.user)
                if udata.usertype == 'Police':
                    return redirect('/policeapp/home/')
                else:
                    return redirect('/userapp/home/')
            else:
                return HttpResponse("<h1>User deactivated</h1>")
        else:
            return render(request,'signin.html',{'filler':'Alert : Email or Password does not match try again'})
    else:
        return render(request,'signin.html')

def signup(request):
    if request.method == 'POST':
        aadhar = request.POST['aadhar']
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST['usertype']

        uobj = User(username=username)
        uobj.save()
        uobj.set_password(password)
        uobj.save()
        upobj = UserProfile(user=uobj,aadhar=aadhar,usertype=usertype)
        upobj.save()
        uxobj = User.objects.get(username = username)
        udobj = UserDeatil(user=uxobj,fullname='',gender='',dateofbirth='0001-01-01',occupation='',maritialstatus='',mobile='',laddress='',paddress='')
        udobj.save()
    return render(request,'signup.html')

def psignup(request):
    if request.method == 'POST':
        aadhar = request.POST['aadhar']
        username = request.POST['username']
        password = request.POST['password']
        usertype = request.POST['usertype']

        uobj = User(username=username)
        uobj.save()
        uobj.set_password(password)
        uobj.save()
        upobj = UserProfile(user=uobj,aadhar=aadhar,usertype=usertype)
        upobj.save()
        pxobj = User.objects.get(username = username)
        pdobj = PoliceDetail(user=pxobj,fullname='',gender='',dateofbirth='0001-01-01',post='',pid=None,maritialstatus='',mobile='',laddress='',paddress='')
        pdobj.save()
    return render(request,'psignup.html')

def terms(request):
    return render(request,'terms.html')

def test(request):
    return render(request,'test.html')

def quickcomplaint(request):
    return render(request,'quickcomplaint.html')

@login_required
def signout(request):
    logout(request)
    return redirect('/')
