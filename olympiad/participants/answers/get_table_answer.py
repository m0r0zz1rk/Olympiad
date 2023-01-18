from service.models import TableAnswers


def GetTableAnswerStr(id) -> str:
    """Получение строки вида "ID столбца-Порядковый номер" для табличного ответа на основе полученной ID записи"""
    ans = TableAnswers.objects.get(id=id)
    return f'{ans.column_id}-{str(ans.seq_number)}'


def GetIdTableAnswer(col_id, seq_number) -> int:
    """Получение ID строки табличных ответов на основе полученных ID столбца и порядковоого номера"""
    return TableAnswers.objects.filter(
            column_id=col_id
        ).filter(
            seq_number=seq_number
        ).latest('id').id
