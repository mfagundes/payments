from datetime import datetime

from decouple import config

from core.errors import CalculationException


def cleaning_date_to_use_with_celery(day):
    if isinstance(day, str):
        if 'T' in day:
            day = day.split('T')[0]
        day = datetime.strptime(day, "%Y-%m-%d").date()

    if isinstance(day, datetime):
        day = day.date()

    return day


def create_logentry(creator, object, message=None, is_change=False):
    from django.contrib.admin.models import LogEntry, ADDITION, CHANGE, ContentType

    if not message:
        message = 'Adicionado.'

    LogEntry.objects.log_action(
        user_id=creator.id,
        content_type_id=ContentType.objects.get_for_model(object).pk,
        object_id=object.id,
        object_repr=str(object),
        action_flag=CHANGE if is_change else ADDITION,
        change_message=message,
    )


def calculate_discount(current_value, due_date, new_date):
    daily_discount = config('DAILY_DISCOUNT', default=0, cast=float)
    if not new_date:
        raise CalculationException

    try:
        date_diff = due_date - new_date
        if date_diff.days <= 0:
            #TODO treat errors
            raise CalculationException("Data igual ou inferior à data de vencimento")
        total_discount = (daily_discount / 30) * date_diff.days
        new_value = round(float(current_value) * (1 - total_discount), ndigits=2)
        return new_value
    except CalculationException:
        pass
