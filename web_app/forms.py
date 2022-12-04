from django.forms import Form, CharField, TextInput, HiddenInput

# Token A input field

class TokenForm(Form):
    token_input_A = CharField(
        max_length = 35,
        widget=TextInput(attrs={
            'placeholder' : 'Add Evmos token...',
        })
    )

    token_input_A_data = CharField(max_length=35, widget=HiddenInput)

    token_input_B = CharField(
        max_length = 35,
        widget=TextInput(attrs={
            'placeholder' : 'Add any token...',
        })
    )

    token_input_B_data = CharField(max_length=35, widget=HiddenInput)

    def __init__(self, *args, **kwargs):
        super(TokenForm, self).__init__(*args, **kwargs)
        self.fields['token_input_A'].widget.attrs.update({'class': 'token-input'})
        self.fields['token_input_A'].label = '' # label = '' is required to remove a label above the input field which pushes the input field down.
        self.fields['token_input_B'].widget.attrs.update({'class': 'token-input'})
        self.fields['token_input_B'].label = '' # label = '' is required to remove a label above the input field which pushes the input field down.