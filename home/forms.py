
from django import forms

class SearchPublicationRequest(forms.Form):
	id_pub_request = forms.CharField(label='', required=True, max_length=50, widget=forms.TextInput(attrs={'type' : 'text', 'placeholder' : 'Temukan Pesanan Publikasi (Ex. "publikasi-mulmed-bem_ui-1")', 'class' : 'form-text-control', 'autocomplete' : 'off'}))