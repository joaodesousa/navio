from django import forms
from .models import Clients, Trip, Hotels, Flight, AirCompany, Airport
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.forms import TextInput,EmailInput,PasswordInput, ModelForm, ModelChoiceField
from django.contrib.auth.models import User, Group
from django.core.validators import RegexValidator
from django.views.generic.edit import UpdateView


# Novo Cliente
# Cria utilizador na criação de cliente

class SignUpForm(UserCreationForm):
    address = forms.CharField(max_length=200, label="Morada", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Av. da Liberdade, 170',}))
    nif = forms.CharField(max_length=9, label="NIF", validators=[RegexValidator(r'^\d{1,10}$')], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Deve conter 9 dígitos',}))
    mobile = forms.CharField(max_length=9, label="Telemóvel", validators=[RegexValidator(r'^\d{1,10}$')], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Deve conter 9 dígitos',}))
    city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Lisboa',}))
    postal = forms.CharField(max_length=8, validators=[RegexValidator(r'^\d{4}(-\d{3})?$')], widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder':'0000-000',}))

    def clean_nif(self): 
        nif = self.cleaned_data['nif']; 
        if Clients.objects.filter(nif=nif).exists(): raise forms.ValidationError("NIF já existente.")
        return nif

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'address', 'nif', 'mobile', 'city', 'postal')
    
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilizador do Cliente'})
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['first_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = EmailInput(attrs={'class': 'form-control', 'placeholder': 'nome@dominio.com'})

    def save(self):
       user = super().save()
       group = Group.objects.get(name='Clients')
       user.groups.add(group)
       cleaned_data = self.cleaned_data
       client = Clients.objects.create(
           user=user,
           address=cleaned_data.get('address'),
           city=cleaned_data.get('city'),
           postal=cleaned_data.get('postal'),
           nif=cleaned_data.get('nif'),
           mobile=cleaned_data.get('mobile')
       )
       return user

# Actualizar cliente

class UpdateClient(ModelForm):
    address = forms.CharField(max_length=200, label="Morada", widget=forms.TextInput(attrs={'class': 'form-control'}))
    nif = forms.CharField(max_length=9, label="NIF", validators=[RegexValidator(r'^\d{1,10}$')], widget=forms.TextInput(attrs={'class': 'form-control'}))
    mobile = forms.CharField(max_length=9, label="Telemóvel", validators=[RegexValidator(r'^\d{1,10}$')], widget=forms.TextInput(attrs={'class': 'form-control'}))
    city = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
    postal = forms.CharField(max_length=8, validators=[RegexValidator(r'^\d{4}(-\d{3})?$')], widget=forms.TextInput(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super(UpdateClient, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = EmailInput(attrs={'class': 'form-control'})

    class Meta:
        model = User
        fields = ('email','first_name','last_name', 'address', 'nif', 'mobile', 'city', 'postal')

# Nova Viagem

class NewTrip(ModelForm):

    def __init__(self, *args, **kwargs):
        super(NewTrip, self).__init__(*args, **kwargs)
        self.fields['trip_id'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['destination'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['client'].queryset = Clients.objects.all()

    class Meta:
        model = Trip
        fields = ('trip_id', 'destination', 'client', 'out_flight', 'hotel', 'in_flight')

# Actualizar Viagem

class UpdateTrip(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateTrip, self).__init__(*args, **kwargs)
        self.fields['trip_id'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['destination'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['client'].queryset = Clients.objects.all()


    class Meta:
        model = Trip
        fields = ('trip_id', 'destination', 'client', 'out_flight', 'hotel', 'in_flight')

# Novo Hotel

class NewHotel(ModelForm):

    class Meta:
        model = Hotels
        fields = ('hotel_name', 'address', 'city', 'mobile')


    def __init__(self, *args, **kwargs):
        super(NewHotel, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['address'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['city'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['mobile'].widget = TextInput(attrs={'class': 'form-control', 'maxlength': '9'})

# Actualizar Hotel

class UpdateHotel(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateHotel, self).__init__(*args, **kwargs)
        self.fields['hotel_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['address'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['city'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['mobile'].widget = TextInput(attrs={'class': 'form-control', 'maxlength': '9'})


    class Meta:
        model = Hotels
        fields = ('hotel_name', 'address', 'city', 'mobile')

# Novo Voo

class NewFlight(ModelForm):

    class Meta:
        model = Flight
        fields = ('date', 'flight_id', 'company', 'airport')


    def __init__(self, *args, **kwargs):
        super(NewFlight, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateTimeInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'})
        self.fields['flight_id'].widget = TextInput(attrs={'class': 'form-control'})
        
# Actualizar Voo

class UpdateFlight(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateFlight, self).__init__(*args, **kwargs)
        self.fields['date'].widget = forms.DateTimeInput(attrs={'class': 'form-control', 'data-target': '#datetimepicker1'})
        self.fields['flight_id'].widget = TextInput(attrs={'class': 'form-control'})


    class Meta:
        model = Flight
        fields = ('date', 'flight_id', 'company', 'airport')

# Nova Companhia

class NewCompany(ModelForm):

    class Meta:
        model = AirCompany
        fields = ('company_name',)


    def __init__(self, *args, **kwargs):
        super(NewCompany, self).__init__(*args, **kwargs)
        self.fields['company_name'].widget = TextInput(attrs={'class': 'form-control'})

# Novo Aeroporto

class NewAirport(ModelForm):

    class Meta:
        model = Airport
        fields = ('airport_name', 'airport_city', 'airport_country' )


    def __init__(self, *args, **kwargs):
        super(NewAirport, self).__init__(*args, **kwargs)
        self.fields['airport_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['airport_city'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['airport_country'].widget = TextInput(attrs={'class': 'form-control'})



class UpdateAirport(ModelForm):

    def __init__(self, *args, **kwargs):
        super(UpdateAirport, self).__init__(*args, **kwargs)
        self.fields['airport_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['airport_city'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['airport_country'].widget = TextInput(attrs={'class': 'form-control'})


    class Meta:
        model = Airport
        fields = ('airport_name', 'airport_city', 'airport_country' )




        # ADMIN
        # Criar Funcionário

class NewEmployee(UserCreationForm):
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')

    class Meta:
        model = User
        fields = ('username', 'password1', 'password2', 'first_name', 'last_name', 'email')
    
    def __init__(self, *args, **kwargs):
        super(NewEmployee, self).__init__(*args, **kwargs)
        self.fields['username'].widget = TextInput(attrs={'class': 'form-control', 'placeholder': 'Utilizador do Cliente'})
        self.fields['password1'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['password2'].widget = PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Mínimo 8 caracteres'})
        self.fields['first_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['last_name'].widget = TextInput(attrs={'class': 'form-control'})
        self.fields['email'].widget = EmailInput(attrs={'class': 'form-control', 'placeholder': 'nome@dominio.com'})

    def save(self):
       user = super().save()
       group = Group.objects.get(name='Employees')
       user.groups.add(group)
       cleaned_data = self.cleaned_data
       User.objects.create(
           first_name=cleaned_data.get('first_name'),
           last_name=cleaned_data.get('last_name'),
           email=cleaned_data.get('email')
       )
       return user