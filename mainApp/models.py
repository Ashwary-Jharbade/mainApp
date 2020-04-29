from django.db import models
from django.contrib.auth.models import User
from policeApp.models import PoliceStation

class UserProfile(models.Model):
	user = models.OneToOneField(User,on_delete=models.CASCADE)
	aadhar = models.CharField(max_length=12)
	usertype = models.CharField(max_length=6)
	def __str__(self):
		return self.aadhar

class UserDeatil(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	fullname = models.CharField(max_length=50)
	gender = models.CharField(max_length=10)
	dateofbirth = models.DateField()
	occupation = models.CharField(max_length=30)
	maritialstatus = models.CharField(max_length=10)
	mobile = models.CharField(max_length=10)
	laddress = models.CharField(max_length=100)
	paddress = models.CharField(max_length=100)
	def __str__(self):
		return self.mobile

class PoliceDetail(models.Model):
	user = models.ForeignKey(User,on_delete=models.CASCADE)
	fullname = models.CharField(max_length=50)
	gender = models.CharField(max_length=10)
	dateofbirth = models.DateField()
	post = models.CharField(max_length=30)
	pid = models.ForeignKey(PoliceStation,on_delete=models.CASCADE,blank=True, null=True)
	maritialstatus = models.CharField(max_length=10)
	mobile = models.CharField(max_length=10)
	laddress = models.CharField(max_length=100)
	paddress = models.CharField(max_length=100)
	def __str__(self):
		return str(self.user)

class FIR(models.Model):
	firid = models.CharField(max_length=36)
	userdetailobj = models.ForeignKey(UserDeatil,on_delete=models.CASCADE)
	content = models.CharField(max_length=1500)
	creationdate = models.DateTimeField(auto_now_add=True)
	submissiondate = models.DateTimeField(auto_now_add=False)
	policestation = models.ForeignKey(PoliceStation,on_delete=models.CASCADE,blank=True, null=True)
	status = models.CharField(max_length=30)

	def __str__(self):
		return self.firid

class Evidence(models.Model):
	eid = models.CharField(max_length=36)
	fid = models.ForeignKey(FIR,on_delete=models.CASCADE,blank=True, null=True)
	efile = models.FileField(upload_to='evidence',blank=True, null=True)

	def __str__(self):
		return self.eid

class ActionList(models.Model):
	actionid = models.CharField(max_length=36)
	fid = models.ForeignKey(FIR,on_delete=models.CASCADE)
	police = models.ForeignKey(PoliceDetail,on_delete=models.CASCADE)
	content = models.CharField(max_length=500)
	status = models.CharField(max_length=30)
	actdate = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return self.actionid

'''
class FIR(models.Model):
	fid = models.CharField(max_length=36)
	userdetailobj = models.ForeignKey(UserDeatil,on_delete=models.CASCADE)
	content = models.CharField(max_length=1500)
	creationdate = models.DateTimeField(auto_now_add=True)
	submissiondate = models.DateTimeField(auto_now_add=False)
	police = models.ForeignKey(UserDeatil,on_delete=models.CASCADE,blank=True, null=True)
	policestation = models.ForeignKey(PoliceStation,on_delete=models.CASCADE,blank=True, null=True)
	status = models.CharField(max_length=30)
'''
