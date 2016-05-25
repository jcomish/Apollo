from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer
from .forms import CustomerForm
from UserProfile.models import Employee
from .models import Store

@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def index(request):
    employee = Employee.objects.get(pk=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)
    customer_list = Customer.objects.filter(store=store_name).order_by('-create_date')[:10]
    form = CustomerForm(initial={'store': employee.store_id})

    context = {
        'customer_list': customer_list,
        'form': form,
        'employee': employee,}
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        #customer_form.store = employee.store_id
        customer_form.save_and_email()


    return render(request, 'base.html', context=context)





#def index(request):
    # customer_list = Customer.objects.order_by('create_date')[:10]
    # #output = ', '.join([q.question_text for q in latest_question_list])
    #
    # if request.method == 'POST':
    #     # create a form instance and populate it with data from the request:
    #     form = CustomerForm(request.POST)
    #     # check whether it's valid:
    #     if form.is_valid():
    #
    #         myCust = Customer()
    #         myCust.account_id = form.account_id
    #         myCust.first_name = form.first_name
    #         myCust.last_name = form.last_name
    #         myCust.phone_number = form.phone_number
    #         myCust.email_address = form.email
    #         myCust.save()
    #
    #         return HttpResponseRedirect('/')
    #
    # else:
    #     form = CustomerForm()
    #
    # context = {
    #     'customer_list': customer_list,
    #     'form': form,
    # }
    #
    # return render(request, 'base.html', context=context)
