from django import forms

class ExamUploadForm(forms.Form):
    exam_name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'placeholder': 'Enter Exam Name'}))
    duration_hours = forms.IntegerField(min_value=1, initial=24, help_text="Link expiration window in hours")
    tsv_file = forms.FileField(help_text="Upload a TSV file")