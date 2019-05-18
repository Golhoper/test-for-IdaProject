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

        if name == '' and image is None:
            raise forms.ValidationError('Нужно ввести данные хотя бы в 1 поле')


class ChangeParamsForm(forms.Form):
    width = forms.IntegerField(label='Ширина',
                             required=False,
                             widget=forms.NumberInput(attrs={'class': 'form-control'}))
    height = forms.IntegerField(label='Высота',
                              required=False,
                              widget=forms.NumberInput(attrs={'class': 'form-control'}))
    size = forms.IntegerField(label='Макс. размер в байтах',
                            required=False,
                            widget=forms.NumberInput(attrs={'class': 'form-control'}))

    def clean(self):
        error_string = ''

        width = self.data.get('width', False)
        height = self.data.get('height', False)
        size = self.data.get('size', False)

        if any([width, height, size]):
            try:
                res = int(width)
            except:
                if width != '':
                    error_string += '"Ширина" должна быть числовым значением. '

            try:
                res = int(height)
            except:
                if height != '':
                    error_string += '"Высота" должна быть числовым значением. '

            try:
                res = int(size)
            except:
                if size != '':
                    error_string += 'Размер в байтах должен быть числовым значением.'

            if error_string != '':
                raise forms.ValidationError(error_string)