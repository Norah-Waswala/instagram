from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from .models import  Profile, Image,  Follow,Followers, User
from .forms import DetailsForm, ImageForm, authform
from .email import send_welcome_email
# Create your views here.
def index(request):
    '''
    Function that renders the landing page
    '''
    return render(request, 'index.html')

# def index(request):
#     '''
#     Function that renders the index page(timeline)
#     '''
#     Images = Image.objects.all()
#     comments = Comment.objects.all()
#     return render(request, 'index.html', {'Images':Images, 'comments':comments})
@login_required(login_url='login')
def search_profile(request):
    if 'search_user' in request.GET and request.GET['search_user']:
        name = request.GET.get("search_user")
        results = Profile.search_profile(name)
        print(results)
        message = f'name'
        params = {
            'results': results,
            'message': message
        }
        return render(request, 'search.html', params)
    else:
        message = "You haven't searched for any image category"
    return render(request, 'search.html', {'message': message})
@login_required(login_url='/accounts/login/')
def createImage(request):
    
    createImage = ImageForm()
    
    if request.method=='Image':
        form = authform(request.Image)
        if form.is_valid():
            print('valid')
            name = form.cleaned_data['your_name']
            email = form.cleaned_data['email']
            user = User(name = name,email = email)
            user.save()
            send_welcome_email(name,email)
            
            
        else:
            form=authform()
            
        createImage = ImageForm(request.Image,request.Files)
        if createImage.is_valid():
            createImage.save()
            return redirect('index')
        else:
            return HttpResponse('Your form is incorrect')
    else: render(request, 'createImage_form.html', {'createImage':createImage, 'authform':form})
    
 
@login_required(login_url='/accounts/login/')   
def update_Image(request, Image_id):
    Image_id=int(Image_id)
    try:
        Image_up=Image.objects.get(id=Image_id)
    except Image.DoesNotExist:
        return redirect('index')
    Image_form=ImageForm(request.Image or None,instance=Image_up)
    if Image_form.is_valid():
        Image_form.save()
        return redirect('index')
    return render(request,'createImage_form.html', {'update':Image_form})

@login_required(login_url='/accounts/login/')
def delete_Image(request, Image_id):
    Image_id=int(Image_id)
    try:
        Image_up=Image.objects.get(id=Image_id)
    except Image.DoesNotExist:
        return redirect('index')
    Image_up.delete()
    return redirect('index')

def showprofile(request):
    Images = Image.objects.all()
    following = Follow.objects.all()
    followers  = Followers.objects.all()
    followercount=len(followers)  
    
    if request.method=='Image':
        details_form = DetailsForm(request.Image, request.Files)
        Images_form = ImageForm(request.Image, request.Files)
        
        if details_form.is_valid():
            details_form.save()
            
        if Images_form.is_valid():
            Images_form.save()
            
            return redirect('showprofile')
        else:
            return HttpResponse('Some of the details in your forms are incorrect')
    else:
        return render(request,'showprofile.html', {'details_form':details_form, 'Images_form':Images_form, 'Images':Images, 'following':following, 'followercount':followercount}) 