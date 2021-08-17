from django.db import models, transaction
from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.signals import post_save
from django.dispatch import receiver
from django_rest_passwordreset.signals import reset_password_token_created
from django.db.models import Sum
from django.template.loader import render_to_string, get_template
from django.core.mail import get_connection, EmailMultiAlternatives

class CustomUserManager(UserManager):
    def get_by_natural_key(self, username):
        case_insensitive_username_field = '{}__iexact'.format(self.model.USERNAME_FIELD)
        return self.get(**{case_insensitive_username_field: username})

# Create your models here.
class User(AbstractUser):
    STUDENT = 'ST'
    TEACHER = 'TE'
    USER_ROLE = (
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    )

    who_is = models.CharField(max_length=2, choices=USER_ROLE, default=TEACHER)
    objects = CustomUserManager()
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

    def is_it_my_course(self, course_id):
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.filter(course__user=self).exists()
    
    @transaction.atomic
    def set_course_payment(self, course_id):
        if self.is_it_my_course(course_id):
            course = Course.objects.get(pk=course_id)
            user = self
            subs = Subscription.objects.get(course__user=user)
            subs.status = 'PA'
            subs.save()
            return True
        else:
            return False

    @property
    def numero_aulas(self):
        courses = Course.objects.filter(user=self)
        return Lecture.objects.filter(course_in = courses).count()

    def is_it_my_course(self, course_id):
        course = Course.objects.get(pk=course_id)
        return Subscription.objects.filter(user=self, course=course).exists()
    
    @transaction.atomic
    def buy_course(self, course_id):
        if not self.is_it_my_course(course_id):
            course = Course.objects.get(pk=course_id)
            user = self
            Subscription.objects.create(course=course, user=user, price=course.price)
            return True
        else:
            return False

    @transaction.atomic
    def favorite_course(self, course_id):
        course = Course.objects.get(pk=course_id)
        user = self

        subscription = Subscription.objects.get(course=course, user=user)
        subscription.is_favorite = not subscription.is_favorite
        subscription.save()

    @transaction.atomic
    def remove_course(self, course_id):
        course = Course.objects.get(pk=course_id)
        user = self

        subscription = Subscription.objects.get(course=course, user=user)
        subscription.delete()

    @transaction.atomic
    def rate_course(self, course_id, rating):
        course = Course.objects.get(pk=course_id)
        user = self

        subscription = Subscription.objects.get(course=course, user=user)
        subscription.rating = rating
        subscription.save()

class Course(models.Model):
    name = models.CharField(max_length=200)
    thumb = models.CharField(max_length=255, null=True, blank=True)
    created_date = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(decimal_places=2, max_digits=8)
    user = models.ForeignKey("User", related_name="courses", on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    @property
    def numero_alunos(self):
        return Subscription.objects.filter(course=self).count()

    @property
    def total_subscricoes(self):
        out = self.subscriptions.all()
        cont = 0
        for i in out:
            cont += i.price
        print(cont)
        return cont

class Subscription(models.Model):
    PAID = 'PA'
    PENDING = 'PE'
    PAYMENT_STATUS = (
        (PAID, 'Paid'),
        (PENDING, 'Pending'),
    )
    status = models.CharField(
        max_length=2,
        choices=PAYMENT_STATUS,
        default=PENDING,
    )
    price = models.DecimalField(decimal_places=2, max_digits=8)
    user = models.ForeignKey("User", related_name="subscriptions", on_delete=models.CASCADE)
    course = models.ForeignKey("Course", related_name="subscriptions", on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=False)
    rating = models.DecimalField(default=0, decimal_places=1, max_digits=2)


class DiscountCoupon(models.Model):
    PER_PRICE = 'PPR'
    PER_PERCENTAGE = 'PPE'
    DISCOUNT_CHOICES = (
        (PER_PRICE, 'Per Price'),
        (PER_PERCENTAGE, 'Per Percentage'),
    )
    discount_type = models.CharField(
        max_length=3,
        choices=DISCOUNT_CHOICES,
        default=PER_PRICE,
    )
    value = models.DecimalField(decimal_places=2, max_digits=8)
    expiration_date = models.DateField()
    course = models.ForeignKey("Course", related_name="discount_coupons", on_delete=models.CASCADE)


@receiver(reset_password_token_created)
def password_reset_token_created(sender, reset_password_token, *args, **kwargs):
    """
    Handles password reset tokens
    When a token is created, an e-mail needs to be sent to the user
    :param sender:
    :param reset_password_token:
    :param args:
    :param kwargs:
    :return:
    """
    # send an e-mail to the user
    context = {
        'current_user': reset_password_token.user,
        'username': reset_password_token.user.username,
        'email': reset_password_token.user.email,
        # ToDo: The URL can (and should) be constructed using pythons built-in `reverse` method.
        'reset_password_url': "http://some_url/reset/?token={token}".format(token=reset_password_token.key)
    }

    # render email text
    email_html_message = render_to_string('email/user_reset_password.html', context)
    email_plaintext_message = render_to_string('email/user_reset_password.txt', context)

    msg = EmailMultiAlternatives(
        # title:
        "Password Reset for {title}".format(title="Some website title"),
        # message:
        email_plaintext_message,
        # from:
        "noreply@somehost.local",
        # to:
        [reset_password_token.user.email]
    )
    msg.attach_alternative(email_html_message, "text/html")
    msg.send()