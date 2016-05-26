from django.contrib.auth.decorators import login_required, user_passes_test
from . import services
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test

# only allow superusers access


@login_required
@user_passes_test(lambda u: u.is_superuser)
def index(request):
    if 'action' in request.GET:
        action = request.GET['action']
        if request.GET['action'] == 'user':
            results = services.import_users()

    return HttpResponse('Success' + results)


