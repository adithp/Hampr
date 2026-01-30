from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Ticket
from .forms import TicketForm

class ContactView(CreateView):
    model = Ticket
    form_class = TicketForm
    template_name = 'ticket/contact.html'
    success_url = reverse_lazy('ticket:contact') 

    def form_valid(self, form):
        messages.success(self.request, "Your ticket has been submitted successfully! We will get back to you soon.")
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, "There was an error submitting your ticket. Please check the form.")
        return super().form_invalid(form)

