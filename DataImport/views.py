from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from . import services
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from UserProfile.models import Employee

# only allow superusers access


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request):

    if Employee.objects.filter(user_id=request.user.id).exists():
        employee = Employee.objects.get(user_id=request.user.id)
    else:
        employee = ''

    context = {
        'employee': employee,
    }

    return render(request, 'data.html', context)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_emp(request):

    results = services.import_users(request)

    return HttpResponse('Results: ' + results)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_stores(request):

    results = services.import_stores()

    return HttpResponse('Results: ' + results)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_msg_types(request):

    results = services.import_notification_settings()
    return HttpResponse('Results: ' + results)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_status(request):

    results = services.import_statuses()

    return HttpResponse('Results: ' + results)


@login_required
@user_passes_test(lambda u: u.is_superuser)
def add_messages(request):

    results = services.import_messages()

    return HttpResponse('Results: ' + results)


