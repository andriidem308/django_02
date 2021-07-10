"""Account forms file."""
from account.models import Avatar, Profile, User
from account.tasks import send_activation_link_mail
from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField, UserChangeForm, UsernameField
from django.db import transaction
from django.utils.text import slugify


class UserRegisterForm(forms.ModelForm):
    """User registration Form."""

    password = forms.CharField(widget=forms.PasswordInput)
    confirmation_password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        """UserRegisterForm Meta."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password', 'confirmation_password')

    def clean(self):
        """Clean information."""
        clean_data: dict = super().clean()
        """Here is location of our form (breakpoint for checking in next line)."""
        if clean_data['password'] != clean_data['confirmation_password']:
            self.add_error('password', 'Password mismatch!')
            # raise forms.ValidationError("Password mismatch!")
            """Alternatively error in forms not in fields."""

        if not clean_data['username']:
            clean_data['username'] = slugify(clean_data['first_name'])
        return clean_data

    def clean_email(self):
        """Clean email."""
        email = self.cleaned_data['email']
        if User.objects.filter(email__iexact=email).exists():
            self.add_error('email', 'Email already exists!')
        return email

    @transaction.atomic
    def save(self, commit=True):
        """Save and send mail."""
        instance: User = super().save(commit=False)
        instance.is_active = False
        instance.set_password(self.cleaned_data["password"])
        instance.save()

        send_activation_link_mail.apply_async(instance.id)
        return instance


class AvatarForm(forms.ModelForm):
    """Avatar Form."""

    class Meta:
        """Avatar Form Meta."""

        model = Avatar
        fields = ("file_path",)

    def __init__(self, request, *args, **kwargs):
        """Init Avatar Form."""
        self.request = request
        super().__init__(*args, **kwargs)

    def save(self, commit=False):
        """Save Avatar Form."""
        instance = super().save(commit=False)
        instance.user = self.request.user
        instance.save()
        return instance


class ProfileForm(UserChangeForm):
    """Profile Form."""

    email = forms.EmailField(widget=forms.EmailInput(attrs={"class": 'form-control', "placeholder": "Ваш имейл"}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": 'form-control'}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"class": 'form-control'}))

    password = ReadOnlyPasswordHashField(
        label='Password',
        help_text=(
            'Raw passwords are not stored, so there is no way to see this '
            'user’s password, but you can change the password using '
            '<a href="{}">this form</a>.'
        ),
    )

    class Meta:
        """Profile Form Meta."""

        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password',)
        field_classes = {'username': UsernameField}

    def __init__(self, *args, **kwargs):
        """Init Profile Form."""
        super().__init__(*args, **kwargs)
        password = self.fields.get('password')
        if password:
            password.help_text = password.help_text.format('../password/')
        user_permissions = self.fields.get('user_permissions')
        if user_permissions:
            user_permissions.queryset = user_permissions.queryset.select_related('content_type')

    def clean_password(self):
        """Clean password from Profile Form."""
        return self.initial.get('password')

    def save(self, commit=False):
        """Save Profile Form."""
        instance = super().save(commit=False)
        instance.user = self.request.user
        instance.save()
        return instance


class ProfilePageForm(forms.ModelForm):
    """Create Profile for User using Profile model."""

    class Meta:
        """Meta class for ProfilePageForm."""

        model = Profile
        fields = ('bio', 'profile_picture', 'website_url', 'facebook_url', 'instagram_url', 'twitter_url')
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control'}),
            # 'profile_picture' : forms.TextInput(attrs={'class':'form-control'}),
            'website_url': forms.TextInput(attrs={'class': 'form-control'}),
            'facebook_url': forms.TextInput(attrs={'class': 'form-control'}),
            'twitter_url': forms.TextInput(attrs={'class': 'form-control'}),
            'instagram_url': forms.TextInput(attrs={'class': 'form-control'}),

        }
