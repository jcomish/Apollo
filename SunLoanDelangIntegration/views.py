from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Customer
from .forms import CustomerForm
from .models import CustomerPDF
from UserProfile.models import Employee
from .models import Store
from .models import Message
from .models import SentMessages
from . import services
from . import pdf


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def update(request):
    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_id = customer_form.update_and_email(request.POST.get('customer_id'))
            return HttpResponseRedirect('/?customer_id=' + str(customer_id))
        else:
            return render(request, 'base.html', {'form': customer_form})
            # todo: return to the update page load form data from user.
        
    return HttpResponseRedirect('/')


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
        contract = CustomerPDF.objects.filter(customer_id=customer.id).order_by('-create_date')[:1]
        context.update({'customer':customer,})
        context.update({'contract': contract,})

    if request.method == 'POST':
        customer_form = CustomerForm(request.POST)
        if customer_form.is_valid():
            customer_id = customer_form.save_and_notify()
        else:
            return render(request, 'base.html', {'form': customer_form})
        return HttpResponseRedirect('/?customer_id=' + str(customer_id))

    return render(request, 'base.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def code(request):
    employee = Employee.objects.get(user_id=request.user.id)

    context = {
        'employee': employee,
    }

    if 'customer_id' in request.GET:
        # todo: restrict access to storeid from customer object
        try:
            customer = Customer.objects.get(pk=request.GET['customer_id'])
            services.send_sms_welcome_message(customer)
        except Exception as e:
            customer = e

        context.update({'customer': customer,})

        return HttpResponseRedirect('/?customer_id=' + str(customer.id))

    # todo: redirect to error page - contract could not be generated
    return render(request, 'base.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def contract(request):
    employee = Employee.objects.get(user_id=request.user.id)
    notifications = Message.objects.all().exclude(name='Welcome')

    context = {
        'employee': employee,
        'notifications': notifications,
    }

    if 'customer_id' in request.GET:
        # todo: restrict access to storeid from customer object
        try:
            customer = Customer.objects.get(pk=request.GET['customer_id'])
            pdf.generate_doc(customer)
        except Exception as e:
            customer = e

        context.update({'customer': customer,})

        return HttpResponseRedirect('/?customer_id=' + str(customer.id))

    # todo: redirect to error page - contract could not be generated
    return render(request, 'base.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def search(request):

    employee = Employee.objects.get(user_id=request.user.id)
    store_name = Store.objects.get(pk=employee.store_id)
    action = 'add'

    if request.method == 'POST':

        search_string = request.POST.get('search')
        form = CustomerForm(initial={'store': employee.store_id, 'user_id': request.user.id})
        field = request.POST.get('criteria')
        customer_list = Customer.objects.filter(**{'store':store_name, field + '__icontains':search_string})\
            .order_by('-create_date')[:10]

        context = {
            'customer_list': customer_list,
            'employee': employee,
            'action': action,
            'form': form,
        }

        return render(request, 'base.html', context=context)

    else:
        return HttpResponseRedirect('/')


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def view(request):
    employee = Employee.objects.get(user_id=request.user.id)
    notifications = Message.objects.all().exclude(name='Welcome')

    context = {
        'employee': employee,
        'notifications': notifications,
    }

    if 'customer_id' in request.GET:
        # todo: restrict access to storeid from customer object
        try:
            customer = Customer.objects.get(pk=request.GET['customer_id'])
        except Exception as e:
            customer = e
        context.update({'customer': customer,})

    if request.method == 'POST':
        customer_id = request.POST.get('cust_id')
        message_id = request.POST.get('message')
        services.send_message(customer_id, message_id)

        return HttpResponseRedirect('/?customer_id=' + str(customer_id))

    return render(request, 'base_view.html', context=context)


@login_required
@user_passes_test(lambda u: u.groups.filter(name='employee').count() == 1)
def history(request):
    employee = Employee.objects.get(user_id=request.user.id)
    notifications = Message.objects.all().exclude(name='Welcome')
    context = {
        'employee': employee,
        'notifications': notifications,
    }

    if 'customer_id' in request.GET:
        # todo: restrict access to storeid from customer object
        try:
            customer = Customer.objects.get(pk=request.GET['customer_id'])
            history_list = SentMessages.objects.filter(customer=customer).exclude(delang_message_id=0).order_by('-date_sent')[:10]
        except Exception as e:
            customer = e
            history_list = ''
        context.update({'customer': customer, 'history_list' : history_list})

    if request.method == 'POST':
        customer_id = request.POST.get('cust_id')
        message_id = request.POST.get('message')
        services.send_message(customer_id, message_id)

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

