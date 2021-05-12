from django.shortcuts import render, redirect
from django.http import HttpResponse
from keras.preprocessing import image
from keras.preprocessing.image import load_img
from keras.models import load_model
import numpy as np
import matplotlib.pyplot as plt

from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.contrib.auth.models import User, auth
from django.contrib.auth.forms import UserCreationForm
from . forms import SignUp

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.decorators import login_required
# Create your views here.

def login(request):
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        
        if user is not None:
            auth.login(request,user)
            return redirect(home)
        else:
            return redirect('/')
    else:
        return render(request, 'login.html')

def signup(request):
    form = SignUp()
    if request.method == 'POST':
        form = SignUp(request.POST)
        if form.is_valid():
            form.save()

    context = {'form':form}
    return render(request, 'signup.html', context)

@login_required(login_url='/')
def home(request):
    context ={}
    if request.method == 'POST' and request.FILES['myfile']:
        
        myfile = request.FILES['myfile']
        
        fs = FileSystemStorage()
        filename = fs.save(myfile.name, myfile)
        uploaded_file_url = fs.url(filename)
        
        print(uploaded_file_url)
        
        image_path= 'D:/Django/DjangoProject'+ uploaded_file_url
        img = image.load_img(image_path, target_size=(32, 32))
        img = np.expand_dims(img, axis=0)
        
        model = load_model('GoodModel.h5')
        #model = load_model('flag.h5')

        #context['result']=model.predict_classes(img)
        
        #result = model.predict_classes(img)
        
        result = np.argmax(model.predict(img), axis=1)
        if result ==[0]:
            print("Classified: Afganistan")
        elif result ==[1]:
            print("Classified: America")
        elif result ==[2]:
            print("Classified: Argentina")
        elif result ==[3]:
            print("Classified: Bangladesh")
        elif result ==[4]:
            print("Classified: Bhutan")
        elif result ==[5]:
            print("Classified: India")
        elif result ==[6]:
            print("Classified: Maldives")
        elif result ==[7]:
            print("Classified: Nepal")
        elif result ==[8]:
            print("Classified: Pakistan")
        else:
            print("Classified: SriLanka")
        
        context['result']=result
        context['prob']=model.predict(img)
        context['image_name']=myfile.name
        context['url']=fs.url(image)
        
    return render(request, 'home.html',context)
    
def logoutUser(request):
    logout(request)
    return redirect('/')