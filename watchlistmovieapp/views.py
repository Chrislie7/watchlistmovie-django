from argparse import Action
from this import d
from django.db.models import Count
from email import message
from django.db.models import Q
from pdb import post_mortem
from urllib.request import Request
from django.contrib  import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from matplotlib.pyplot import title
from platformdirs import user_cache_dir
from watchlistmovieapp.models import userdetail,watchList
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from datetime import date
from django.http import JsonResponse




import json

import requests
api_key = "2c2ff10535db86631ca0eed7fb422c44"
# http://127.0.0.1:8000/masuk/?next=/account/saveAccount/1486ad2dace7f52ed363fd3a2ed5a433/8996726f0dfa4cdd57b7811c653aa4496f7b543b
def signup(request):
    if request.POST:
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            
            messages.success(request,"Success")
            return redirect('signup')
        else:
            messages.error(request, "Terjadi kesalahan!")
            return redirect('signup')
    else:
        form = UserCreationForm()
        konteks= {
            'form':form
        }
    return render(request,'signup.html',konteks)

# @login_required(login_url=settings.LOGIN_URL)
# def getAuthorizationPage(request):
    
#     current_user = request.user
#     konteks= {
#         'current_user': current_user.id
#     }
#     return render(request,'getAuthorizationPage.html',konteks)

# @login_required(login_url=settings.LOGIN_URL)
# def saveAccount(request,api_key,sessionID):
   
#     current_user = request.user
#     print(current_user.id)
#     simpanCredential = credentialSessionTMDB.objects.create(api_key=api_key, session_id=sessionID, user_id = current_user.id)
    
#     simpanCredential.api_key = api_key
#     simpanCredential.session_id = sessionID
#     simpanCredential.save()
#     messages.success(request,"Success")
#     return JsonResponse({'text': 'sukses'})
    

# @login_required(login_url=settings.LOGIN_URL)
# def getSessionID(request):
#     try:
#         current_user = request.user
#         return credentialSessionTMDB.objects.get(user_id = current_user.id).session_id
#     except:
#         print("An exception occurred")
#         return ''
    
    
# @login_required(login_url=settings.LOGIN_URL)
# def getApikey(request):
#     try:
#         current_user = request.user
#         return credentialSessionTMDB.objects.get(user_id = current_user.id).api_key
#     except:
#         print("An exception occurred")
#         return ''
    
# Create your views here.
@login_required(login_url=settings.LOGIN_URL)
def HomePage(request):
    
    # user = getSessionID(request)
    # if user == '':
    #     current_user = request.user
    #     konteks = {
    #         'id' : current_user.id
    #     }
    #     return render(request,'getAuthorizationPage.html',konteks)
    
    response = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+api_key+'&language=en-US&page=1')
    
    print("Status code: ", response.status_code)
    res = json.loads(response.text)
    
    if response.status_code == 200:
        pesan = "sukses"
    print(res.get("results"))
    konteks = {
        'json' : res.get("results"),
        'pesan': pesan
    }
    return render(request,'HomePage.html',konteks)


#@login_required(login_url=settings.LOGIN_URL)
#def tambah_film(request):
#    if request.POST:
#       form = FormFilm(request.POST)
#        if form.is_valid():
#           form.save()
#            
#            form = FormFilm()
#            pesan = "Data berhasil disimpan"
#
#            konteks = {
#                'form':form,
#                'pesan':pesan
#            }
#    else:
#        form = FormFilm()
#
#        konteks = {
#            'form': form,
#        }
#    return render(request, 'tambah-film.html',konteks)
#

@login_required(login_url=settings.LOGIN_URL)
def addToWatchList(request,id_film,title):
    #jangan lupa validasi jika sudah di ada di watchlist
    # cari cara untuk simpen account_id
  
    # data = { "media_type": "movie", "media_id": id_film, "watchlist": 'true' }
    # response = requests.get('https://api.themoviedb.org/3/account/12397301/watchlist?api_key='+api_key+'&session_id='+getSessionID(request),data)
   
    current_user = request.user
    #if response.status_code >= 200 & response.status_code <= 299:
    try:

        watchListChecker =  watchList.objects.filter(idFilm= id_film).exists()
        if watchListChecker: # update
            print(str(id_film)+"exist")
            
            messages.success(request,"Film Ini sudah ada di Watch List MovieMu")

        else: # create
            watchListAdd =  watchList.objects.create(idFilm= id_film,addUser = current_user.id)
            watchListAdd.save()
            
            messages.success(request,"Berhasil Ditambahkan ke Watch List Movie")
    except Exception as e:
        print(str(e))
  

    account = User.objects.get(id=current_user.id)
    addActionDetail = userdetail(user= account , action='add', titleFilm=title,idFilm = id_film)          
    addActionDetail.save()
    print("Sukses Save DB")
    
    # print("Status code: ", response.status_code)
    # print("response: ", response.json())
    # res = json.loads(response.text)
    #tempData = UserWatchlist.objects.create(idfilm=id_film,)
    return redirect('/homePage')

@login_required(login_url=settings.LOGIN_URL)
def deleteWatchList(request,id_film,title):
    #jangan lupa validasi jika sudah di ada di watchlist
    # cari cara untuk simpen account_id
    
    # data = { "media_type": "movie", "media_id": id_film, "watchlist": False}
  
    # response = requests.post('https://api.themoviedb.org/3/account/12397301/watchlist?api_key='+getApikey(request)+'&session_id='+getSessionID(request),json=data)
    #if response.status_code >= 200 & response.status_code <= 299:
        
        

    current_user = request.user
    deleteRow = watchList.objects.filter(Q(addUser=current_user.id) & Q(idFilm=id_film)).order_by('last_updated').reverse()
    deleteRow.delete()


    account = User.objects.get(id=current_user.id )
    addActionDetail = userdetail(user= account , action='delete', titleFilm=title, idFilm = id_film)          
    addActionDetail.save()
    print("Catat sukses")

    #print("Status code: ", response.status_code)
    #print("response: ", response.json())
    #res = json.loads(response.text)
    #messages.success(request,"Berhasil menghapus ke Watch List Movie")
    #tempData = UserWatchlist.objects.create(idfilm=id_film,)
    return redirect('/Watchlistpage')

@login_required(login_url=settings.LOGIN_URL)
def updateWatchList(request,id_filmBefore):
   
    

    answer = request.POST['movie'].split('#')
    current_user = request.user
    note = request.POST.get('noteUpdate')
    print(note)




    id_film = answer[0]
    title = answer[1]
    
    checkerUpdate = watchList.objects.filter(Q(addUser=current_user.id) & Q(idFilm=id_film) ).exists()
    if checkerUpdate:
        print(checkerUpdate)
        messages.success(request,"Film Sudah ada di Watch List Movie")
    else:
        account = User.objects.get(id=current_user.id)
        updateActionDetail = userdetail(user= account , action='update', titleFilm=title,idFilm = id_film)   
        updateActionDetail.idFilm = id_film
        updateActionDetail.titleFilm = title
        updateActionDetail.save()

        print("berhasil Update user detail(pencatatan)")
        print(current_user.id)
        print(id_film)
        updatewatchList =  watchList.objects.filter(Q(addUser=current_user.id) & Q(idFilm=id_filmBefore)).order_by('last_updated').reverse().first()  
        print(updatewatchList)
        
        
        if updatewatchList is None :
            print("updatewatctList is none")
        else:
            updatewatchList.idFilm = id_film
            updatewatchList.save()   
            print("berhasil update watch list")
            print("sukses update")
    
        messages.success(request,"Berhasil update note ke Watch List Movie")

    return redirect('/Watchlistpage')






@login_required(login_url=settings.LOGIN_URL)
def WatchListView(request):
    
    
    # print("Status code: ", response.status_code)
    # print("Response: ", response.json())
    # res = json.loads(response.text)
  
    #if response.status_code >= 200 & response.status_code <= 299:
    
    current_user = request.user
    objToView = watchList.objects.filter(addUser = current_user.id)
    if objToView:
        print(type(objToView))
        listData = []
        for i in objToView:
            link = 'https://api.themoviedb.org/3/movie/'+str(i.idFilm)+'+?api_key='+api_key+'&language=en-US'
            response = requests.get(link)
            res = json.loads(response.text)
            
            listData.append(res)
            
        allFilm = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+api_key+'&language=en-US&page=1')
        




        print("Status code: ", response.status_code)
        res = json.loads(allFilm.text)
        
        print(res.get("results"))
        konteks = {
            'response' : listData,
            'allfilm': res.get("results")
        }
            
            
        return render(request, 'watchListPage.html',konteks)
    else:
        
            
            
        return render(request, 'watchListPage.html')
@login_required(login_url=settings.LOGIN_URL)
def viewNote(request,id_film):
    
    current_user = request.user
    print(current_user.id+id_film)
    now = userdetail.objects.filter(Q(user_id=current_user.id) & Q(idFilm=id_film)).order_by('id').reverse().first()
    print(now.note)
    if now == ' ' or now is None:
        now = '--empty note--'
    else:
        now = now.note
    html = ' <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js"></script><script src="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/js/bootstrap.min.js"></script> <center> <div class="modal-dialog card"> <div class="modal-content"> <div class="modal-header"> <div class="modal-title"> <h3>--NOTE--</h3> </div> </div> <div class="modal-body"> <strong> %s </strong> </div> <div class="modal-footer"> <button><a href="https://watchlistmovie-p1.herokuapp.com/Watchlistpage/" class="btn btn-dark" data-dismiss="modal">Cancel</a></button> </div> </div> </div> </center> <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/bootstrap@3.3.7/dist/css/bootstrap.min.css" integrity="sha384-BVYiiSIFeK1dGmJRAkycuHAHRg32OmUcww7on3RYdg4Va+PmSTsz/K68vbdEjh4u" crossorigin="anonymous"> ' % now 
    return HttpResponse(html)

def sample_view(request):
    current_user = request.user
    return current_user.id