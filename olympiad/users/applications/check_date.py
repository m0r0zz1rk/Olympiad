from service.models import Olympiads


def CheckAppDateSave(date) -> bool:
    """Проверка на дату сохранения заявки (должна быть в диапазоне дат подачи заявок для одной из олимпиад в базе)"""
    return Olympiads.objects.filter(date_reg_start__lte=date).\
            filter(date_reg_end__gte=date).exists()
