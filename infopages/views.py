from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from .models import *
import random
from django.http.response import JsonResponse
# from django.contrib.auth.models import User
# from django.contrib.auth.forms import AuthenticationForm


def home(request):
    katkurs = KCat.objects.order_by('id')  # категории
    kurses = Kurse.objects.all()  # курсы
    return render(request, 'infopages/index.html', {'kurses': kurses, 'katkurs': katkurs})


def about(request):
    return render(request, 'infopages/about.html')


def kurs(request):
    if request.method == 'GET':
        kurseid = request.GET['id']
        try:
            kursdata = Kurse.objects.get(id=kurseid)
        except Exception as e:
            print(e)
            return redirect('page404')
        steps = Step.objects.all().filter(kurseid_id=kurseid).count()
        stepsdata = Step.objects.order_by('order_number').filter(kurseid_id=kurseid)
        return render(request, 'infopages/kurs.html', {'kursdata': kursdata, 'stepsdata': stepsdata, 'steps': steps})
    else:
        pass


def step(request):
    if request.method == 'GET':
        stepid = request.GET['id']
        try:
            stepdata = Step.objects.get(id=stepid)
        except Exception as e:
            print(e)
            return redirect('page404')

        # делаем ссылки для предыдущего и следующего материалов
        kurse_id = stepdata.kurseid_id
        stepnumber = stepdata.order_number
        steps = Step.objects.all().filter(kurseid_id=kurse_id).count()
        nextqid = ''
        prvqid = ''
        prev = stepnumber - 1
        nexts = stepnumber + 1
        if 1 < stepnumber < steps:
            prvq = Step.objects.all().filter(kurseid_id=kurse_id).filter(order_number=prev)
            if prvq:
                for e in prvq:
                    prvqid = e.id
            else:
                prvqid = 0

            nextq = Step.objects.all().filter(kurseid_id=kurse_id).filter(order_number=nexts)
            if nextq:
                for e in nextq:
                    nextqid = e.id
            else:
                nextqid = 0
        if stepnumber == 1:
            prvqid = 0
            nextq = Step.objects.all().filter(kurseid_id=kurse_id).filter(order_number=nexts)
            if nextq:
                for e in nextq:
                    nextqid = e.id
            else:
                nextqid = 0

        if stepnumber == steps:
            nextqid = 0
            prvq = Step.objects.all().filter(kurseid_id=kurse_id).filter(order_number=prev)

            if prvq:
                for e in prvq:
                    prvqid = e.id
            else:
                prvqid = 0

        return render(request, 'infopages/step.html', {'stepdata': stepdata, 'prvqid': prvqid, 'nextqid': nextqid})
    else:
        pass


def loginpage(request):
    if request.method == 'GET':
        return render(request, 'infopages/login.html')
    else:
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'infopages/login.html', {'error': '&nbsp;Неверное имя пользователя, или пароль.'})
        else:
            login(request, user)
            return redirect('stats')


def logoutpage(request):
    if request.method == 'POST':
        logout(request)
        return render(request, 'infopages/logout.html')


def page404(request):
    return render(request, 'infopages/404.html')


def userstats(request):
    if request.user.is_superuser:
        return redirect('/admin')
    else:
        try:
            courses = Nazn.objects.get(user=request.user.id).kurse.all()
            resultdata = []
            for elem in courses:
                error = ''
                try:
                    results = Results.objects.get(user=request.user, kurseid=elem.id)
                    result_int = results.result_int

                except Exception as e:
                    result_int = 0
                    error = e

                resultdata.append({
                    'kurseid': elem.id,
                    'title': elem.title,
                    'result_int': result_int,
                    'error': error
                })

            zadaniya = Zadanie.objects.all().filter(user=request.user)
            zadanie = []
            for elm in zadaniya:
                zadanie.append({
                    'text': elm.text,
                    'vipolnen': elm.vipolnen,
                })

            return render(request, 'infopages/lk.html', {'results': resultdata, 'zadanie': zadanie})

        except Exception as e:
            return render(request, 'infopages/lk.html', {'error': e})


def test(request):
    try:
        # получаем список назначенных курсов
        datac = []
        # кол во вопросов изначально = 0
        qwc = 0
        courses_objs = Nazn.objects.get(user=request.user.id).kurse.all()
        for courses_obj in courses_objs:
            error = ''
            try:
                results = Results.objects.get(user=request.user, kurseid=courses_obj.id)
                result_int = results.result_int

            except Exception as e:
                result_int = 0
                error = e

            if result_int != 100:
                # для каждого из курсов получаем уроки
                steps_objs = Step.objects.order_by('order_number').filter(kurseid_id=courses_obj.id)
                datas = []
                for steps_obj in steps_objs:
                    # для каждого урока в курсе получаем вопросы
                    question_objs = list(Question.objects.filter(stepid_id=steps_obj.id))
                    dataq = []
                    random.shuffle(question_objs)
                    for question_obj in question_objs:
                        qwc = qwc+1
                        dataa = []
                        answer_objs = list(Answer.objects.filter(questionid_id=question_obj.id))
                        random.shuffle(answer_objs)
                        for answer_obj in answer_objs:
                            dataa.append({
                                'answer_id': answer_obj.id,
                                'text': answer_obj.answer,
                                'is_correct': answer_obj.is_correct
                            })

                        dataq.append({
                            'question_id': question_obj.id,
                            'text': question_obj.question,
                            'answer': dataa
                        })

                    datas.append({
                        'step_id': steps_obj.id,
                        'steptitle': steps_obj.title,
                        'question': dataq
                    })

                datac.append({
                    'course_id': courses_obj.id,
                    'coursetitle': courses_obj.title,
                    'step': datas,
                    'error': error
                })
        payload = {'data': datac, 'qwc': qwc}
    except Exception as e:
        return render(request, 'infopages/test.html', {'error': e})
    return render(request, 'infopages/test.html', payload)
    # return JsonResponse(payload)


def result(request):
    payload = []
    answers = []
    negative = []
    negative_steps = []
    if request.method == 'GET':  # получаем массив с ответами
        datac = []
        # получаем список назначенных курсов
        courses_objs = Nazn.objects.get(user=request.user.id).kurse.all()
        for courses_obj in courses_objs:
            c = str(courses_obj.id)
            maximum_count = 0
            right_count = 0
            negative_count = 0
            # для каждого из курсов получаем уроки
            steps_objs = Step.objects.order_by('order_number').filter(kurseid_id=courses_obj.id)
            for steps_obj in steps_objs:
                # для каждого урока в курсе получаем вопросы
                question_objs = list(Question.objects.filter(stepid_id=steps_obj.id))
                for question_obj in question_objs:
                    answered = 0
                    # для каждого вопроса получаем количество правильных ответов
                    mc = Answer.objects.filter(questionid_id=question_obj.id).filter(is_correct=True).count()
                    maximum_count = maximum_count + mc  # плюсуем получая максимальный балл
                    rrr = Answer.objects.all().filter(questionid_id=question_obj.id).filter(is_correct=True)
                    for el in rrr:
                        a = str(el.id)
                        if request.GET.get('answerid[' + c + '][' + a + ']'):  # есть верный ответ в гет
                            right_count = right_count+1
                            answered = 1
                            answers.append({
                                'right_ids': request.GET.get('answerid[' + c + '][' + a + ']')
                            })
                        else:  # верного ответа в гет нет, значит добавляем материал в плохо освоенные
                            negative_steps.append({
                                'negative_st': steps_obj.id
                            })

                    nnn = Answer.objects.all().filter(questionid_id=question_obj.id).filter(is_correct=False)
                    for el in nnn:
                        n = str(el.id)
                        if request.GET.get('answerid[' + c + '][' + n + ']'):
                            negative_count = negative_count+0.5
                            if answered == 1:
                                negative_count = negative_count+0.5  # если уже есть верный ответ, то прибавляем еще 0.5

                            negative.append({
                                'negative_ids': request.GET.get('answerid[' + c + '][' + n + ']')
                            })
                            negative_steps.append({
                                'negative_st': steps_obj.id
                            })
            error = ''
            try:
                itogo = (right_count-negative_count)/maximum_count*100
            except Exception as e:
                error = e
                itogo = 0
            if itogo < 0:
                itogo = 0

            if itogo > 1:
                delres = Results.objects.filter(user=request.user, kurseid=courses_obj.id)
                delres.delete()
                newres = Results(user=request.user, kurseid=courses_obj.id, result_int=int(itogo))
                newres.save()

            datac.append({
                'course_id': courses_obj.id,
                'coursetitle': courses_obj.title,
                'maximum_count': maximum_count,
                'right_count': right_count,
                'negative_count': int(negative_count),
                'itogo': int(itogo),
            })
        # уникализируем список уроков в которых были ошибки
        negative_steps = list(set(val for dic in negative_steps for val in dic.values()))
        nstepsdata = []
        # запрашиваем по этим урокам инфу
        for el in negative_steps:
            nsteps = Step.objects.get(id=el)
            nstepsdata.append({
                'nstepid': el,
                'title': nsteps.title,
            })

        payload = {'data': datac, 'answers': answers, 'negative': negative, 'negative_steps': nstepsdata, }
    return render(request, 'infopages/result.html', payload)
    # return JsonResponse(payload)
