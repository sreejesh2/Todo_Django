from django.shortcuts import render,redirect
from django.views.generic import View,TemplateView,FormView,CreateView,ListView,UpdateView,DetailView
from .forms import RegistrationForm,LoginForm,TodoForm,TodoChangeForm,ForgotForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from .models import Tasks
from django.utils.decorators import method_decorator
from django.urls import reverse_lazy
from django.views.decorators.cache import never_cache
# Create your views here.


def sign_required(fn):
    def wrapper(request,*args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request,"please login ")
            return redirect('login')
        return fn(request,*args,**kwargs)
    return wrapper

decks=[sign_required,never_cache]

class SignUpView(CreateView):
    model=User
    template_name='register.html'
    form_class=RegistrationForm
    success_url=reverse_lazy('login')

    def form_valid(self, form):
        messages.success(self.request,"Registration Successfully")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Registration faild")
        return super().form_invalid(form)

    # def get(self,request,*args, **kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    
    # def post(self,request,*args, **kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"Registration successfully")
    #         return redirect('login')
    #     messages.error(request,"Registration faild")
    #     return render(request,self.template_name,{"form":form})


class SigninView(View):
    templates_name='login.html'
    form_class=LoginForm
    model=User

    def get(self,request,*args, **kwargs):
        form=self.form_class
        return render(request,self.templates_name,{"form":form})
    
    def post(self,request,*args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            uname=form.cleaned_data.get("username")
            pwd=form.cleaned_data.get("password")
            usr=authenticate(request,username=uname,password=pwd)
            if usr:
                login(request,user=usr)
                messages.success(request,"Login successfully")
                return redirect('home')
        messages.error(request,"Login faild")    
        return render(request,self.templates_name,{"form":form})    

@method_decorator(decks,name='dispatch')
class IndexView(TemplateView):
    template_name='home.html' 

    # def get(self,request,*args, **kwargs):
    #     return render(request,self.template_name) 

def sign_out(request,*args, **kwargs):
    logout(request)
    return redirect('login')   


@method_decorator(sign_required,name='dispatch')
class TodoCreateView(CreateView):
    model=Tasks
    template_name='task-add.html'
    form_class=TodoForm
    success_url=reverse_lazy('all-todo')
   
    def form_valid(self, form):
        form.instance.user=self.request.user
        messages.success(self.request,"Todo has been created")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Todo Creation Faild")
        return super().form_invalid(form)


    # def get(self,request,*args, **kwargs):
    #     form=self.form_class
    #     return render(request,self.template_name,{"form":form})
    
    # def post(self,request,*args, **kwargs):
    #     form=self.form_class(request.POST)
    #     if form.is_valid():
    #         form.instance.user=request.user
    #         form.save()
    #         messages.success(request,"Todo Added Successfully")
    #         return redirect('all-todo')
    #     messages.error(request,"Faild to Create Todo")
    #     return render(request,self.template_name,{"form":form})



@method_decorator(decks,name='dispatch')
class TodoListView(ListView):
    model=Tasks
    template_name='todo-list.html'
    context_object_name="tasks"
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user).order_by("-created_date")
    
    # def get(self,request,*args, **kwargs):
    #     qs=self.model.objects.filter(user=request.user).order_by("-created_date")
    #     return render(request,self.template_name,{"tasks":qs})
    

@method_decorator(decks,name='dispatch')
class TodoTrueView(View):
    def get(self, request, *args, **kwargs):
        id = kwargs.get("pk")
        Tasks.objects.filter(id=id).update(status=True)
        return redirect('all-todo')


@method_decorator(decks,name='dispatch')
class TodoDetailView(DetailView):
    template_name='todo-detail.html'
    model=Tasks
    context_object_name="task"
    

    # def get(self,request,*args, **kwargs):
    #     id=kwargs.get("pk")
    #     qs=Tasks.objects.get(id=id)
    #     return render(request,self.template_name,{"task":qs})



@method_decorator(decks,name='dispatch')
class TodoEditView(UpdateView):
    template_name='todo-edit.html'
    form_class=TodoChangeForm
    model=Tasks
    success_url=reverse_lazy('all-todo')

    def form_valid(self, form):
        messages.success(self.request,"Todo has been Updated")
        return super().form_valid(form)
    def form_invalid(self, form):
        messages.error(self.request,"Todo Updation Faild")
        return super().form_invalid(form)


    # def get(self,request,*args, **kwargs):
    #     id=kwargs.get('pk')
    #     obj=Tasks.objects.get(id=id)
    #     form=self.form_class(instance=obj)
    #     return render(request,self.template_name,{"form":form})
    # def post(self,request,*args, **kwargs):
    #     id=kwargs.get('pk')
    #     obj=Tasks.objects.get(id=id)
    #     form=self.form_class(instance=obj,data=request.POST)
    #     if form.is_valid():
    #         form.save()
    #         messages.success(request,"Todo has been Updated")
    #         return redirect('all-todo')
    #     return render(request,self.template_name,{"form":form})
    


@sign_required
def todo_delete(request,*args, **kwargs):
    id=kwargs.get('pk')
    obj=Tasks.objects.get(id=id) 
    if request.user ==  obj.user:
        Tasks.objects.get(id=id).delete()
        return redirect('all-todo')
    else:
        messages.error(request,"You have not permission to delete this content")
        return redirect('all-todo')

class ForgotView(FormView):
    model=User
    form_class=ForgotForm
    template_name='reset-pass.html'

    def post(self,request,*args, **kwargs):
        form=self.form_class(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get("username")
            email=form.cleaned_data.get("email")
            pwd1=form.cleaned_data.get("password1")
            pwd2=form.cleaned_data.get("password2")
            if pwd1==pwd2:
                try:
                    usr=User.objects.get(username=username,email=email)
                    usr.set_password(pwd1)
                    usr.save()
                    messages.success(request,"passwoed changed")
                    return redirect('login')
                except Exception as e:
                    messages.error(request,"invalid credential")
                    return render(request,self.template_name,{"form":form})
            else:
                messages.error(request,"password mismatch") 
                return render(request,self.template_name,{"form":form})   
    
