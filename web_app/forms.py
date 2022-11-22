from django.forms import Form, CharField

class TokenFormA(Form):
    token_input_A = CharField(max_length = 35)

class TokenFormB(Form):
    token_input_B = CharField(max_length = 35)
