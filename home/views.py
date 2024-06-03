import os
from django.shortcuts import render,redirect
from django.template.loader import render_to_string
from django.http import HttpResponse, JsonResponse
from django.db import transaction
from django.db.models import Avg,Sum,Count
from django.conf import settings

from .models import *

from haikunator import Haikunator
import datetime
import string
import random
import time

# Create your views here.


class UserInfo:
    def __init__(self, request):
        self.request = request
        if 'account' in request.POST.keys():
            self.account = request.POST['account']
        if 'password' in request.POST.keys():
            self.password = request.POST['password']
        if 'useremail' in request.POST.keys():
            self.useremail = request.POST['useremail']
        if 'usergender' in request.POST.keys():
            self.gender = request.POST['usergender']
        if 'userbirth' in request.POST.keys():
            self.userbirth = request.POST['userbirth']
        if 'userCareer' in request.POST.keys():
            self.career = request.POST['userCareer']
        if 'userResident' in request.POST.keys():
            self.resident = request.POST['userResident']

    def user_auth_info(self):
        memberid_login = Members.objects.filter(account=self.account,password=self.password).values('id')
        return self.account, self.password, memberid_login

    def user_not_auth_info(self):
        return self.useremail, self.gender, self.userbirth, self.career, self.resident

    def user_auth_info_create(self):
        memberid_auth = Members.objects.filter(account=self.account).values('id')
        return self.account, self.password, memberid_auth

    def user_update(self, memberid):
        member = Members.objects.get(id=memberid)
        member.useremail = self.useremail
        member.gender = self.gender
        member.userbirth = self.userbirth
        member.career = self.career
        member.resident = self.resident
        member.save()

    def user_login(self, memberid_login):
        self.request.session['user'] = memberid_login[0]
        self.request.session.set_expiry(3600)


def create(request):
    if 'user' in request.session:
        return HttpResponse("<script>location.href='/storymap';</script>")
    else:
        if request.method == 'POST':
            account, password, memberid_auth = UserInfo(request).user_auth_info_create()
            useremail, gender, userbirth, career, resident = UserInfo(request).user_not_auth_info()
            if memberid_auth:
                return HttpResponse("<script>alert('帳號已有人使用');location.href='/create';</script>")
            Members.objects.create(account=account, password=password, useremail=useremail, gender=gender, userbirth=userbirth, career=career, resident=resident)
            memberid_login = Members.objects.filter(account=account,password=password).values('id')
            if memberid_login:
                UserInfo(request).user_login(memberid_login)
                return HttpResponse("<script>alert('已完成註冊');location.href='/storymap';</script>")
        return render(request,'create.html',locals())


def update(request):
    if 'user' in request.session:
        if request.method == 'POST':
            memberid = request.session['user']['id']
            useremail, gender, userbirth, career, resident = UserInfo(request).user_not_auth_info()
            UserInfo(request).user_update(memberid)
            return HttpResponse("<script>alert('資料已更新');location.href='/storymap';</script>")
        member = Members.objects.get(id=request.session['user']['id'])
        return render(request,'update.html',locals())
    else:
        return HttpResponse("<script>location.href='/';</script>")


def login(request):
    if 'user' in request.session:
        return HttpResponse("<script>location.href='/storymap';</script>")
    else:
        if request.method == "POST":
            account, password, memberid_login = UserInfo(request).user_auth_info()
            if memberid_login:
                UserInfo(request).user_login(memberid_login)
                return HttpResponse("<script>alert('登入成功');location.href='/storymap';</script>")
            else:
                return HttpResponse("<script>alert('登入失敗，密碼錯誤！');location.href='/';</script>")
        return render(request,'login.html',locals())


def logout(request):
    if 'user' in request.session:
        request.session.clear()
        return HttpResponse("<script>alert('登出');location.href='/';</script>")
    else:
        return HttpResponse("<script>location.href='/';</script>")


def storymap(request):
    if 'user' in request.session:
        return render(request,'storymap.html',locals())
    else:
        return HttpResponse("<script>location.href='/';</script>")


def checkname(request,name):
    result = Members.objects.filter(account=name)
    if result :
        message = "帳號已註冊"
    else:
        message = "帳號可使用"
    return HttpResponse(message)


def survey(request):
    if 'user' in request.session:
        member = Members.objects.get(id=request.session['user']['id'])
        account = member.account
        if Survey_Outcome.objects.filter(id=member.id).values('id'):
            return HttpResponse("<script>alert('您已填過問卷囉～謝謝！');location.href='/storymap';</script>")
        else:
            if request.method == 'POST':
                Question1 = request.POST["Q1"]
                Question2 = request.POST["Q2"]
                Question3 = request.POST["Q3"]
                Question4 = request.POST["Q4"]
                Question5 = request.POST["Q5"]
                Question6 = request.POST["Q6"]
                Question7 = request.POST["Q7"]
                Survey_Outcome.objects.create(id=member.id,account=account,Question1=Question1,Question2=Question2,Question3=Question3,Question4=Question4,Question5=Question5,Question6=Question6,Question7=Question7)        
                return HttpResponse("<script>alert('問卷已送出');location.href='/storymap';</script>")
            return render(request,'survey.html',locals())
    else:
        return HttpResponse("<script>location.href='/';</script>")

def userpattern_count():
    numGender = ''
    Gender_Selections = ['男性', '女性']
    for index, gender in enumerate(Gender_Selections):
        if index == 0:
            numGender = str(Members.objects.filter(gender=gender).aggregate(Count("gender"))["gender__count"])
        else:
            numGender = numGender + ',{}'.format(str(Members.objects.filter(gender=gender).aggregate(Count("gender"))["gender__count"]))

    numCareer = ''
    Career_Selections = ['金融業', '製造業', '軍公教', '電子科技業', '傳統產業', '服務業', '媒體行銷公關', '法律顧問', '自營商', '自由業(SOHO)', '學生', '其他']
    numCTotal = Members.objects.all().aggregate(Count("career"))["career__count"]
    for index, career in enumerate(Career_Selections):
        numC = Members.objects.filter(career=career).aggregate(Count("career"))["career__count"]
        if index == 0:
            numCareer = '{},{},{}'.format(str(numC), career, str(format(int(numC)/int(numCTotal),  '.0%')))
        else:
            numCareer = numCareer + ',{},{},{}'.format(str(numC), career, str(format(int(numC)/int(numCTotal),  '.0%')))

    return numGender, numCareer

def userpattern(request):
    if 'user' in request.session:
        numGender, numCareer = userpattern_count()
        return render(request,'userpattern.html',locals())
    else:
        return HttpResponse("<script>location.href='/';</script>")
