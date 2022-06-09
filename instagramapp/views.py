from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from .models import  Profile, Post,  Follow,Followers, User,Comments
from .forms import DetailsForm, PostForm, authform,NewUserForm
from .email import send_welcome_email
from django.shortcuts import  render, redirect
from django.contrib.auth import login,authenticate
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm 

def register_request(request):
	if request.method == "POST":
		form = NewUserForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful." )
			return redirect("index")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserForm()
	return render (request=request, template_name="registration/register.html", context={"register_form":form})


def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("index")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="registration/login.html", context={"login_form":form})


    
@login_required(login_url='login')
def index(request):
    post = Post.objects.all()
    users = User.objects.exclude(id=request.user.id)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user.profile
            post.save()
            return HttpResponseRedirect(request.path_info)
    else:
        form = PostForm()
    params = {
        'post': post,
        'form': form,
        'users': users,

    }
    return render(request, 'index.html',params)
# def index(request):
#     '''
#     Function that renders the index page(timeline)
#     '''
#     Images = Image.objects.all()
#     comments = Comments.objects.all()
  
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
        message = "No user with that name"
    return render(request, 'search.html', {'message': message})
@login_required(login_url='/accounts/login/')
def createImage(request):
    
    createImage = PostForm()
    
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
            
        createImage = PostForm(request.Image,request.Files)
        if createImage.is_valid():
            createImage.save()
            return redirect('index')
        else:
            return HttpResponse('Your form is incorrect')
    else: render(request, 'upload.html', {'createImage':createImage, 'authform':form})
    
 
@login_required(login_url='/accounts/login/')   
def update_Image(request, Image_id):
    Image_id=int(Image_id)
    try:
        Image_up=Post.objects.get(id=Image_id)
    except Post.DoesNotExist:
        return redirect('index')
    Image_form=PostForm(request.Image or None,instance=Image_up)
    if Image_form.is_valid():
        Image_form.save()
        return redirect('index')
    return render(request,'createImage_form.html', {'update':Image_form})

@login_required(login_url='/accounts/login/')
def delete_Image(request, Image_id):
    Image_id=int(Image_id)
    try:
        Image_up=Post.objects.get(id=Image_id)
    except Post.DoesNotExist:
        return redirect('index')
    Image_up.delete()
    return redirect('index')

def showprofile(request):
    posts = Post.objects.all()
    following = Follow.objects.all()
    followers  = Followers.objects.all()
    followercount=len(followers)
    followingcount=len(following) 
    current_user = request.user 
    
    if request.method=='POST':
        details_form = DetailsForm(request.POST, request.FILES)
        posts_form = PostForm(request.POST, request.FILES)
        
        if details_form.is_valid():
            profile = details_form.save(commit=False)
            profile.user = current_user
            profile.save()
            
        if posts_form.is_valid():
            post = posts_form.save(commit=False)
            post.profile = current_user.profile
            posts_form.save()
            
        return redirect('profile')
        
    else:
        details_form = DetailsForm
        posts_form = PostForm
        
    return render(request,'profile.html', {'details_form':details_form, 'posts_form':posts_form, 'posts':posts, 'following':following, 'followercount':followercount, 'followingcount':followingcount})

def update(request):
    current_user = request.user
    if request.method== 'POST':
        form = DetailsForm(request.POST, request.FILES)
        if form.is_valid():
            Profile.objects.filter(id=current_user.profile.id).update(bio=form.cleaned_data["bio"])
            profile = Profile.objects.filter(id=current_user.profile.id).first()
            profile.profile_pic.delete()
            profile.profile_pic=form.cleaned_data["profile_pic"]
            profile.save()
        return redirect('profile')
    else:
        form = DetailsForm()
    return render(request, 'update_profile.html', {"form":form})

def search_results(request):

    if 'profile' in request.GET and request.GET["profile"]:
        search_term = request.GET.get("profile")
        searched_profiles = Profile.search_by_title(search_term)
        message = f"{search_term}"

        return render(request, 'search.html',{"message":message,"profiles": searched_profiles})

    else:
        message = "You haven't searched for any term"
        return render(request, 'search.html',{"message":message})

