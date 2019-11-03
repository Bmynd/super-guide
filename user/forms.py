from django import forms
from django.forms import ValidationError

from user.models import Profile


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'

    def clean_max_distance(self):
        # 获取最小距离和最大距离
        cleaned_data = self.clean()
        min_distance = cleaned_data.get('min_distance')
        max_distance = cleaned_data.get('max_distance')
        if min_distance > max_distance:
            raise ValidationError('min_distance > max_distance')
        return max_distance

    def clean_max_dating_age(self):
        # 获取最小年龄和最大年龄
        cleaned_data = self.clean()
        min_dating_age = cleaned_data.get('min_dating_age')
        max_dating_age = cleaned_data.get('max_dating_age')
        if min_dating_age > max_dating_age:
            raise ValidationError('min_dating_age > max_dating_age')
        return max_dating_age