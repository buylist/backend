from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from mainapp.models import Buyer, ItemInChecklist, Item, Category, Checklist


# Register your models here.


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = Buyer
        fields = ('email', 'username')

    def clean_password2(self):
        """

        :return:
        """
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        """

        :param commit:
        :return:
        """
        # Save the provided password in hashed format
        user = super().save(commit=False)
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

    class Meta:
        model = Buyer
        fields = ('username', 'email', 'password', 'is_active', 'is_admin')

    def clean_password(self):
        """

        :return:
        """
        # Regardless of what the user provides, return the initial value.
        # This is done here, rather than on the field, because the
        # field does not have access to the initial value
        return self.initial["password"]


class ItemInline(admin.TabularInline):
    model = Item
    # fieldsets = (
    #     (None, {'fields': ('pk', 'name', 'buyer')}),
    # )


class CategoryAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name', 'color', 'created', 'modified']
    list_filter = ['name', 'color', 'modified']
    search_fields = ['name']
    fieldsets = (
        (None, {
            'fields': (('name', 'color',),)
        }
         ),
    )
    filter_horizontal = ()

    inlines = [ItemInline, ]


class ItemInCheckListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'checklist_id', 'quantity', 'item_id', 'modified', 'deleted', 'value']
    list_filter = ['checklist_id', 'modified', 'modified', 'deleted']
    search_fields = ['checklist_id']


class ItemsChangeForm(admin.ModelAdmin):
    list_display = ['pk', 'buyer', 'name', 'category', 'created', 'modified']
    list_filter = ['category', 'created', 'modified']
    search_fields = ['name']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'is_admin')
    list_filter = ('is_admin',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2')}
         ),
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Buyer, UserAdmin)
admin.site.register(Item, ItemsChangeForm)
admin.site.register(Category, CategoryAdmin)
admin.site.register(ItemInChecklist, ItemInCheckListAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
admin.site.unregister(Group)
