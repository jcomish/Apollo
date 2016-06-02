from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer
from .forms import CustomerForm
from UserProfile.models import Employee
from .models import Store


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def update(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        customer_id = customer_form.update_and_email(request.POST.get('customer_id'))
        return HttpResponseRedirect('/?customer_id=' + str(customer_id))

    return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def index(request):

    employee = Employee.objects.get(user_id=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)
    customer_list = Customer.objects.filter(store=store_name).order_by('-create_date')[:10]
    action = 'add'
    verification_code = 'none'

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


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def search(request):

    employee = Employee.objects.get(user_id=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)
    action = 'add'
    verification_code = 'none'

    if request.method == 'POST':

        search = request.POST.get('search')
        field = request.POST.get('criteria')
        customer_list = Customer.objects.filter(**{'store':store_name, field + '__icontains':search})\
            .order_by('-create_date')[:10]

        context = {
            'customer_list': customer_list,
            'employee': employee,
            'action': action,
        }

        return render(request, 'base.html', context=context)

    else:
        return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def view(request):
    employee = Employee.objects.get(user_id=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)

    context = {
        'employee': employee,
    }

    if 'customer_id' in request.GET:
        # todo: restrict access to storeid from customer object
        try:
            customer = Customer.objects.get(pk=request.GET['customer_id'])
        except Exception as e:
            customer = e
        context.update({'customer': customer,})

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        customer_id = customer_form.save_and_email()
        return HttpResponseRedirect('/?customer_id=' + str(customer_id))

    return render(request, 'base_view.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def verify(request):
    employee = Employee.objects.get(user_id=request.user.id)
    # store_name = Store.objects.get(pk=employee.store_id)
    code = request.POST.get('code')
    is_validated = ''

    if request.method == 'POST':
        if 'customer_id' in request.GET:
            # todo: restrict access to customer based on storeid from customer object and employee storeid
            # todo: assign color codes to customer status
            customer_id = request.GET['customer_id']
            try:
                customer = Customer.objects.get(pk=customer_id)
                # todo: check to make sure code is numeric or else this is going ot blow up
                if int(code) == customer.verification_code:
                    Customer.objects.filter(pk=customer_id).update(status=3)
                    is_validated = 'Success'
                else:
                    is_validated = 'Invalid Code. Try Again'

            except Exception as e:
                customer = e

            return HttpResponseRedirect('/?customer_id=' + str(customer_id) + "&validated=" + is_validated)

    return HttpResponseRedirect('/')

