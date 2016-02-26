from django.conf import settings
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy

from django.views.generic.base import TemplateView
from django.views.generic.edit import FormView

from .forms import APNSForm, GCMForm


class Home(TemplateView):

    template_name = 'home/index.html'


class APNSTester(FormView):

    template_name = 'apns_tester.html'
    form_class = APNSForm
    success_url = reverse_lazy('home:apns')

    def form_valid(self, form, *args, **kwargs):

        try:
            x = form.send_message()
            print x
            messages.success(self.request, 'Message(s) sent.')
        except Exception as err:
            messages.error(self.request, str(err))

        return super(APNSTester, self).form_valid(form, *args, **kwargs)


class GCMTester(FormView):

    template_name = 'gcm_tester.html'
    form_class = GCMForm
    success_url = reverse_lazy('home:gcm')

    def form_valid(self, form, *args, **kwargs):
        """
        Called if the form validation passes.
        """

        result = form.send_message()
        try:
            result = form.send_message()
            if result.get('failure'):
                error = result.get('results')[0]['error']
                messages.error(self.request, error)
            elif result.get('success'):
                messages.success(self.request, 'Message(s) sent.')
        except Exception as err:
            messages.error(self.request, str(err))

        return super(GCMTester, self).form_valid(form, *args, **kwargs)
