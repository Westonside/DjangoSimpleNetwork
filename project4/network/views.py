from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.http import JsonResponse
import json
from .models import User,Post,Actions, Follower
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, "network/index.html")


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]

        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")




@csrf_exempt
@login_required
def post(request):
    if request.method != "POST":
        return JsonResponse({"error":"POST request is required for this route"},status=405)
    data = json.loads(request.body)
    user = request.user
    body = data.get("body", "")
    #not making a new post for some reason look into that 
    
    newPost = Post(user=user,body=body)
    newPost.save()
    print(body)
    print(user)
    
    return JsonResponse({"message":"post successful"}, status = 201)
    # print(request.status_code)



def getPosts(request,section):
    print(f'request, {request.user}')

    #check if the use is anonymous and allow them to only see the all posts change request value

    # if request.user.is_anonymous:
    #     print('equal')
    print(section)
    
    #where determine the starting and endpoints
    start = int(request.GET.get("start") or 0)
    print(start)
    end = int(request.GET.get("end") or (start+9))
    print(start)
    print(end)


    #use section to indicate wheter you are using the following or the all posts sections for fetch requests
    if section == "All Posts":
        #all posts
        
        posts = Post.objects.all()
        
    
    elif section == "Following":
        #get who user follows
        # posts = Post.objects.filter()

        print('get users where user follows this person')
        followed = Follower.objects.filter(follower=request.user)
        tester = followed.first()
        print(tester.followedUser)
        
        posts = Post.objects.filter(user=followed[0].followedUser)
        print(f"first follower {posts}")
        for follow in followed[1:]:
            #go from the second entry onwards and do the union of the sets
            posts = posts | Post.objects.filter(user=follow.followedUser)
        print(f'test 123 {posts} ')
        print(posts)
        
        #else the user is trying to get the posts of a user
    else:
        user = User.objects.filter(username=section).first()
        print(f"here is the user {user}")
        posts = Post.objects.filter(user=user)
        print(posts)
        
        
    
    
    posts = posts.order_by("-timestamp").all()
    posts = posts[start:end]
    
    # # returns all of the posts posted ever
    # return JsonResponse([post.serialize() for post in range(start,end+1)], safe = False)
    if request.user.is_anonymous:
            return JsonResponse([post.serialize(request) for post in posts], safe = False)
    return JsonResponse([post.serialize(request) for post in posts], safe = False)
    
def getUser(request,userID):
    print(userID)
    user = User.objects.filter(username=userID).first()
    print(user)
    
    followers = Follower.objects.filter(followedUser = user.pk )
    followersCount = Follower.objects.filter(followedUser = user).count()

    following = Follower.objects.filter(follower = user).count()
    return JsonResponse({"user": user.username, "followers": followersCount, "following": following})

def getUserPosts(request, user):
    print('find the posts of a selected user')

# @login_required
def doesFollow(request, selectedUser):
    if(request.method !="GET"):
        return JsonResponse({"error":"improper request"}, 405)
    theUser = User.objects.filter(username = selectedUser).first()
    print("here is the user obhect shit")
    print(theUser)
    theFollow = Follower.objects.filter(followedUser = theUser, follower = request.user).first()
    print(theFollow)
    print("above is the does follow code")
    if(theFollow is None):
        return JsonResponse({"follow_status": False})
    else:
        return JsonResponse({"follow_status": True})

@login_required
def getSelf(request):
    followers = Follower.objects.filter(followedUser = request.user)
    followersCount = Follower.objects.filter(followedUser = request.user).count()
    
    for follower in followers:
        print(follower)

    # print(followers)
    following = Follower.objects.filter(follower = request.user).count()
    print(following)
    return JsonResponse({"followers": followersCount, "following": following}, safe = False)




def likePost(request,postID):
    print(f"user {request.user} liked {postID}")
    print('like post')
    testing = Actions.objects.filter(postID = postID, actionUserID=request.user.pk).first()
    if testing is None:
        post = Post.objects.filter(pk=postID).first()
        user = User.objects.filter(pk=request.user.pk).first()
        newLike = Actions(postID = post, actionUserID = user, liked = True)
        newLike.save()
    elif testing.liked == True:
        testing.liked = False
        testing.save()
    elif testing.liked == False:
        testing.liked = True
        testing.save()

    else:
        return JsonResponse({"error": "An error has occured that I could not predict"})
    print(testing)
    return JsonResponse({"success": True})



@csrf_exempt
def editPost(request,post):
    if request.method != "PUT":
        return JsonResponse({"error":"PUT request is required for this route"},status=405)
    data = json.loads(request.body  )
    print(data)
    thePost = Post.objects.filter(pk=post)
    print(thePost)
    thePost.update(body=data["editValue"])
    print(thePost)
    return JsonResponse({})
    

@login_required
def followUser(request, name):
    print(name)
    if request.method !="GET":
        return JsonResponse({"status": "Incorrect Request Type!"})

    selectedUser = User.objects.filter(username = name).first()
    doesFollow = Follower.objects.filter(followedUser = selectedUser, follower = request.user).first()
    print(f"here ya go {doesFollow}")
    if(request.user == selectedUser):
        return JsonResponse({"status": "User already followed"})
    if doesFollow is None: 
        follow = Follower(followedUser = selectedUser, follower = request.user)
        follow.save()
        print("followed")
        return JsonResponse({"status" : "Followed user"})
    else:
        doesFollow.delete()
        print('unfollowed')
        return JsonResponse({"status":"Unfollowed user"})

