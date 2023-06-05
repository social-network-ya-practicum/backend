from django.db.models import Q

from users.models import CustomUser


def filter_birthday(current_day, current_month, next_month, day_one, day_two):
    """
    Если 30 число нечетного месяца или 29 число четного месяца
    Если 28 число високосного года или 27 невисоконого месяц февраль
    """
    if current_day == day_one:
        queryset = CustomUser.objects.filter(
            (Q(birthday_date__gte=current_day)
             & Q(birthday_date__lte=current_day + 1)
             & Q(birthday_date__month=current_month))
            | (Q(birthday_date__day=1)
               & Q(birthday_date__month=next_month))
        ).order_by('birthday_date')[:3]
        return queryset
    """
    Если 31 число нечетного месяца или 30 число четного месяца
    Если 29 число високосного года или 28 невисокосного месяц февраль
    """
    if current_day == day_two:
        queryset = CustomUser.objects.filter(
            (Q(birthday_date=current_day)
             & Q(birthday_date__month=current_month))
            | ((Q(birthday_date__day=1)
               | Q(birthday_date__day=2))
               & Q(birthday_date__month=next_month))
        ).order_by('birthday_date')[:3]
        return queryset
    queryset = CustomUser.objects.filter(
        birthday_date__day__gte=current_day,
        birthday_date__day__lt=(current_day + 3),
        birthday_date__month=current_month
    ).order_by('birthday_date')[:3]
    return queryset
