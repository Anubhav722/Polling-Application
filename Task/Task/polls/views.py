from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, Http404
from polls.forms import UserForm, QuestionForm, ChoiceForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from polls.models import Question, Choice
from django.core.urlresolvers import reverse
# Create your views here.
def index(request):
    latest_question_list=Question.objects.all()
    return render(request, 'index.html',{'latest_question_list':latest_question_list})
    
def login_user(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(username=username, password=password)
        
        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/polls/')
            else:
                return HttpResponse('Ur polls account is disabled')
        else:
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse('Invalid login details supplied')
            
    else:
        return render(request, 'login.html', {})
        
        
        
        
        
"""def register(request):
    is_registered=False
    if request.method=='POST':
        form=UserForm(data=request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            username=form.cleaned_data['username']
            password=form.cleaned_data['password']
            user.set_password(password)
            user.save()
            user=authenticate(username=username, password=password)"""
                    
        
def register(request):
    is_registered=False
    if request.method=='POST':
        
        user_form = UserForm(data=request.POST)
        if user_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            
            is_registered = True
        else:
            print user_form.errors
    else:
        user_form = UserForm()
    return render(request,
            'register.html',
            {'user_form': user_form, 'is_registered': is_registered} )
            
            
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/polls/')
    
    
"""def create_question(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    
    else:
        form=QuestionForm(request.POST)
        if form.is_valid():
            question=form.save(commit=False) # Here question is a ForeignKey
            question.user=request.user
            question.save()
            return render(request, 'detail.html', )
            
    return render(request, 'create_question.html', {'form':form})"""
    
    
    
@login_required 
def create_question(request):
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    is_created=False
    question_obj = None
    if request.method == 'POST':
        form=QuestionForm(request.POST)
        if form.is_valid():
            question_obj = form.save(commit=False)
            question_obj.user = request.user
            question_obj.save()
            is_created=True

        else:
            print form.errors
    else:
        form=QuestionForm()
    
    return render(request, "create_question.html",{'form':form, 'is_created':is_created, 'question_obj':question_obj })
    
    
"""@login_required
def add_choices(request, question_id):
    question=get_object_or_404(Question, id=question_id)
    
    is_added=False
    choice_obj=None
    if request.method=='POST':
        form=ChoiceForm(request.POST)
        if form.is_valid():
            choice_obj=form.save(commit=False)
            choice_obj.user=request.user
            choice_obj.save()
            is_added=True
            
        else:
            print form.errors
            
    else:
        form=ChoiceForm()
        
    return render(request, 'add_choices.html', {'form':form, 'is_added':is_added, 'choice_obj':choice_obj, 'question_id':question_id})"""
    
    
    
def add_choices(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    
    if not request.user.is_authenticated():
        return render(request, 'login.html')
    else:
    
        is_added=False
        choice_obj=None
        if request.method=='POST':
            form=ChoiceForm(request.POST)
            if form.is_valid():
                choice_obj=form.save(commit=False)
                
                question=Question.objects.get(id=question_id)
                choice_obj.question=question
                choice_obj.save()
                is_added=True
            
            else:
                print form.errors
            
        else:
            form=ChoiceForm()
        
        return render(request, 'add_choices.html', {'form':form, 'is_added':is_added, 'choice_obj':choice_obj, 'question_id':question_id,})
        


def vote(request, question_id):
    question=get_object_or_404(Question, id=question_id)
    
    if not request.user.is_authenticated():
        return render(request, 'login.html')
        
    else:
        #q=Question.objects.get(id=question_id)
        #if question.choice_set.user_record=='False':
            
            try:
                selected_choice=question.choice_set.get(pk=request.POST['choice'])
                question.choice_set.user_record=True
            except(KeyError, Choice.DoesNotExist):
                return render(request, 'detail.html',{'question':question, 'error_message':"You didn't select a choice"})
            
            else:
                selected_choice.vote_count+=1
                selected_choice.save()
                return HttpResponseRedirect(reverse('polls:result', args=(question.id,)))
        #else:
        #    return HttpResponse('You have already voted')
            
def detail(request, question_id):
    try:
        question=Question.objects.get(pk=question_id)
    except Question.DoesNotExist:
        raise Http404("Question does not exist")
        
    return render(request, 'detail.html', {'question':question})
    
def result(request, question_id):
    question=get_object_or_404(Question, pk=question_id)
    return render(request, 'result.html', {'question':question})
            
            
            
            
            
            
            
            
            
            
            
            