from django.forms import ModelForm
from django.forms import Textarea
from .models import Post


class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        edit = kwargs.get('instance')
        super(PostForm, self).__init__(*args, **kwargs) 
        if edit:
            self.fields['text'].help_text = "Текст редактируемого поста"
        else:
            self.fields['text'].help_text = " Текст нового поста"
        
    class Meta:
        model = Post
        fields = ['text', 'group']
        labels = {
            'text': 'Текст поста',
            'group': 'Группы'
        }
        widgets = {
            'text': Textarea(attrs={'style': 'height: 193px;'}),
        
        }
        help_texts = {
            "group": "Группа, к которой будет относиться пост",
        }