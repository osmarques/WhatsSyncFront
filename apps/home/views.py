# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""

import base64
from io import BytesIO
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect,JsonResponse
from django.template import loader
from django.urls import reverse
from .forms import PessoaForm
import json as j
from django.views.decorators.csrf import csrf_exempt
#from .message import *
from .banco import *
from .Functions import *
from urllib.parse import unquote

#@csrf_exempt
@login_required(login_url="/login/")
def index(request):
    context = {'segment': 'index'}
    html_template = loader.get_template('home/index.html')
    return HttpResponse(html_template.render(context, request))

@csrf_exempt
#@login_required(login_url="/login/")
def pages(request):
    
    context = {}
    # All resource paths end in .html.
    # Pick out the html file name from the url. And load that template.
    try:


        api_key = "123"
        token = "otavio"
        load_template = request.path.split('/')[-1]
        print(request)
        print(load_template)
        print(request.method)

        status = instance_info_v2()
        print(status)

        
        # #print(ver_user.text)
        # ver_user = ver_user.get('instance_data', {}).get('user', {})
        if status:
            qrcode = init_instance_v2()
            load_template = 'qrcode.html'
            
        

        valida_login = get_qrcode()

        if valida_login:
            load_template = 'qrcode.html'

        print(load_template)
        context['segment'] = load_template

        if load_template == 'admin':
            return HttpResponseRedirect(reverse('admin:index'))
        
        if load_template == 'chat.html':
            if request.method == 'POST':
                print('Entrou no post')
                form = PessoaForm(request.POST)

                
                if form.is_valid():  # Corrigido de 'formulario' para 'form')
                    formulario = PessoaForm()
                    msg = form.cleaned_data['mensagem']
                    minha_variavel = request.POST.get('minhaVariavel', '')
                    minha_variavel = minha_variavel.replace('  ','')
                    linhas_sem_em_branco = [linha for linha in minha_variavel.splitlines() if linha.strip()]
                    nova_string = "\n".join(linhas_sem_em_branco)

                    nova_string = nova_string.replace('(','').replace(',)','')
                    print(nova_string)
                    # numberid = get_number(nova_string + ' ')
                    # numero = numberid.split('@')
                    # num_trat = numero[0].split('-',1)
                    #conversas = select(nova_string)
                    menu = barra_chat()
                    print(msg)
                    send_text(nova_string,msg)

                    context = {'formulario': formulario,'conversas':conversas,'menu':menu} # Corrigido de 'formulario' para 'form'
                    html_template = loader.get_template('home/' + load_template)
                    return HttpResponse(html_template.render(context, request))
            
            if request.method == 'GET':
                
                formulario = PessoaForm()
                print('gerou conversas')
                conversas = select('')
                menu = barra_chat()
                print('gerou barra')

                context = {'formulario': formulario,'conversas':conversas,'menu':menu}  # Adiciona o formulário ao contexto
                html_template = loader.get_template('home/' + load_template)
                return HttpResponse(html_template.render(context, request))
            
        if load_template == 'mensagens':
            if request.method == 'POST':
                corpo_solicitacao = request.body.decode('utf-8')
                corpo_solicitacao = corpo_solicitacao.replace('++','').replace('%0A','').replace('+', ' ')
                corpo_solicitacao = unquote(corpo_solicitacao)
                #print(corpo_solicitacao)
                numberid = get_number(corpo_solicitacao)
                conversas = select(numberid)
                print (conversas)
                return HttpResponse(conversas)
            
        if load_template == 'conversas':
                conversas = select()
                return HttpResponse(conversas)
            
        if load_template == 'qrcode.html':
            if request.method == 'GET':
                context = {'imagem_base64': qrcode,}
                #qrcode = get_qrcode()

                #context = {'qrcode': qrcode,}
                html_template = loader.get_template('home/' + load_template)
                return HttpResponse(html_template.render(context, request))
            
        if load_template == 'webhook':   
            if request.method == 'POST':
                print('entrou no webhook')
                json = j.loads(request.body)
                insert('recebida',json)
                # Faça algo com os dados recebidos, por exemplo, salve no banco de dados
                # e retorne uma resposta adequada

            return j.JsonResponse({'status': 'success'})

                
        print('Deu ruim')
        html_template = loader.get_template('home/' + load_template)
        return HttpResponse(html_template.render(context, request))

    except template.TemplateDoesNotExist:

        html_template = loader.get_template('home/page-404.html')
        return HttpResponse(html_template.render(context, request))

    except:
        html_template = loader.get_template('home/page-500.html')
        return HttpResponse(html_template.render(context, request))
    

@csrf_exempt
def webhook_receiver(request):
    if request.method == 'POST':
        print('entrou no webhook')
        json = j.loads(request.body)
        insert(json)

        # Faça algo com os dados recebidos, por exemplo, salve no banco de dados
        # e retorne uma resposta adequada

        return j.JsonResponse({'status': 'success'})

    return j.JsonResponse({'status': 'error', 'message': 'Método não permitido'}, status=405)

@csrf_exempt
def chat(request):
        load_template = request.path.split('/')[-1]
        context['segment'] = load_template
        if request.method == 'POST':
            print('Entrou no post')
            form = PessoaForm(request.POST)

            
            if form.is_valid():  # Corrigido de 'formulario' para 'form'
                formulario = PessoaForm()
                msg = form.cleaned_data['mensagem']
                #print(msg)
                print("chegou aqui 1 - module chat")
                        
                context = {'formulario': formulario} # Corrigido de 'formulario' para 'form'
                html_template = loader.get_template('home/' + load_template)
                return HttpResponse(html_template.render(context, request))
            
            if request.method == 'GET':
                
                formulario = PessoaForm()
                print(formulario)
                context = {'formulario': formulario}  # Adiciona o formulário ao contexto
                print(context)
                html_template = loader.get_template('home/' + load_template)
                return HttpResponse(html_template.render(context, request))
            
@csrf_exempt
def mensagens(request):
    if request.method == 'GET':
        conversas = select()

        # Faça algo com os dados recebidos, por exemplo, salve no banco de dados
        # e retorne uma resposta adequada

        return conversas

    return conversas          
            



