from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import UserProfile
# Create your views here.


from .forms import UserProfile

@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 0)
def index(request):
    form = UserProfile()
    context = {
            'form': form,}
    if request.method == 'POST':
        user_form = UserProfile(request.POST)
        user_form.save()

    return render(request, 'base.html', context=context)