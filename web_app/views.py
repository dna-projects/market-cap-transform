from dataclasses import dataclass
from django.http import JsonResponse
from django.views.generic import TemplateView, FormView
from django.shortcuts import render, redirect
from web_app.services import get_covalent_data, get_coingecko_data
from web_app.forms import TokenForm
import json

class InitialPageView(FormView):
    template_name = "initial.html"
    form_class = TokenForm

    def get(self, request):
        request.session.clear()
        for item in request.session.keys():
            print(item)
        return render(request, self.template_name, {'form': self.form_class})

    def post(self, request):
        # Redirect when form is submitted
        if request.accepts('text/html'):
            return redirect('transform')
        # When the JS from the frontend makes a post request, Django
        # will return data using JsonResponse
        elif request.accepts('application/json'):
            json_data = json.load(request)
            token_query = json_data['token_query'].lower()
            input_name = json_data['token_id']
            first_api_call = get_coingecko_data("https://api.coingecko.com/api/v3/search?", token_query, "query")

            tokens_data_cov = get_covalent_data('9001', 'xy=k/diffusion/tokens/')

            # Organize json data from covalent into a dictionary of name, symbol, and address
            token_records = [
                {
                    'name': token['contract_name'],
                    'symbol': token['contract_ticker_symbol'],
                    'address': token['contract_address']
                }
                    for token in tokens_data_cov['data']['items']
            ]

            compatible_tokens = []
            for token_data in token_records:
                if token_query in token_data['name'].lower() or token_query in token_data['symbol'].lower():
                    coin_info_by_addr = get_coingecko_data(f"https://api.coingecko.com/api/v3/coins/evmos/contract/{token_data['address']}")
                    if coin_info_by_addr:
                        compatible_tokens.append({'name': token_data["name"], 'id': coin_info_by_addr['id']})

            # Django prefers the data given to the frontend is a dictionary
            try:
                token_id = {'token_data': first_api_call["coins"][0]["id"]}
            except:
                print("could not find token part 1")
                token_id = {}

            request.session[input_name] = token_id
            print(request.session[input_name])
            # token_list = {'token_list' : first_api_call["coins"]}
            token_list = {'token_list' : compatible_tokens}
            return JsonResponse(token_list)

class TransformPageView(TemplateView):
    template_name = "transform.html"

    # Keep track of token properties
    @dataclass
    class Token:
        name: str
        img: str = None
        symbol: str = None
        price: float = None
        transform_price: float = None
        percentage: float = None

    def calculate_percentage(self, market_cap_a, market_cap_b):
        # Based on which token has the larger marketcap
        calculation = max(market_cap_a, market_cap_b) / min(market_cap_a, market_cap_b) * 100
        # Set to negative when token a is larger
        if market_cap_a > market_cap_b:
            calculation *= - 1
        return calculation

    def get(self, request):
        # Second API call
        token_a_id = request.session["id_token_input_A"]
        token_a_info = {}
        token_b_id = request.session["id_token_input_B"]
        token_b_info = {}
        try:
            second_api_call_token_a = get_coingecko_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false", token_a_id["token_data"], "ids")
            token_a_info = {
                'price': second_api_call_token_a[0]["current_price"] , 
                'market_cap': second_api_call_token_a[0]["market_cap"],
                'img_url': second_api_call_token_a[0]["image"],
                'symbol': second_api_call_token_a[0]["symbol"]
            }
            second_api_call_token_b = get_coingecko_data("https://api.coingecko.com/api/v3/coins/markets?vs_currency=usd&order=market_cap_desc&per_page=100&page=1&sparkline=false", token_b_id["token_data"], "ids")
            token_b_info = {
                'price': second_api_call_token_b[0]["current_price"] , 
                'market_cap': second_api_call_token_b[0]["market_cap"],
                'img_url': second_api_call_token_b[0]["image"],
                'symbol': second_api_call_token_b[0]["symbol"]
            }

            # Setup each token
            token_a = self.Token(
                token_a_id["token_data"], 
                token_a_info["img_url"], 
                token_a_info["symbol"], 
                token_a_info["price"],
                token_b_info["market_cap"] / token_a_info["market_cap"] * token_a_info["price"], 
                self.calculate_percentage(token_a_info["market_cap"], token_b_info["market_cap"])
            )

            token_b = self.Token(
                token_b_id["token_data"], 
                token_b_info["img_url"], 
                token_b_info["symbol"], 
                token_b_info["price"], 
                percentage=297
            )
        except:
            print("No results...")
            token_a_info = {}
            token_b_info = {}

        return render(request, self.template_name,
            {"token_a": token_a, "token_b": token_b})