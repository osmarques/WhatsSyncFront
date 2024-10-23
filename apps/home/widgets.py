

from django.forms.widgets import Select

class IconSelect(Select):
    def create_option(self, name, value, label, selected, index, subindex=None, attrs=None):
        option = super(IconSelect, self).create_option(name, value, label, selected, index, subindex, attrs)
        if value:
            option['icon'] = self.choices.queryset.model._meta.get_field('campo_dropdown').get_choices_dict().get(value)
        return option
