from django.test import TestCase

# Create your tests here.
from django.contrib.auth.models import User
user = User.objects.get(username='your_username')
print(user.get_group_permissions())
