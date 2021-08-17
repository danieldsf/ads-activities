from rest_framework import generics, mixins, viewsets
from rest_framework.permissions import *
from rest_framework.response import Response
from rest_framework.reverse import reverse
from .permissions import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.authtoken.views import ObtainAuthToken, Token
from rest_framework.decorators import api_view

class FaturamentoView(APIView):
    def get(self, request):
        all_faturamento = request.user.courses.all()
        contador = 0
        for i in all_faturamento:
            contador += i.total_subscricoes

        return Response({'faturamento': contador})

class CurrentUserView(APIView):
    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

@api_view(['POST'])
def remove_course(request):
    course = request.data['course']
    user = request.user
    return Response({'status': user.remove_course(course)})

@api_view(['POST'])
def favorite_course(request):
    course = request.data['course']
    user = request.user
    return Response({'status': user.favorite_course(course)})

@api_view(['POST'])
def buy_course(request):
    course = request.data['course']
    
    user = request.user
    
    return Response({'status': user.buy_course(course)})

class CustomAuthToken(ObtainAuthToken):
    
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_serializer = UserSerializer(serializer.validated_data['user'])
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'user': user_serializer.data
        })

class CourseList(generics.ListCreateAPIView):
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        return Course.objects.filter(user=self.request.user)

    serializer_class = CourseSerializer
    name = 'course_list'
    filter_fields = ('price',)
    permission_classes = (OnlyTeacherCanEditCourse,)

class PublicCourseList(generics.ListCreateAPIView):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    name = 'public_course_list'
    filter_fields = ('price',)
    permission_classes = (OnlyTeacherCanEditCourse,)

class CourseDetail(generics.RetrieveUpdateDestroyAPIView):
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    name = 'course_detail'
    permission_classes = (OnlyTeacherCanEditCourse,)

class DiscountCouponDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = DiscountCouponSerializer
    name = 'discountcoupon_detail'
    permission_classes = (IsAuthenticated, OnlyTeacherCan)

    def get_queryset(self):
        user = self.request.user
        if self.request.auth != None:
            courses = Course.objects.filter(teacher = user)
            return Subscription.objects.filter(courses_in = courses)

class DiscountCouponList(generics.ListCreateAPIView):
    queryset = DiscountCoupon.objects.all()
    serializer_class = DiscountCouponSerializer
    name = 'discountcoupon_list'
    permission_classes = (IsAuthenticated, OnlyTeacherCan)

class SubscriptionDetail(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SubscriptionSerializer
    name = 'subscription_detail'
    permission_classes = (IsAuthenticated, OnlyStudentCourses)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Subscription.objects.filter(user=user)

class SubscriptionList(generics.ListCreateAPIView):
    serializer_class = SubscriptionSerializer
    name = 'subscription_list'
    permission_classes = (IsAuthenticated, OnlyStudentCourses)

    def get_queryset(self):
        """
        This view should return a list of all the purchases
        for the currently authenticated user.
        """
        user = self.request.user
        return Subscription.objects.filter(user=user)
   
class TeacherDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSerializer
    name = 'teacher_detail'

class TeacherList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = TeacherSerializer
    name = 'teacher_list'

class StudentDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    name = 'student_detail'

class StudentList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = StudentSerializer
    name = 'student_list'

class ApiRoot(generics.GenericAPIView):
    name = 'api-root'
    def get(self, request, *args, **kwargs):
        return Response({
            'courses': reverse(CourseList.name, request = request),
            'students': reverse(StudentList.name, request = request),
            'teachers': reverse(TeacherList.name, request = request),
            'subscriptions': reverse(SubscriptionList.name, request = request),
            'discoutcoupon': reverse(DiscountCouponList.name, request = request)
        })
