from django.shortcuts import render,redirect
from Store.models import *
from Store.forms import *
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.db.models import Q
from django.contrib.auth.decorators import login_required
import razorpay
from django.conf import settings
from paypal.standard.forms import PayPalEncryptedPaymentsForm
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
import stripe
import time
from django.http import HttpResponse
import random




def index(request):
    orders = UserOrder.objects.filter(user=request.user)
    context = { 'order':orders }
    return render(request, "store/order/index.html", context)