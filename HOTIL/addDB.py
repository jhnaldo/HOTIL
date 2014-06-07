# -*- coding: utf-8-*-`

from board.models import Problem
from django.contrib.auth.models import User

def init():
    manager = User.objects.create_user(username='test_manager', password='1234')
    student = User.objects.create_user(username='test_student', password='1234')
    manager.first_name = '관리자'
    student.first_name = '학생'
    manager.is_staff = True
    manager.save()
    student.save()
