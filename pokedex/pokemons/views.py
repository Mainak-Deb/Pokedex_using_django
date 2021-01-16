from django.shortcuts import render,redirect,HttpResponse
import requests
from django.core.paginator import Paginator

from math import ceil
# import the logging library
import logging
import json

colors = {
	'fire': ['#FDDFDF','#de3700'],
	'grass': ['#DEFDE0','#21c400'],
	'electric': ['#FCF7DE','#fa9a00'],
	'water': ['#DEF3FD','#087fc4'],
	'ground': ['#f4e7da','#8f4300'],
	'rock': ['#d5d5d4','#3b3a39'],
	'fairy': ['#fceaff','#ab18ad'],
	'poison': ['#98d7a5','#175900'],
	'bug': ['#f8d5a3','#f07605'],
	'dragon': ['#97b3e6','#c43800'],
	'psychic': ['#eaeda1','#819605'],
	'flying': ['#F5F5F5','#c93838'],
	'fighting': ['#E6E0D4','#996909'],
	'normal': ['#F5F5F5','#996909'],
    'ghost':['#7f7894','#240342'],
    'dark':['#5e5e5c','#0f0f0f'],
    'ice':['#79e4e8','#0388a6'],
    'steel':['#B2B4B5','#696B6F']
};

def index(request):
    mons=[]
    
    for i in range(1,85):
        url="https://pokeapi.co/api/v2/pokemon/"+str(i)
        response = requests.get(url)
        pkmn = response.json()
        poke_type=pkmn['types'][0]['type']['name']
        type_color=colors[poke_type]
        mons.append([i,pkmn['species']['name'],poke_type,type_color])
    paginator=Paginator(mons,28)
    page_num=request.GET.get('page')
    mons_obj=paginator.get_page(page_num)
    
    params={
        'names':mons_obj
    }
    # return HttpResponse(params['names'])
    return render(request, 'index.html',params)

def pokemon(request,pk):
    mons=[]
    url="https://pokeapi.co/api/v2/pokemon/"+str(pk)
    
    response = requests.get(url)
    poke = response.json()
    poke_id=poke['id']

    poke_type=[]
    for c in poke['types']:
        poke_type.append([c['type']['name'],colors[c['type']['name']]])
    type_color=colors[poke_type[0][0]]
    weight=poke['weight'];
    height=poke['height'];
    stats=[]
    for gi in poke["stats"]:
        stats.append(gi["base_stat"]/1.5)
   
    abilities=[]
    for i in poke["abilities"]:
        abilities.append(i["ability"]["name"])
   
    urlw="https://pokeapi.co/api/v2/type/"+str(poke_type[0][0])
    response = requests.get(urlw)
    wek= response.json()
    weakness=[]
    for j in wek['damage_relations']['double_damage_from']:
        weakness.append([j['name'],colors[j['name']]])
    if(len(weakness)==0): weakness.append(["No weakness",'#e0ffde'])
   
    img="https://pokeres.bastionbot.org/images/pokemon/"+str(poke_id)+".png"

    urlbio="https://pokeapi.co/api/v2/pokemon-species/"+str(poke_id)
    response = requests.get(urlbio)
    bio= response.json()
    for b in bio["flavor_text_entries"]:
        if(b["language"]["name"]=="en"):
            desc=b["flavor_text"]
            break;
    shape=bio["shape"]["name"];
    egg=bio[ "egg_groups"][0]["name"];
    try:
        habitat=bio["habitat"]["name"];
    except:
        habitat="No data";
    url_evolution=bio["evolution_chain"]["url"];
    response = requests.get(url_evolution)
    Evolution= response.json()
    chain=[]
    try:
        e1=Evolution["chain"]["species"]["name"];
    except:
        e1="None"
    try:
        e2=Evolution["chain"]["evolves_to"][0]["species"]["name"];
    except:
        e2="None"
    try:
        e3=Evolution["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"];
       
    except:
        e3="None"
    chain=[e1,e2,e3];
   
    evolution=[]
    evolution_name=["Unevolved","First evolution","Second evolution"]
 
    for ev in chain:
      if(ev!="None"):
        url="https://pokeapi.co/api/v2/pokemon/"+str(ev)
        response = requests.get(url)
        evolve = response.json()
        evolve_id=evolve['id']
        evolution.append([evolve_id,ev,"https://pokeres.bastionbot.org/images/pokemon/"+str(evolve_id)+".png"])

    for ev in range(len(evolution)):
        evolution[ev].append(evolution_name[ev])

    pokes={
        "poke_id":poke_id,
        'names':poke['species']['name'].upper(),
        "image":img,
        "type":poke_type,
        "color":type_color,
        "weak":weakness,
        "weight":weight/10,
        "height":height/10,
        "ability":abilities,
        "desc":desc,
        "shape":shape,
        "egg":egg,
        "habitat":habitat,
        "evolution":evolution,
        "data":stats
        
    }
    # return HttpResponse(pokes['weak'])
    return render(request, 'pokemon.html',pokes)
    

def search(request):
    try:
        if request.method=="POST":
            query= request.POST.get('pksearch', '')

        url="https://pokeapi.co/api/v2/pokemon/"+str(query)
            
        response = requests.get(url)
        poke = response.json()
        poke_id=poke['id']

        poke_type=[]
        for c in poke['types']:
            poke_type.append([c['type']['name'],colors[c['type']['name']]])
        type_color=colors[poke_type[0][0]]
        weight=poke['weight'];
        height=poke['height'];
        stats=[]
        for gi in poke["stats"]:
            stats.append(gi["base_stat"]/1.5)
        
        abilities=[]
        for i in range(2):
            abilities.append(poke["abilities"][i]["ability"]["name"])
        
        urlw="https://pokeapi.co/api/v2/type/"+str(poke_type[0][0])
        response = requests.get(urlw)
        wek= response.json()
        weakness=[]
        for j in wek['damage_relations']['double_damage_from']:
            weakness.append([j['name'],colors[j['name']]])
        if(len(weakness)==0): weakness.append(["No weakness",'#e0ffde'])
    
        img="https://pokeres.bastionbot.org/images/pokemon/"+str(poke_id)+".png"

        urlbio="https://pokeapi.co/api/v2/pokemon-species/"+str(poke_id)
        response = requests.get(urlbio)
        bio= response.json()
        for b in bio["flavor_text_entries"]:
            if(b["language"]["name"]=="en"):
                desc=b["flavor_text"]
                break;
        shape=bio["shape"]["name"];
        egg=bio[ "egg_groups"][0]["name"];
        habitat=bio["habitat"]["name"];
        url_evolution=bio["evolution_chain"]["url"];
        response = requests.get(url_evolution)
        Evolution= response.json()
        chain=[]
        try:
            e1=Evolution["chain"]["species"]["name"];
        except:
            e1="None"
        try:
            e2=Evolution["chain"]["evolves_to"][0]["species"]["name"];
        except:
            e2="None"
        try:
            e3=Evolution["chain"]["evolves_to"][0]["evolves_to"][0]["species"]["name"];
        
        except:
            e3="None"
        chain=[e1,e2,e3];
        evolution=[]
        evolution_name=["Unevolved","First evolution","Second evolution"]
    
        for ev in chain:
            if(ev!="None"):
                url="https://pokeapi.co/api/v2/pokemon/"+str(ev)
                response = requests.get(url)
                evolve = response.json()
                evolve_id=evolve['id']
                evolution.append([evolve_id,ev,"https://pokeres.bastionbot.org/images/pokemon/"+str(evolve_id)+".png"])

        for ev in range(len(evolution)):
            evolution[ev].append(evolution_name[ev])

        pokes={
            "poke_id":poke_id,
            'names':poke['species']['name'].upper(),
            "image":img,
            "type":poke_type,
            "color":type_color,
            "weak":weakness,
            "weight":weight/10,
            "height":height/10,
            "ability":abilities,
            "desc":desc,
            "shape":shape,
            "egg":egg,
            "habitat":habitat,
            "evolution":evolution,
            "data":stats
            
        }
        # return HttpResponse(pokes['weak'])
        return render(request, 'pokemon.html',pokes)
        

    except :
         return HttpResponse("Sorry, pokemon not found, please check spelling or enter a valid pokemon name")


def typepk(request,tk):
    mons=[]
    urlt="https://pokeapi.co/api/v2/type/"+str(tk)
    response = requests.get(urlt)
    typejson= response.json()
    typen=typejson['pokemon']
    for t in range(50):
        tname=typejson['pokemon'][t]['pokemon']['name']
        url="https://pokeapi.co/api/v2/pokemon/"+str(tname)
        response = requests.get(url)
        pkmn = response.json()
        poke_id=pkmn['id']

        poke_type=pkmn['types'][0]['type']['name']
        type_color=colors[poke_type]
        mons.append([poke_id,pkmn['species']['name'],poke_type,type_color])
    params={
        'typename':str(tk),
        'names':mons
    }
    # return HttpResponse(params['names'])
    return render(request, 'index.html',params)
