from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,DetailView,ListView,UpdateView,FormView
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from quizfntendapp import forms
from django.http import HttpResponseRedirect
from rest_framework.views import APIView
from Quiz.models import *
# Create your views here.

class SignUpView(View):
    def get(self,request,*args,**kwargs):
        form=forms.RegistrationForm()
        return render(request,"registration.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.RegistrationForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            messages.success(self.request, "User added successfully.")
            return redirect("signin")
        else:
            return render(request,"registration.html",{"form":form})

class LoginView(View):
    def get(self,request,*args,**kwargs):
        form=forms.LoginForm()
        return render(request,"login.html",{"form":form})

    def post(self,request,*args,**kwargs):
        form=forms.LoginForm(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            print(uname,pwd)
            user=authenticate(request,username=uname,password=pwd)
            if user:
                login(request,user)
                messages.success(request,"You are In..")
                return redirect("index")
            else:
                messages.error(request,"Invalid Username or Password.")
                return render(request, "login.html",{"form":form})

class IndexView(TemplateView):
    template_name = "home.html"

class SignOutView(View):
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect("signin")

class ListCategoryView(ListView):
    model = Category
    context_object_name = "cat"
    template_name = "list-categories.html"
class QuizListView(ListView):
    model = Quiz
    context_object_name = "quiz"
    template_name = "quiz-list.html"
    def get_queryset(self):
        # return Carts.objects.filter(user=self.request.user).exclude(status="cancelled")
        id=self.kwargs['id']
        return Quiz.objects.filter(category_id=id)

class QuestionListView(ListView):
    model = Questions
    context_object_name = "question"
    template_name = "view-questions.html"
    def get_queryset(self):
        id=self.kwargs['id']
        print(id)
        return Questions.objects.filter(quiz_id=id)

# class CaluculateMarks(View):
#     def post(self,request,*args,**kwargs):
#         if request.COOKIES.get('quiz_id') is not None:
#             quiz_id = request.COOKIES.get('quiz_id')
#             qs = Quiz.objects.get(id=quiz_id)
#
#             total_marks = 0
#             questions = Questions.objects.all().filter(quiz=qs)
#             for i in range(len(questions)):
#
#                 selected_ans = request.COOKIES.get(str(i + 1))
#                 actual_answer = questions[i].correct_answer
#                 if selected_ans == actual_answer:
#                     total_marks = total_marks + questions[i].marks
#             user = User.objects.get(user_id=request.user.id)
#             result = Result()
#             result.marks = total_marks
#             result.quiz = qs
#             result.user = user
#             result.save()
#
#             return redirect('index')

def calculate_marks_view(request):
    if request.COOKIES.get('quiz_id') is not None:
        quiz_id = request.COOKIES.get('quiz_id')
        qs = Quiz.objects.get(id=quiz_id)

        total_marks = 0
        questions = Questions.objects.all().filter(quiz=qs)
        for i in range(len(questions)):

            selected_ans = request.COOKIES.get(str(i + 1))
            actual_answer = questions[i].correct_answer
            if selected_ans == actual_answer:
                total_marks = total_marks + questions[i].marks
        user = User.objects.get(user_id=request.user.id)
        result = Result()
        result.marks = total_marks
        result.quiz = qs
        result.user = user
        result.save()

        return HttpResponseRedirect('index')




