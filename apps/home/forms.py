import os
import json

from django import forms

from instapush.libs import gcm, apns


class APNSForm(forms.Form):

    pem_certificate = forms.FileField()
    device_tokens = forms.CharField(widget=forms.Textarea)
    apns_message = forms.CharField(widget=forms.Textarea, required=False)
    apns_data = forms.CharField(widget=forms.Textarea, required=False)
    use_json = forms.BooleanField(required=False)

    def clean_pem_certificate(self):

        f = self.cleaned_data.get('pem_certificate')
        content = f.readlines()
        tfile = open("/tmp/%s" % f.name, 'w')
        tfile.writelines(content)
        filename = os.path.abspath(tfile.name)
        tfile.close()

        return filename

    def send_message(self, *args, **kwargs):
        data = self.cleaned_data
        pem_cert = data.get('pem_certificate')
        message = data.get('apns_message')
        ids = data.get('device_tokens').split(",")
        json_data = data.get('apns_data')
        message_obj = json.loads(json_data) if json_data else {"message": message}

        return apns.apns_send_bulk_message(ids, message_obj, certfile=os.path.abspath(pem_cert))


class GCMForm(forms.Form):

    api_key = forms.CharField()
    device_tokens = forms.CharField(widget=forms.Textarea)
    gcm_message = forms.CharField(widget=forms.Textarea, required=False)
    gcm_data = forms.CharField(widget=forms.Textarea, required=False)
    use_json = forms.BooleanField(required=False)

    def clean_gcm_data(self):
        gcm_data = self.cleaned_data.get('gcm_data')
        if gcm_data:
            try:
                json.loads(gcm_data)
            except Exception:
                raise forms.ValidationError(
                        'Data you entered does not seem to be valid json.')
        return gcm_data

    def send_message(self, *args, **kwargs):
        data = self.cleaned_data
        api_key = data.get('api_key')
        message = data.get('gcm_message')
        ids = data.get('device_tokens').split(",")
        json_data = data.get('gcm_data')
        message_obj = json.loads(json_data) if json_data else {"message": message}

        return gcm.gcm_send_bulk_message(ids, message_obj, api_key=api_key)
