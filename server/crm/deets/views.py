from django.shortcuts import render
from django.contrib import messages
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
import json

# db
import os
from supabase import create_client, Client

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# Create your views here.
def read(request):
    response = supabase.table('crm').select("*").execute()
    messages.success(request, 'Read successful...')
    response_data = response.data
    return HttpResponse(response_data)

@csrf_exempt
def add(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            try:
                EmailValidator()(email)
            except ValidationError:
                return HttpResponse('Invalid email...')
        response = supabase.table('crm').insert(data).execute()
        messages.success(request, 'Add successful...')
        return HttpResponse(response)
    else:
        return HttpResponse('Invalid request method...')

@csrf_exempt
def update(request, id):
    if request.method == 'PUT':
        data = json.loads(request.body)
        email = data.get('email')
        if email:
            try:
                EmailValidator()(email)
            except ValidationError:
                return HttpResponse('Invalid email...')
        response = supabase.table('crm').update(data).eq('id', id).execute()
        messages.success(request, 'Update successful...')
        return HttpResponse(response)
    else:
        return HttpResponse('Invalid request method...')

@csrf_exempt
def delete(request, id):
    if request.method == 'DELETE':
        response = supabase.table('crm').delete().eq('id', id).execute()
        messages.success(request, 'Delete successful...')
        return HttpResponse(response)
    else:
        return HttpResponse('Invalid request method...')
