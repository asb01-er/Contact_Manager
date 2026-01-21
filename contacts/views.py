from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from django.http import HttpResponse
from .forms import ContactForm, SignUpForm
from .models import Contact

# Sign Up
def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# Dashboard / Contacts
@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {'contacts': contacts, 'form': ContactForm()}
    return render(request, 'contacts.html', context)

# HTMX Search
@login_required
def search_contacts(request):
    query = request.GET.get('search','')
    contacts = request.user.contacts.filter(Q(name__icontains=query)|Q(email__icontains=query))
    return render(request, 'partials/contact-list.html', {'contacts': contacts})

# Add Contact
@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES, initial={'user': request.user})
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()
        response = render(request, 'partials/contact-row.html', {'contact': contact})
        response['HX-Trigger'] = 'success'
        return response
    else:
        response = render(request, 'partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response

# Delete Contact
@login_required
@require_http_methods(['POST'])
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'contact-deleted'
    response['HX-Redirect'] = '/'
    return response
