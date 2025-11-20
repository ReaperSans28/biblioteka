from django.forms import ModelForm

from landing.models import Item

class ItemsForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(ItemsForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )

        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Описание"}
        )