import random
from datacenter.models import Schoolkid, Subject, Lesson, Mark, Chastisement, Commendation


def studentExcepts(schoolkid):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        return student
    except Schoolkid.MultipleObjectsReturned:
        print('По вашему запросу найдено больше 1 ученика. Введите более точный запрос.')
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. Попробуйте повторить запрос, исправив ошибки.')


def subjectExcepts(name_subject, student):
    try:
        if student:
            subject = Subject.objects.get(title__contains=name_subject, year_of_study=student.year_of_study)  
            return subject
    except Subject.MultipleObjectsReturned: 
        print('По вашему запросу найдено больше 1 предмета. Введите более точный запрос.')
    except Subject.DoesNotExist:
        print('Предмет не найден. Попробуйте повторить запрос, исправив ошибки.')


def fix_marks(schoolkid):
    student = studentExcepts(schoolkid)
    if student:
        bad_marks = Mark.objects.filter(schoolkid=student, points__lte=3)
        bad_marks.update(points=5)


def remove_chastisements(schoolkid):
    student = studentExcepts(schoolkid)
    if student:
        chastisements = Chastisement.objects.filter(schoolkid=student)
        chastisements.delete()
    

def create_commendation(schoolkid, name_subject):
    student = studentExcepts(schoolkid)
    subject = subjectExcepts(name_subject, student)
    if subject and student:
        lessons = Lesson.objects.filter(year_of_study=student.year_of_study, group_letter=student.group_letter, subject=subject)
        lesson = random.choice(lessons)
        comendation_text=random.choice(['Молодец', 'Хвалю!', 'Гораздо лучше, чем я ожидал!', 'Очень хороший ответ!', 'Замечательно!', 'Так держать!', 'Ты на верном пути!'])
        Commendation.objects.create(schoolkid=student, teacher=lesson.teacher, subject=lesson.subject, created=lesson.date, text=comendation_text)
