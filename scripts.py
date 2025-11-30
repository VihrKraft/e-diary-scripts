import random
from datacenter.models import Schoolkid, Subject, Lesson, Mark, Chastisement, Commendation


def fix_marks(schoolkid):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        bad_marks = Mark.objects.filter(schoolkid=student, points__lte=3)
        for bad_mark in bad_marks:
            bad_mark.points=5
            bad_mark.save()
    except Schoolkid.MultipleObjectsReturned: 
        print('По вашему запросу найдено больше 1 ученика. Введите более точный запрос.')
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. Попробуйте повторить запрос, исправив ошибки.')


def remove_chastisements(schoolkid):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        chastisements = Chastisement.objects.filter(schoolkid=student)
        chastisements.delete()
    except Schoolkid.MultipleObjectsReturned:
        print('По вашему запросу найдено больше 1 ученика. Введите более точный запрос.')
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. Попробуйте повторить запрос, исправив ошибки.')
    

def create_commendation(schoolkid, name_subject):
    try:
        student = Schoolkid.objects.get(full_name__contains=schoolkid)
        subject = Subject.objects.get(title__contains=name_subject, year_of_study=student.year_of_study)  
        lessons = Lesson.objects.filter(year_of_study=student.year_of_study, group_letter=student.group_letter, subject=subject)
        lesson = random.choice(lessons)
        comendations=Commendation.objects.filter(schoolkid=student, subject=subject)
        comendation_text=random.choice(['Молодец', 'Хвалю!', 'Гораздо лучше, чем я ожидал!', 'Очень хороший ответ!', 'Замечательно!', 'Так держать!', 'Ты на верном пути!'])
        comendations.create(schoolkid=student, teacher=lesson.teacher, subject=lesson.subject, created=lesson.date, text=comendation_text)
    except Schoolkid.MultipleObjectsReturned: 
        print('По вашему запросу найдено больше 1 ученика. Введите более точный запрос.')
    except Schoolkid.DoesNotExist:
        print('Ученик не найден. Попробуйте повторить запрос, исправив ошибки.')
    except Subject.MultipleObjectsReturned: 
        print('По вашему запросу найдено больше 1 предмета. Введите более точный запрос.')
    except Subject.DoesNotExist:
        print('Предмет не найден. Попробуйте повторить запрос, исправив ошибки.')
