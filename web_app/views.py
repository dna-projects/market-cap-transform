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
            json_data = json.load(request)
            data_from_post = json_data['token_query']
            input_name = json_data['token_id']
            first_api_call = get_coingecko_data("https://api.coingecko.com/api/v3/search?", data_from_post, "query")
            # Django prefers the data given to the frontend is a dictionary
            try:
                token_id = {'token_data': first_api_call["coins"][0]["id"]}
            except:
                print("could not find token part 1")
                token_id = {}
            request.session[input_name] = token_id
            return JsonResponse({})

class TransformPageView(TemplateView):
    template_name = "transform.html"

    # Keep track of token properties
    @dataclass
    class Token:
        name: str
        img: str = None
        price: float = None
        percentage: float = None

    # TODO - Figure out how to handle what happens when the name 
    # spans onto a separate line. 

    def get(self, request):

        # Second API call
        token_a_id = request.session["id_token_input_A"]
        token_a_info = {}
        token_b_id = request.session["id_token_input_B"]
        token_b_info = {}
        try:
            second_api_call_token_a = get_coingecko_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false", token_a_id["token_data"], "ids")
            token_a_info = {'token_price': second_api_call_token_a[0]["current_price"] , 'token_market_cap': second_api_call_token_a[0]["market_cap"]}
            second_api_call_token_b = get_coingecko_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false", token_b_id["token_data"], "ids")
            token_b_info = {'token_price': second_api_call_token_b[0]["current_price"] , 'token_market_cap': second_api_call_token_b[0]["market_cap"]}
        except:
            print("could not find token part 2")
            token_a_info = {}
            token_b_info = {}

        token_a = self.Token(token_a_id["token_data"], '💸', token_b_info["token_market_cap"] / token_a_info["token_market_cap"] * token_a_info["token_price"], token_b_info["token_market_cap"] / token_a_info["token_market_cap"] * 100)
        token_b = self.Token(token_b_id["token_data"], '💸', token_b_info["token_price"], 297)

        return render(request, self.template_name,
            {"token_a": token_a, "token_b": token_b, "token_a_price": token_a_info, "token_b_price": token_b_info})