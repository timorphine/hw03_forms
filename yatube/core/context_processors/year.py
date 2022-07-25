import datetime


def year(request):
    """Выводит значение текущего года"""
    year_now = datetime.datetime.today()
    return {
        'year': year_now.strftime('%Y')
    }
