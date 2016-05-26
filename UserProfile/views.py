from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .forms import UserForm


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 0)
def index(request):
    form = UserForm()
    context = {
            'form': form,}
    if request.method == 'POST':
        user_form = UserForm(request.POST)
        user_form.save()

    return render(request, 'user.html', context=context)