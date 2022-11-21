from dataclasses import dataclass
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from web_app.services import get_covalent_data

class InitialPageView(TemplateView):
    template_name = "initial.html"

    def get(self, request):
        # UNCOMMENT TO make covalent API request 
        # NOTE - Must add COVALENT_API_KEY='...api key...' to .env file

        # tokens_data = get_covalent_data('9001', 'xy=k/diffusion/tokens/')
        # token_list = [token['contract_ticker_symbol'] for token in tokens_data['data']['items']]
        # print(token_list)
        return render(request, self.template_name)

    # TODO - Pass data (token a, token b) into TransformPageView
    # TODO - Check if redirect works (first add form to template file)
    def post(self, request):
        return redirect('transform')

class TransformPageView(TemplateView):
    template_name = "transform.html"

    # Keep track of token properties
    @dataclass
    class Token:
        name: str
        img: str = None
        price: float = None
        percentage: float = None

    token_a = Token('Evmos', '💸', 451.23, 297)

    # TODO - Figure out how to handle what happens when the name 
    # spans onto a separate line. 
    token_b = Token('Cryptocurrency with super long name...')

    def get(self, request):
        return render(request, self.template_name, 
            {"token_a": self.token_a, "token_b": self.token_b})