from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test

#lockdown to admins
@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 0)
def index(request):
    return render(request, 'test.html')
    #template = loader.get_template('base.html')
    #return HttpResponse(template.render("Hello, world. You're at the polls index.", request))
