from django.forms import ModelForm, forms, BooleanField

from mailing.models import NewsLetter, Client, Message


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = "form-check-input"
            else:
                field.widget.attrs['class'] = "form-control"


class NewsLetterForm(StyleFormMixin, ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'
        exclude = ('owner',)


class ClientForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
        exclude = ('owner',)


class MessageForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Message
        fields = '__all__'
        exclude = ('owner',)


class NewsLetterManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = NewsLetter
        fields = '__all__'


class ClientManagerForm(StyleFormMixin, ModelForm):
    class Meta:
        model = Client
        fields = '__all__'
