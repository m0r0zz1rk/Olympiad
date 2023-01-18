from service.models import QuestionColumns, TableAnswers


def CreateRowsForQuestion(label, question_id, seq_number) -> None:
    """Создание строки ответов для каждого существующего заголовка столбцов вопроса"""
    for column in QuestionColumns.objects.filter(question_id=question_id):
        new_row = TableAnswers(
            label=label,
            column_id=column.id,
            seq_number=seq_number
        )
        new_row.save()
    return None