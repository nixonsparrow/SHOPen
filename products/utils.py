from django.utils import timezone


def two_weeks_from_now():
    return (timezone.now() + timezone.timedelta(weeks=2)).date()
