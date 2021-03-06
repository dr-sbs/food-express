from django import forms

from location.models import DeliveryLocation

class BuyNowForm(forms.Form):
    delivery_location = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}))
    quantity = forms.IntegerField(
            min_value=1,
            max_value=10,
            initial=1,
            required=False,
            widget=forms.TextInput(attrs={'class':'form-control'})
        )
    
    def __init__(self, request, *args, **kwargs):
         super(forms.Form, self).__init__(*args, **kwargs)
         self.fields['delivery_location'].choices = [(l.id, l.title) for l in DeliveryLocation.objects.filter(customer=request.user.customer)]
