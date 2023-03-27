from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Quiz,Questions,Result,Category,UserQuizAnswer

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "email",
            "username",
            "password"
        ]

    def create(self,validated_data):
        user=User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        user = self.context['request'].user

        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.set_password(validated_data['password'])
        instance.save()

        return instance

class CategorySerializer(serializers.ModelSerializer):
    # name=serializers.CharField(read_only=True)
    class Meta:
        model=Category
        fields="__all__"


class QuizSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'

    def create(self, validated_data):
        user=self.context.get("user")
        return Quiz.objects.create(**validated_data,user=user)

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model=Questions
        fields="__all__"

class QuizTakeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Questions
        fields=["question_text","option1","option2","option3","option4"]

class QuizByCategorySerializer(serializers.ModelSerializer):
    name=serializers.CharField(read_only=True)
    class Meta:
        model=Quiz
        # exclude=["quiz_title","user"]
        fields="__all__"
class QuestionsByQuizId(serializers.ModelSerializer):
    class Meta:
        model=Questions
        # exclude=["quiz_title","user"]
        fields="__all__"

class AnswerSerializer(serializers.ModelSerializer):
    user=serializers.CharField(read_only=True)
    class Meta:
        model=Result
        fields="__all__"
    def create(self, validated_data):
        user=self.context.get("user")
        quiz=self.context.get("quiz")
        question=self.context.get("question")
        return Result.objects.create(user=user,quiz=quiz,**validated_data)

class MarksSerializer(serializers.ModelSerializer):
    class Meta:
        model=Result
        fileds="__all__"

class UserScoreForEachQuizSerializer(QuizSerializer):
    class Meta:
        model=UserQuizAnswer
        exclude=["id",'cnt']
    def to_representation(self, instance):
        representation = super(QuizSerializer,self).to_representation(instance)
        quz=representation.pop("quiz")
        ins=Quiz.objects.get(id=quz)
        representation['quiz']=ins.quiz_title
        quiz_no='Result of '+ins.quiz_title
        return {quiz_no:representation}

class UserProfileDisplaySerializer(UserSerializer):
    class Meta:
        model=User
        fields=["email","username"]

    def retrieve(self, request, *args, **kwargs):
        user = request.user
        ur = User.objects.get(user=user.id)
        return ur

    # def get(self,request):
    #     user=UserSerializer(id=request.user.id)
    #     return user
class QuizByUSerSerializer(serializers.ModelSerializer):
    # quiz_title=serializers.CharField(read_only=True)
    # user=serializers.CharField(read_only=True)
    class Meta:
        model=Quiz
        fields=["quiz_title","date_created"]

class QuizAnalysisSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserQuizAnswer
        exclude = ["id"]

    # def get(self, request, *args, **kwargs):
    #     user = request.user
    #     print(user)
        # def retrieve(self, request, *args, **kwargs):
        # ans=UserQuizAnswer.objects.get(user_id=user)
        # score=ans.marks
        # avg=score/ans.cnt
        # return ({"Score":score,"Average score":avg})



