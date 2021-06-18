import graphene
from graphene_django import DjangoObjectType
from graphene_django import DjangoListField

from .models import Quizzes, Category, Question, Answer


class CategoryType(DjangoObjectType):
    class Meta:
        model = Category
        fields = ("id", "name")


class QuizzesType(DjangoObjectType):
    class Meta:
        model = Quizzes
        fields = ("id", "title", "category", "date_created")


class QuestionType(DjangoObjectType):
    class Meta:
        model = Question
        fields = ("title", "quiz")


class AnswerType(DjangoObjectType):
    class Meta:
        model = Answer
        fields = ("question", "answer_text", "is_right")


class Query(graphene.ObjectType):

    all_questions = graphene.Field(QuestionType, id=graphene.Int())
    all_answers = graphene.List(AnswerType, id=graphene.Int())
    all_categories = graphene.List(CategoryType)
    # all_quizzes = DjangoListField(QuizzesType)
    all_quizzes = graphene.List(QuizzesType)

    quiz = graphene.String()

    def resolve_all_questions(root, info, id):
        return Question.objects.get(pk=id)

    def resolve_all_answers(root, info, id):
        return Answer.objects.filter(question=id)

    def resolve_all_quizzes(root, info):
        return Quizzes.objects.filter(pk=2)

    def resolve_all_categories(root, info):
        return Category.objects.all()

    def resolve_quiz(root, info):
        return f"This is some line"


class CategoryMutation(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name):
        category = Category(name=name)
        category.save()
        return CategoryMutation(category=category)


class CategoryRenaming(graphene.Mutation):
    class Arguments:
        id = graphene.ID()
        name = graphene.String(required=True)

    category = graphene.Field(CategoryType)

    @classmethod
    def mutate(cls, root, info, name, id):
        category = Category.objects.get(pk=id)
        category.name = name
        category.save()
        # category.delete()     # For deleting
        return CategoryMutation(category=category)


class Mutation(graphene.ObjectType):

    update_category = CategoryMutation.Field()
    rename_category = CategoryRenaming.Field()

schema = graphene.Schema(query=Query, mutation=Mutation)
