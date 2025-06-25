from apps.user.models import User
from typing import Optional

from django.db.models import QuerySet
from django.contrib.auth.models import Group


def create_user(data: dict) -> User:
    password = data.pop("password", None)
    user = User(**data)
    if password:
        user.set_password(password)
    user.save()

    try:
        group = Group.objects.get(id=2)
        user.groups.add(group)
    except Group.DoesNotExist:
        pass
    return user


def get_users_filtered(group_id: Optional[int] = None) -> QuerySet:
    users = User.objects.all()
    if group_id:
        users = users.filter(groups__id=group_id)
    return users
