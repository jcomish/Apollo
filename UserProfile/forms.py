from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserChangeForm
from .models import Employee


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        exclude = ('',)


class UserForm(UserChangeForm):
    class Meta:
        model = User
        exclude = ('',)

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        student_kwargs = kwargs.copy()
        if 'instance' in kwargs:
            self.student = kwargs['instance'].student
            student_kwargs['instance'] = self.student
        self.student_form = EmployeeForm(*args, **student_kwargs)
        self.fields.update(self.student_form.fields)
        self.initial.update(self.student_form.initial)

        # define fields order if needed
        self.fields.keyOrder = (
            'last_name',
            'first_name',
            # etc
            'address',
        )

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        self.errors.update(self.student_form.errors)
        return cleaned_data

    def save(self, commit=True):
        self.student_form.save(commit)
        return super(UserForm, self).save(commit)

















# from django import forms
# from django.forms import ModelForm
# from .models import UserProfile
#
#
# class UserProfileForm(forms.ModelForm):
#     class Meta:
#         model = UserProfile
#         exclude = ()
#     #   todo: build form for userprofile modification


