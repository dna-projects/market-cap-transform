from django.forms import Form, CharField, TextInput

# Token A input field

class TokenFormA(Form):
    token_input_A = CharField(
        max_length = 35,
        widget=TextInput(attrs={
            'placeholder' : 'Enter token A...',
        })
    )

    def __init__(self, *args, **kwargs):
        super(TokenFormA, self).__init__(*args, **kwargs)
        self.fields['token_input_A'].widget.attrs.update({'class': 'token-input'})
        self.fields['token_input_A'].label = '' # label = '' is required to remove a label above the input field which pushes the input field down.

# Token B input field

class TokenFormB(Form):
    token_input_B = CharField(
        max_length = 35,
        widget=TextInput(attrs={
            'placeholder' : 'Enter token B...',
        })
    )

    def __init__(self, *args, **kwargs):
        super(TokenFormB, self).__init__(*args, **kwargs)
        self.fields['token_input_B'].widget.attrs.update({'class': 'token-input'})
        self.fields['token_input_B'].label = '' # label = '' is required to remove a label above the input field which pushes the input field down.