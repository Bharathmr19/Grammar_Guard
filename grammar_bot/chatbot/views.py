from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests

def index(request):
    return render(request, 'chatbot/index.html')

@api_view(['POST'])
def chatbot_api(request):
    user_input = request.data.get('message')
    response = process_user_input(user_input)
    return Response({'response': response})

def process_user_input(user_input):
    api_url = "https://api.languagetool.org/v2/check"
    payload = {
        'text': user_input,
        'language': 'en-US'
    }
    response = requests.post(api_url, data=payload)
    result = response.json()
    corrections = result.get('matches', [])
    if corrections:
        suggestions = []
        for correction in corrections:
            message = correction.get('message')
            suggestions.append(message)
        return ' '.join(suggestions)
    else:
        return "Your text seems to be correct!"
