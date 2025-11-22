from django.forms import ModelForm, TextInput, Textarea, NumberInput, FileInput, CheckboxInput

from landing.models import Item, Book, News


class ItemForm(ModelForm):
    class Meta:
        model = Item
        fields = ["name", "description"]

    def __init__(self, *args, **kwargs):
        super(ItemForm, self).__init__(*args, **kwargs)

        self.fields["name"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Название"}
        )

        self.fields["description"].widget.attrs.update(
            {"class": "form-control", "placeholder": "Описание"}
        )


class BookForm(ModelForm):
    """Форма для создания и редактирования книги"""

    class Meta:
        model = Book
        fields = ["title", "author", "description", "isbn", "year_published", "pages", "cover_image"]

    def __init__(self, *args, **kwargs):
        super(BookForm, self).__init__(*args, **kwargs)

        # Настраиваем виджеты и атрибуты
        self.fields["title"].widget = TextInput(attrs={
            "class": "form-control",
            "placeholder": "Название книги"
        })
        self.fields["author"].widget = TextInput(attrs={
            "class": "form-control",
            "placeholder": "Автор"
        })
        self.fields["description"].widget = Textarea(attrs={
            "class": "form-control",
            "placeholder": "Описание книги",
            "rows": 4
        })
        self.fields["isbn"].widget = TextInput(attrs={
            "class": "form-control",
            "placeholder": "ISBN (13 цифр)"
        })
        self.fields["year_published"].widget = NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Год издания"
        })
        self.fields["pages"].widget = NumberInput(attrs={
            "class": "form-control",
            "placeholder": "Количество страниц"
        })
        self.fields["cover_image"].widget = FileInput(attrs={
            "class": "form-control"
        })


class NewsForm(ModelForm):
    """Форма для создания и редактирования новости"""

    class Meta:
        model = News
        fields = ["title", "content", "image", "is_published"]

    def __init__(self, *args, **kwargs):
        super(NewsForm, self).__init__(*args, **kwargs)

        self.fields["title"].widget = TextInput(attrs={
            "class": "form-control",
            "placeholder": "Заголовок новости"
        })
        self.fields["content"].widget = Textarea(attrs={
            "class": "form-control",
            "placeholder": "Содержание новости",
            "rows": 6
        })
        self.fields["image"].widget = FileInput(attrs={
            "class": "form-control"
        })
        self.fields["is_published"].widget = CheckboxInput(attrs={
            "class": "form-check-input"
        })