from contextlib import redirect_stderr
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect

#a decorators for un_authorized users
def unauthenticated_user(view_func):
    def wrapper(request,*args,**kwargs):
        print(f'User Active: {request.user}')
        print(f'User : {request.user.is_authenticated}')

        if request.user.is_authenticated:
            
            return redirect('home')
        else:
            return view_func(request,*args,**kwargs)

    return wrapper


#decorators for allowing roles 
def allowed_users(allowed_roles = []):
    def decorator(view_func):
        def wrapper(request, *args , **kwargs):
            group = None
            #group = allowed_roles 
            print('Checking Group ---- if it exists')
            #print(request.user.groups)
            print(request.user.groups.exists())
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                print(group)
            if group in allowed_roles:
                return view_func(request , *args, **kwargs)

            else:
                print('it is working')
                return  redirect('dashboard')
        return wrapper 
    return decorator

#admin_ony_decorator
def admin_only(viewfunc):
    
    def wrapper(request,*args,**kwargs):
        print('GROUP_NAME :',request.user.groups.all())

        group = None 
        if request.user.groups.exists():
            group = request.user.groups.all()[0].name
        
        if group == 'customer':
            return redirect('home')
        if group == 'admin':
            return viewfunc(request, *args, **kwargs)
            

    return wrapper