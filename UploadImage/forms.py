from django import forms


class ArticleForm(forms.Form):
    name = forms.CharField(label='Вставьте url',
                           widget=forms.URLInput(attrs={'class': 'form-control',
                                                        'placeholder': 'link to page'}),
                           required=False)
    picture = forms.ImageField(label='Или выберите картинку',
                               required=False)

    def clean(self):
        name = self.cleaned_data.get('name')
        image = self.cleaned_data.get('picture')

        if name and image:
            raise forms.ValidationError('Заполненным может быть только 1 поле')

        if name == '' and image == None:
            raise forms.ValidationError('Нужно ввести данные хотя бы в 1 поле')

