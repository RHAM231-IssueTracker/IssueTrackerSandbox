from django.shortcuts import render
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .forms import ContactForm
from .models import ContactText, ContactHeader, ContactImage
from base_pages.models import (ContactButton, LinkButton)


# Handles the backend of the contact form. This reads in the data
# from the form and then sends it to the specified email addresses.
# Form fields are pulled from forms.py in the contact app.
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            # Let's create a context for rendering html in an email
            # This allows us to pull variables from our form and input
            # them in an email in any format we want.
            email_context = {
                'name': form.cleaned_data['name'],
                'email': form.cleaned_data['sender'],
                'message': form.cleaned_data['message'],
            }
            # Pass context into the template and convert it to be email friendly.
            # We use strip_tags as a backup to render the template in non-html
            # capable browsers.
            html_content = render_to_string('contact/contact_email.html', email_context)
            plain_message = strip_tags(html_content)
            from_email = form.cleaned_data['sender']
            cc_myself = form.cleaned_data['cc_myself']
            recipients = ['recipients@email.com']
            # If the the checkbox is checked, add the form user to the list of email
            # recipients.
            if cc_myself:
                recipients.append(from_email)
            # Call django's send mail function and pass everything we just created
            send_mail(subject, plain_message, from_email, recipients,
                      fail_silently=False, html_message=html_content)

            # Build a context from the database to create our contact success page
            context = {
                'contact_headers': ContactHeader.objects.all().order_by('index_key'),
                'contact_images': ContactImage.objects.all().order_by('index_key'),
                'home_button': LinkButton.objects.get(name='Home Button'),
                'email': ContactButton.objects.get(
                    header='Email'),
                'title': 'Contact',
                'form': form,
            }

            # If the form was submitted successfully, render the success page using
            # context above.
            return render(request, 'contact/contact_form_success.html', context)

    # Otherwise, set form to equal the empty form. Django handles error messages automatically.
    else:
        form = ContactForm()

    # Build a context for the contact page. and pass it to render.
    context = {
        # Pull all our ContactButtons from the database except the email button.
        'page_buttons': ContactButton.objects.exclude(header='Email').order_by('page_order'),
        # Get just the Contact Form Submit Button from LinkButtons.
        'submit_button': LinkButton.objects.get(name='Contact Form Submit Button'),
        'contact_text': ContactText.objects.all().order_by('index_key'),
        'contact_headers': ContactHeader.objects.all().order_by('index_key'),
        'email': ContactButton.objects.get(
            header='Email'),
        'title': 'Contact',
        'form': form,
    }
    return render(request, 'contact/contact_form.html', context)
    
