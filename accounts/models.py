from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass
# ستكون بيانات المتجر في مودل اخر مربوط بال User 
# اما في المستقبل اذا تم اضافة موظفين فقط سانشئ group من الصلاحيات و اعطيه لهم و بالنسبة لصاحب المتجر اخصص له صلاحية معينة تمكنه من فعل اي شيئ او ببساطة صلاحية مثل staff او superuser