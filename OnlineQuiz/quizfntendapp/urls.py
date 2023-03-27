from quizfntendapp import views
from django.urls import path

urlpatterns = [
    path("signup", views.SignUpView.as_view(), name="register"),
    path("login", views.LoginView.as_view(), name="signin"),
    path("home", views.IndexView.as_view(), name="index"),
    path("list-categories", views.ListCategoryView.as_view(), name="list-category"),
    path("quiz-list/<int:id>", views.QuizListView.as_view(), name="quiz-list"),
    path('question-list/<int:id>',views.QuestionListView.as_view(),name="question-list"),
    path('calculate-marks',views.calculate_marks_view,name="calculate-marks"),
    path("signout", views.SignOutView.as_view(), name="signout"),

]