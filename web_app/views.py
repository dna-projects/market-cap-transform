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
        # UNCOMMENT TO make covalent API request 
        # NOTE - Must add COVALENT_API_KEY='...api key...' to .env file

        # tokens_data = get_covalent_data('9001', 'xy=k/diffusion/tokens/')
        # token_list = [token['contract_ticker_symbol'] for token in tokens_data['data']['items']]
        # print(token_list)

        # NOTE - Uncomment to make coingecko api request
        # search = get_coingecko_data("evmos")
        # print(search["coins"][0]["id"])
        return render(request, self.template_name, {"form_A":self.form_A , "form_B":self.form_B})

    # TODO - Pass data (token a, token b) into TransformPageView
    # TODO - Check if redirect works (first add form to template file)
    def post(self, request):
        # When the JS from the frontend makes a post request, Django
        # will return data using JsonResponse
        if request.accepts('application/json'):
            data_from_post = json.load(request)['token_query']
            first_api_call = get_coingecko_data("https://api.coingecko.com/api/v3/search?", data_from_post, "query")
            # Django prefers the data given to the frontend is a dictionary
            try:
                token_id = {'token_data': first_api_call["coins"][0]["id"]}
            except:
                print("could not find token part 1")
                token_id = {}
            # Second API call
            token_data = {}
            try:
                second_api_call = get_coingecko_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false", token_id["token_data"], "ids")
                token_data = {'token_price': second_api_call[0]["current_price"] , 'token_market_cap': second_api_call[0]["market_cap"]}
            except:
                print("could not find token part 2")
                token_data = {}
            return JsonResponse(token_data)

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