from django.contrib.auth.forms import SetPasswordForm

class CustomerSetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.items():
            field.widget.attrs['class'] = "w-full px-4 py-2 mt-2 bg-gray-100 text-gray-900 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-green-600"