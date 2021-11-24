from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from agents.models import Agency,Agent, MailProvider, AgentMailbox

class AgencyAdmin(admin.ModelAdmin):
    list_display = ('__unicode__', 'branch', 'telephone', 'email', 'address','city', 'sitelink',)
    search_fields = ['name']
    ordering = ('name',)
admin.site.register(Agency, AgencyAdmin)


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Agent
        fields = ('email', 'forename', 'surname', 'mobile', 'photo', 'agency')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """
    password = ReadOnlyPasswordHashField()
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput,required=False)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput,required=False)

    class Meta:
        model = Agent
        fields = ('email', 'password', 'forename', 'surname', 'mobile', 'photo', 'agency', 'is_active', 'is_admin')

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super(UserChangeForm, self).save(commit=False)
        newpass = self.cleaned_data["password1"]
        if newpass and newpass != '':
            user.set_password(newpass)
        else:
            user.password = self.initial["password"]
        if commit:
            user.save()
        return user



class AgentAdmin(UserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'forename', 'surname', 'mobile', 'photo', 'agency', 'public', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password', 'password1', 'password2')}),
        ('Personal info', {'fields': ('forename', 'surname', 'mobile', 'photo', 'agency', 'role',)}),
        ('Permissions', {'fields': ('public', 'is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'forename', 'surname', 'mobile', 'photo', 'agency', 'role', 'password1', 'password2')}
        ),
    )
    search_fields = ('email', 'forename', 'surname')
    ordering = ('surname',)
    filter_horizontal = ()

# Now register the new UserAdmin...
admin.site.register(Agent, AgentAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)


#class OutsideAgentAdmin(admin.ModelAdmin):
#    list_display = ('__unicode__', 'mobile', 'email', 'agency',)
#admin.site.register(OutsideAgent, OutsideAgentAdmin)

class MailProviderAdmin(admin.ModelAdmin):
    list_display = ('name',)
admin.site.register(MailProvider, MailProviderAdmin)

class AgentMailboxAdmin(admin.ModelAdmin):
    list_display = ('agent', 'email',)
admin.site.register(AgentMailbox, AgentMailboxAdmin)
