"""OnlineQuiz URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from Quiz.views import (UserModelViewsetView,QuizViewSet,RetrieveDeleteUser,UpdateUserByAdmin,
    QuestionCreateApiView,CategoryCreateApiView,TakeQuestionApiView,RetriveQuizByCategory,
                        RetrieveQuestionsByQuizId,AnswerCreateApiView,CalculateMArksApiView,
                        UserScoreForEachQuizView,UserProfileDisplayView,QuizAnalysisView,LogoutView)


router = DefaultRouter()
router.register("account/signup", UserModelViewsetView, basename="signup"),

# For creating editing deleting quiz title
router.register("quiz/create",QuizViewSet,basename="quiz-operations"),
# For Calculating marks of a quiz
router.register("quiz/calculate-marks",CalculateMArksApiView,basename="marks"),
#API for answer saving
router.register('quiz/answers',AnswerCreateApiView,basename="answer"),
# API for quiz Analysis
# router.register('quiz/analysis',QuizAnalysisView,basename="analysis"),
#API for getting profile and quizes created by user
# router.register('user/quiz-created',UserProfileDisplayView,basename='profile'),

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quiz/user/login', TokenObtainPairView.as_view()),
    path('quiz/user/token/refresh', TokenRefreshView.as_view()),
    path('quiz/user/logout', LogoutView.as_view(),name="logout"),

    # API for admin to  delete and view users
    path('quiz/user/get-delete/<int:pk>',RetrieveDeleteUser.as_view()),
    # API for admin to  update users
    path('quiz/user/edit/<int:pk>',UpdateUserByAdmin.as_view()),
    # API for user to create quiz-questions
    path('user/quiz-question/create/',QuestionCreateApiView.as_view(),name="add-questions"),
    # API for creating and listing category
    path('category/create',CategoryCreateApiView.as_view()),
    # API for listing quiz by category
    path('quiz/category/<int:id>',RetriveQuizByCategory.as_view()),
    # API for listing questions under a quiz id
    path('quiz/questions/<int:id>',RetrieveQuestionsByQuizId.as_view()),
    # API for taking quiz
    path('take/quiz/<int:id>',TakeQuestionApiView.as_view()),
    #API for getting all quiz result of a user
    path('quiz/all-result',UserScoreForEachQuizView.as_view()),
    #API for users to view questions created by them
    path('user/quiz-created',UserProfileDisplayView.as_view()),
    # API for quiz Analysis
    path('quiz/analysis',QuizAnalysisView.as_view()),
    #Front End URL
    path("web/", include("quizfntendapp.urls")),

]+router.urls
