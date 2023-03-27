from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet,ViewSet
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from .models import User,Quiz,Questions,Category,Result,UserQuizAnswer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import authentication,permissions,status
from .serializer import (UserSerializer,QuizSerializer,QuestionSerializer,CategorySerializer,
                         QuizTakeSerializer,QuizByCategorySerializer,QuestionsByQuizId,AnswerSerializer,
                         MarksSerializer,UserScoreForEachQuizSerializer,UserProfileDisplaySerializer,
                         QuizByUSerSerializer,QuizAnalysisSerializer)
from django.contrib.auth import authenticate,login,logout

from rest_framework.views import APIView
from rest_framework import  generics
from .permissions import IsAdmin
from rest_framework.filters import SearchFilter

# Create your views here.
class QuizViewSet(ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        serializer = QuizSerializer(data=request.data, context={"user": user})
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data)
        else:
            return Response(data=serializer.errors)


class UserModelViewsetView(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()



class RetrieveDeleteUser(generics.RetrieveDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer

class UpdateUserByAdmin(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    permission_classes = (IsAdmin,)
    serializer_class = UserSerializer

class CategoryCreateApiView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = CategorySerializer


class QuestionCreateApiView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    search_fields = ['difficulty_level','date','title']
    filter_backends = (SearchFilter,)
    queryset = Questions.objects.all()

    serializer_class = QuestionSerializer

class TakeQuestionApiView(APIView):
    def get(self,request,**kwargs):
        quiz=kwargs.get("id")
        print(quiz)
        questions=Questions.objects.filter(quiz_id=quiz)
        print(questions)
        serializer=QuizTakeSerializer(questions,many=True)
        return Response(serializer.data)


class RetriveQuizByCategory(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, **kwargs):
        cat = kwargs.get("id")

        # serializer_class = QuizByCategorySerializer
        print(cat)
        quiz=Quiz.objects.filter(category_id=cat)
        print(quiz)
        serializer=QuizByCategorySerializer(quiz,many=True)
        return Response(serializer.data)

class RetrieveQuestionsByQuizId(APIView):

    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, **kwargs):
        quiz = kwargs.get("id")

        # serializer_class = QuizByCategorySerializer
        print(quiz)
        quiz=Questions.objects.filter(quiz_id=quiz)
        if quiz:
            serializer=QuestionsByQuizId(quiz,many=True)
            return Response(serializer.data)
        else:
            return Response({"Message":"No questions under the given category"})

class AnswerCreateApiView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Result.objects.all()
    serializer_class = AnswerSerializer
    def create(self, request, *args, **kwargs):
        user = request.user
        question_id=request.data["question"]
        question=Questions.objects.get(id=question_id)
        ans=Result.objects.filter(question_id=question_id,user_id=user.id)
        if ans:
            return Response({"Message": "You already attended the quiz.."})
        else:
            quiz=Quiz.objects.get(id=question.quiz_id)
            serializer=AnswerSerializer(data=request.data,context={"user":user,"quiz":quiz,"question":question})
            if serializer.is_valid():
                serializer.save()
                return Response(data=serializer.data)
            else:
                return Response(data=serializer.errors)

class CalculateMArksApiView(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Result.objects.all()
    serializer_class = AnswerSerializer
    def retrieve(self, request, *args, **kwargs):
        # Get all questions for the quiz
        user = request.user
        quiz=kwargs.get("pk")
        chk=Result.objects.filter(user_id=user,quiz_id=quiz)
        questions=Questions.objects.filter(quiz_id=quiz)
        if questions and chk:
            cnt=Questions.objects.filter(quiz_id=quiz).count()

            total_marks = 0
            answer_data = []
            for question in questions:
                # Get the correct answer for the question
                correct_answer = question.correct_answer

                # Get the user's answer from the answers dictionary
                user_answ=Result.objects.get(user=user,question_id=question.id)

                # Check if the user's answer is correct
                if user_answ.answer == correct_answer:
                    # Assign marks for correct answers
                    marks=1
                    total_marks+=1
                else:
                    marks=0



            #     # Add the marks to the total marks for the quiz
            #     total_marks += marks
            #
                # Add the answer data to the list
                answer_data.append({
                    'question': question.question_text,
                    'user_answer': user_answ.answer,
                    'correct_answer': correct_answer,
                    'marks': marks,
                })
            if total_marks>=int(cnt/2):
                statuss='Passed'
            already_chk=UserQuizAnswer.objects.get(user=user,quiz_id=quiz)
            if already_chk:
                return Response("You already calculated mark")
            else:
                qzans = UserQuizAnswer.objects.create(user=user, quiz_id=quiz, marks=total_marks,status=statuss)
                return Response({"Total Score is ":total_marks,"Total Questions ":cnt,"Your Answers":answer_data})
        else:
            return Response({"Message":"You didnt attend this quiz yet"})

class UserScoreForEachQuizView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    # queryset = UserQuizAnswer.objects.all()
    # serializer_class = UserScoreForEachQuizSerializer
    def get(self, request, **kwargs):
        user=request.user

        quiz_result = UserQuizAnswer.objects.filter(user_id=user.id)


        # return Response({"msg":"mk"})
        if quiz_result:
            serializer = UserScoreForEachQuizSerializer(quiz_result, many=True)
            return Response(serializer.data)
        else:
            return Response({"msg":"No data to display"})

class UserProfileDisplayView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self,request,**kwargs):
        user=User.objects.get(id=request.user.id)
        if user:
            serializer=UserProfileDisplaySerializer(user)
            lst=[]
            lst1=[]
            lst.append(serializer.data)
            quiz=Quiz.objects.filter(user_id=request.user.id)
            print(quiz)
            for q in quiz:
                serializer1=QuizByUSerSerializer(q)
                lst1.append(serializer1.data)
            return Response({"profile":lst[0],"Quizes Created":lst1})
        else:
            return Response({"Nothing to display"})

# Quiz Analytics: The system should display analytics on each quiz, such as the average score,
# the number of times the quiz has been taken,
# and the percentage of users who have passed the quiz.

class QuizAnalysisView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = UserQuizAnswer.objects.all()
    serializer_class = QuizAnalysisSerializer

    def list(self,request, *args, **kwargs):
        user = request.user
        analysis=[]
        quiz_result = UserQuizAnswer.objects.filter(user_id=user.id)
        if quiz_result:
            for result in quiz_result:
                quest_cnt=Questions.objects.filter(quiz_id=result.quiz_id).count()
                quiz=Quiz.objects.filter(id=result.quiz_id)
                quiz_user_cnt=UserQuizAnswer.objects.filter(quiz_id=result.quiz_id,status='Passed').count()

                total_cnt=UserQuizAnswer.objects.filter(quiz_id=result.quiz_id).count()
                for q in quiz:
                    analysis.append({
                        'Quiz':q.quiz_title,
                        'Total Marks':result.marks,
                        'Average-score': result.marks/result.cnt,
                        'No of times quiz taken':result.cnt,
                        'Number of users attended this quiz':total_cnt,
                        'Percentage of users passed quiz':(quiz_user_cnt/total_cnt)*100

                    })
            return Response(analysis)
        else:
            return Response("No data")

class LogoutView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({"Message":"Lgout successfully"})
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)








