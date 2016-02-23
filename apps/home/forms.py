import json

from django import forms

from instapush.libs import gcm


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
