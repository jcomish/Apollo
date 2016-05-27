from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer
from .forms import CustomerForm
from UserProfile.models import Employee
from .models import Store


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def index(request):

    employee = Employee.objects.get(user_id=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)
    customer_list = Customer.objects.filter(store=store_name).order_by('-create_date')[:10]
    action = 'add'

    # todo: refactor all the if statements
    # todo: break out into a services file or other .py structure - getting messy
    # todo: add error handling for Notification selctions (if SMS we must have Phone)
    # todo: add update logic based on action
    if 'action' in request.GET:
        action = request.GET['action']
        if (request.GET['action'] == 'edit') and ('customer_id' in request.GET):
            # todo: restrict access to storeid from customer object
            customer = Customer.objects.get(pk=request.GET['customer_id'])
            form = CustomerForm(instance=customer)
            action = 'edit'
        else:
            form = CustomerForm(initial={'store': employee.store_id, 'user_id':request.user.id})
    else:
        form = CustomerForm(initial={'store': employee.store_id, 'user_id': request.user.id})

    context = {
        'customer_list': customer_list,
        'form': form,
        'employee': employee,
        'action' : action,
    }

    if ('customer_id' in request.GET) and (action != 'edit'):
        # todo: restrict access to storeid from customer object
        customer = Customer.objects.get(pk=request.GET['customer_id'])
        context.update({'customer':customer,})

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        customer_id = customer_form.save_and_email()
        return HttpResponseRedirect('/?customer_id=' + str(customer_id))

    return render(request, 'base.html', context=context)

# def index(request):
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
