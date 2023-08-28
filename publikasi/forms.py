from django import forms
from django.utils import timezone, dateformat

from datetime import date
import datetime

years_to_display = range(datetime.date.today().year, datetime.date.today().year + 50)

TIME_HOUR_CHOICES = (('09:00', '09:00'), ('10:00', '10:00'), ('12:00', '12:00'), ('13:00', '13:00'), ('14:00', '14:00'), ('15:00', '15:00'), ('16:00', '16:00'), ('17:00', '17:00'), ('18:00', '18:00'), ('19:00', '19:00'), ('20:00', '20:00'))
YES_OR_NO = [(True, ''), (False, '')]


class DateInput(forms.DateInput):
	input_type = 'date'

class PublicationRequestCreateForm(forms.Form):
	program = forms.CharField(label='Judul Konten *', required=True, max_length=200, widget=forms.TextInput(attrs={'type' : 'text', 'placeholder' : 'Judul Konten', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	date_posted = forms.DateField(widget=DateInput)
	time_posted = forms.ChoiceField(label='Waktu Publikasi *', choices=TIME_HOUR_CHOICES, widget=forms.Select(attrs={'type' : 'text', 'placeholder' : '00', 'class' : 'form-choice-control', 'autocomplete' : 'off', 'id' : 'time_posted_form'}))
	is_insidental = forms.ChoiceField(label='Insidental', choices=YES_OR_NO, widget=forms.RadioSelect(attrs={'type' : 'radio', 'class' : 'form-radio'}), initial=False)
	bukti_insidental = forms.URLField(label='Link Bukti Insidental *', required=False, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : '(Hanya isi bila insidental)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	publikas = forms.URLField(label='Tautan Konten *', required=True, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : 'Tautan Konten (Google Slide)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	notes = forms.CharField(label='Catatan', required=False, widget=forms.Textarea(attrs={'type' : 'text', 'placeholder' : 'Catatan', 'class' : 'form-text-control', 'autocomplete' : 'off'}))


	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.label_suffix = ""

class AddNotesForm(forms.Form):
	notes = forms.CharField(label='', required=True, widget=forms.Textarea(attrs={'type' : 'text', 'placeholder' : 'Tambah Catatan', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
 
class PublicationRequestEditForm(forms.Form):
	id_pub_request = forms.CharField(required=False)
	program = forms.CharField(label='Judul Konten *', required=True, max_length=200, widget=forms.TextInput(attrs={'type' : 'text', 'placeholder' : 'Judul Konten', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	date_posted = forms.DateField(widget=DateInput)
	time_posted = forms.ChoiceField(label='Waktu Publikasi *', choices=TIME_HOUR_CHOICES, widget=forms.Select(attrs={'type' : 'text', 'placeholder' : '00', 'class' : 'form-choice-control', 'autocomplete' : 'off', 'id' : 'time_posted_form'}))
	is_insidental = forms.ChoiceField(label='Insidental', choices=YES_OR_NO, widget=forms.RadioSelect(attrs={'type' : 'radio', 'class' : 'form-radio'}))
	bukti_insidental = forms.URLField(label='Link Bukti Insidental *', required=False, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : '(Hanya isi bila insidental)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	publikas = forms.URLField(label='Tautan Konten *', required=True, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : 'Tautan Konten (Google Slide)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))				

	# suffix of label : ""
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.label_suffix = ""
  
class DesignLinkForm(forms.Form):
	design_link = forms.URLField(label='Link Publikasi', required=False, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : 'Link URL Publikasi (Tidak Wajib)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))	


class PreviewPublicationLinkForm(forms.Form):
	preview_link_instagram = forms.URLField(label='Preview Link IG Feed (Jika ada)', required=False, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : 'Link Preview IG Feed (Jika ada)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))
	preview_link_twitter = forms.URLField(label='Preview Link Twitter (Jika ada)', required=False, widget=forms.URLInput(attrs={'type' : 'url', 'placeholder' : 'Link Preview Twitter Feed (Jika ada)', 'class' : 'form-text-control', 'autocomplete' : 'off'}))