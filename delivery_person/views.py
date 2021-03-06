from django import forms
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages

from accounts.forms import RegistrationForm
from orders.models import OrderItem, Order
from orders.tasks import send_invoice
from delivery_person.models import DeliveryPerson, OrdersDesignation
from delivery_person.decorators import delivery_person_required
from delivery_person.forms import DeliveryPersonProfileForm
from orders.forms import OrderDesignateForm


@login_required
@staff_member_required
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        profile_form = DeliveryPersonProfileForm(data=request.POST, files=request.FILES)
        if form.is_valid() and profile_form.is_valid():
            new_user = form.save(commit=False)
            new_user.is_delivery_person = True
            new_user.save()
            user_profile = profile_form.save(commit=False)
            user_profile.user = new_user
            user_profile.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account was created for {username}!')
            return redirect('admin:delivery_person_registerdeliveryuser_changelist')
    else:
        form = RegistrationForm()
        profile_form = DeliveryPersonProfileForm()
    
    context = {
        'form': form,
        'profile_form': profile_form,
        'title': 'Register Delivery Person',
    }

    return render(request, 'delivery_person/register.html', context)


@login_required
@delivery_person_required
def home_view(request):
    order_designations = OrdersDesignation.objects.filter(delivery_person=request.user.delivery_person).order_by('order__complete')
    context = {}
    for order_designation in order_designations:
        context[order_designation.order] = OrderItem.objects.filter(order=order_designation.order)
    return render(request, 'delivery_person/home.html', {'context': context})


@login_required
@delivery_person_required
def mark_order_as_complete(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if request.user.delivery_person == order.designation.delivery_person:
        order.complete = True
        order.save()
        messages.success(request, 'Successfully completed order!')
        message = f"""Invoice for your purchase is attached in the pdf file.Your purchase is completed sucessfully.\n
        Your purchase was delivered by: {request.user.username}"""
        send_invoice.delay(order.id, message)
    else:
        messages.error(request, 'You cannot complete someone else\'s order!')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
@delivery_person_required
def mark_order_as_incomplete(request, order_id):
    order = Order.objects.filter(id=order_id).first()
    if request.user.delivery_person == order.designation.delivery_person:
        order.complete = False
        order.save()
        messages.success(request, 'Successfully made order incomplete!')
        message = f"""Your order was accidentently marked as complete. Sorry for the inconvinence. You would soon get our delivery person on your door"""
        send_invoice.delay(order.id, message)
    else:
        messages.error(request, 'You cannot make someone else\'s order incomplete!')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))


@login_required
@delivery_person_required
def delivery_person_profile_update(request):
    if request.method == 'GET':
        form = DeliveryPersonProfileForm(instance=request.user.delivery_person)
    else:
        form = DeliveryPersonProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=request.user.delivery_person
        )
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile successfully updated!')
            return redirect('delivery_person:profile_update')
    context = {
        'form': form,
    }
    return render(
        request,
        'delivery_person/profile_update.html',
        context
    )


@login_required
@delivery_person_required
def delivery_person_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if not request.user.delivery_person == order.designation.delivery_person:
        messages.error(request, 'You are not designated to view the order')
        return redirect('delivery_person:home')
    paid = (not order.payment_by_cash) or order.complete

    restaurants_location = []
    for item in order.items.all():
        restaurants_location.append(item.food.restaurant.location)
    
    restaurants_location = list(set(restaurants_location))

    return render(request,
        'delivery_person/order_detail.html',
        {
            'order': order,
            'paid': paid,
            'restaurants_location': restaurants_location,
        })


@login_required
@staff_member_required
@require_POST
def designate_order_to_delivery_person(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    form = OrderDesignateForm(data=request.POST)
    if not order.verified:
        messages.error(request, 'You cannot designate delivery person for unverified order.')
    elif form.is_valid():
        cd = form.cleaned_data
        delivery_person = DeliveryPerson.objects.get(id=cd['delivery_person'])
        OrdersDesignation.objects.create(order=order, delivery_person=delivery_person)
        messages.success(request, 'Delivery person successfully designated.')
    else:
        messages.error(request, 'Error in designating delivery person!')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))