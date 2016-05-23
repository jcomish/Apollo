from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customers

@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 0)

def index(request):
    customer_list = Customers.objects.order_by('create_date')[:10]
    #output = ', '.join([q.question_text for q in latest_question_list])
    context = {
        'customer_list': customer_list,
    }

    return render(request, 'base.html', context)
    #template = loader.get_template('base.html')
    #return HttpResponse(template.render("Hello, world. You're at the polls index.", request))


