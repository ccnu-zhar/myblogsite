from django import forms
from django.contrib.contenttypes.models import ContentType
from django.db.models import ObjectDoesNotExist
from ckeditor.widgets import CKEditorWidget

class CommentForm(forms.Form):
    content_type = forms.CharField(widget=forms.HiddenInput)
    object_id = forms.IntegerField(widget=forms.HiddenInput)
    text = forms.CharField(widget=forms.Textarea)


    def clean(self):
        # 评论对象验证
        content_type = self.cleaned_data['content_type']
        object_id = self.cleaned_data['object_id']
        try:
            model_class = ContentType.objects.get(model= content_type).model_class()
            model_obj = model_class.objects.get(pk = object_id)
        except ObjectDoesNotExist:
            raise forms.ValidationError('评论对象不存在')

        return self.cleaned_data