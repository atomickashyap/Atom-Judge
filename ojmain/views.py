from django.shortcuts import render
from django.template import loader
from django.http import HttpResponse
from django.views import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from glob import glob
import subprocess
import sys
from .models import UserProfile, Problems, Verdicts,Submissions,TestCases



class login_view(View):
    def get(self, request):
        return render(request, 'ojmain/login.html')
    def post(self, request):
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is not None:
            login(request, user)
            return redirect('/ojmain/problems')
        else:
            return HttpResponse("invalid user")

class register(View):
    def get(self, request):
        return render(request, 'ojmain/register.html')
    def post(self, request):
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user is None:
            newuser = User.objects.create_user(username = request.POST['username'], password = request.POST['password'], email = request.POST['email'])   
            # print(request.POST['username'])
            newuserprofile = UserProfile(user = newuser)
            newuser.save()
            newuserprofile.save()
            messages.success(request,"User Added Successfully")
            # return HttpResponse("registered successfully")
            return redirect('/ojmain/')

        else:
            # return HttpResponse("User already present!")
            messages.error(request,"User already persent")
            # return HttpResponse("registered successfully")
            return redirect('/ojmain/register')

@login_required(login_url = '/ojmain/')
def problems(request):
    _Problems = Problems.objects.all()
    # An empty dictionary
    dux = {}
    # print(request.user.username)
    for x in _Problems:
        #send either the object itself or the primary key of the referenced model when using get with foreignkey
        is_present = Verdicts.objects.filter(pcode = x, user_id = UserProfile.objects.get(user__username = request.user.username)).exists()

        if is_present:
            curuser = Verdicts.objects.get(pcode = x, user_id = UserProfile.objects.get(user__username = request.user.username))
            dux.update({x.pcode : [x.pname, x.difficulty, curuser.solved_status]})
        else:
            newuser = UserProfile.objects.get(user__username = request.user.username)
            _newuser = Verdicts(pcode = x, user_id = newuser, solved_status = "no")
            _newuser.save()
            dux.update({x.pcode : [x.pname, x.difficulty, "no"]})
        
    # print(dux[1])
    context = {'context' : dux}
    # return HttpResponse("You're looking at problems list.")
    return render(request, 'ojmain/problems.html', context)


# @login_required(login_url = '/ojmain/')
# def to_problems(request, p_no):
#     curproblem = Problems.objects.filter(pcode = p_no).values().first()
#     dux = Problems.objects.get(pcode = p_no)
#     return render(request, 'ojmain/problem_statement.html', {'question': dux})


class to_problems(LoginRequiredMixin, View):
    login_url = '/ojmain/'
    def get(self, request, p_no):
        curproblem = Problems.objects.filter(pcode = p_no).values().first()
        dux = Problems.objects.get(pcode = p_no)
        print(dux.pcode)
        return render(request, 'ojmain/problem_statement.html', {'question': dux})
    def post(self, request, p_no):
        test_object = TestCases.objects.get(pcode = p_no)
        problem_sol = request.POST['problem_sol']
        cpp_lang = open("C:/Users/Atomi/OneDrive/Full_Stack_Learning/Main_OJ/OJUDGE/media/code.cpp","w+")
        cpp_lang.write(problem_sol)
        cpp_lang.close()

        ##Might comment the below lines from 83 to 89 later
        with open("C:/Users/Atomi/OneDrive/Full_Stack_Learning/Main_OJ/OJUDGE/media/code.cpp", 'r') as file :
            filedata = file.read()
        # Replace the target string
        filedata = filedata.replace('\n\n', '\n')
        # Write the file out again
        with open("C:/Users/Atomi/OneDrive/Full_Stack_Learning/Main_OJ/OJUDGE/media/code.cpp", 'w') as file:
            file.write(filedata)

        process = subprocess.run('g++ C:/Users/Atomi/OneDrive/Full_Stack_Learning/Main_OJ/OJUDGE/media/code.cpp -o otx' , shell=True, capture_output=True, text=True)
        # procesd = subprocess.run("otx < C:/Users/Atomi/OneDrive/Full_Stack_Learning/Main_OJ/OJUDGE/media/input.txt", shell=True, capture_output=True, text=True)
        procesd = subprocess.run(['otx', '<',  test_object.imp], shell=True, capture_output=True, text=True)

        _user_id = UserProfile.objects.get(user__email = request.user.email)
        _status = Verdicts.objects.get(pcode_id= p_no, user_id = _user_id)


        if procesd.stdout.strip() == open(test_object.out).read():
            if (_status.solved_status != "AC"):
                _status.solved_status = "AC"
                _status.save()
            print('Success')
            Submissions(pcode_id = p_no, user_id = _user_id, vrt = "AC").save()
        else:
            if (_status.solved_status != "AC" and _status.solved_status != "WA"):
                _status.solved_status = "WA"
                _status.save()
            print('Fail')
            Submissions(pcode_id = p_no, user_id = _user_id, vrt = "WA").save()
        return redirect('/ojmain/submissions')

def submissions_view(request):
    dux = Submissions.objects.all()
    tux = Problems.objects.all()
    print(dux)
    print(tux)
    return render(request, 'ojmain/submissions.html', {'question': dux})


@login_required(login_url = '/ojmain/')
def logout_view(request):
    logout(request)
    print("logging out")
    return redirect('/ojmain/')