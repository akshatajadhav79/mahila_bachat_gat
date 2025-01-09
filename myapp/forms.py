# forms.py
from django import forms
from .models import ViewerSession

class ViewerSessionForm(forms.ModelForm):
    class Meta:
        model = ViewerSession
        fields = ('session_id',)

    def __init__(self, *args, **kwargs):
        super(ViewerSessionForm, self).__init__(*args, **kwargs)
        self.fields['session_id'].widget.attrs['placeholder'] = 'Enter unique session ID'

    def clean_session_id(self):
        session_id = self.cleaned_data['session_id']
        if ViewerSession.objects.filter(session_id=session_id).exists():
            raise forms.ValidationError('Session ID already exists')
        return session_id