from dataclasses import dataclass
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from web_app.services import get_covalent_data, get_coingecko_data
from web_app.forms import TokenFormA, TokenFormB
import json

class InitialPageView(FormView):
    template_name = "initial.html"
    form_A = TokenFormA
    form_B = TokenFormB

    def get(self, request):
        if request.accepts('text/html'):
            # UNCOMMENT TO make covalent API request 
            # NOTE - Must add COVALENT_API_KEY='...api key...' to .env file

            # tokens_data = get_covalent_data('9001', 'xy=k/diffusion/tokens/')
            # token_list = [token['contract_ticker_symbol'] for token in tokens_data['data']['items']]
            # print(token_list)

            # NOTE - Uncomment to make coingecko api request
            # search = get_coingecko_data("evmos")
            # print(search["coins"][0]["id"])
            return render(request, self.template_name, {"form_A":self.form_A , "form_B":self.form_B})
        else:
            # When the JS from the frontend makes a post request, Django
            # will return data using JsonResponse 

            # data_from_post = json.load(request)['token_query']
            # Django prefers the data given to the frontend is a dictionary
            data = {'test': 'a test!'}
            return JsonResponse(data)

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