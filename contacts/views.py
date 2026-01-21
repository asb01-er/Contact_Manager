from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from contacts.forms import ContactForm
from contacts.models import Contact

@login_required
def index(request):
    contacts = request.user.contacts.all().order_by('-created_at')
    context = {
        'contacts': contacts,
        'form': ContactForm()
    }
    return render(request, 'contacts.html', context)

@login_required
def search_contacts(request):
    query = request.GET.get('search', '').strip()
    contacts = request.user.contacts.filter(
        Q(name__icontains=query) | Q(email__icontains=query)
    ).order_by('-created_at')

    return render(request, 'partials/contact-list.html', {'contacts': contacts})



@login_required
@require_http_methods(['POST'])
def create_contact(request):
    form = ContactForm(request.POST, request.FILES)
    if form.is_valid():
        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()

        # Return the new contact row partial
        response = render(request, 'partials/contact-row.html', {'contact': contact})
        response['HX-Trigger'] = 'contact-added'
        return response
    else:
        # Return the modal with errors to swap outerHTML
        response = render(request, 'partials/add-contact-modal.html', {'form': form})
        response['HX-Retarget'] = '#contact_modal'
        response['HX-Reswap'] = 'outerHTML'
        response['HX-Trigger-After-Settle'] = 'fail'
        return response

    

@login_required
@require_http_methods(['POST'])
def delete_contact(request, pk):
    contact = get_object_or_404(Contact, pk=pk, user=request.user)
    contact.delete()
    response = HttpResponse(status=204)
    response['HX-Trigger'] = 'contact-deleted'
    response['HX-Redirect'] = '/'
    return response
