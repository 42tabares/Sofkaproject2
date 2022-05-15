from django.shortcuts import redirect, render
from .models import *
from random import shuffle
from .scripts import get_or_none


def startpage(request):

    Players = Player.objects.all()
    players = Players.order_by('highscore')
    
    return render(request, 'startpage.html',{"Players":players})


def startgame(request):
    
    player = request.POST.get("Player")

    if get_or_none(Player, name=player):
        player = Player.objects.get(name=player)
    else:
        Player.objects.create(name = player)
        player = Player.objects.get(name=player)
    
    player.score = 0
    player.save()

    return redirect('/lvl/1/%s/0/'%(player.name))



def answercheck(request, question, answer, player, level, questionnum):
    
    player = Player.objects.get(name=player)
    question = Question.objects.get(id = question)

    if answer == question.answer1:
        player.score += question.points
        player.save()
        return redirect('/lvl/%s/%s/%s'%(level,player.name,questionnum))
    else:
        player.score = 0
        player.save()
        return redirect('/endgame/%s/%s'%(player.name,level))


def gamepage(request, level, player, questionnum):

    question = Question.getrandom(level)
    answers = [Question.answer1, Question.answer2, Question.answer3, Question.answer4]
    shuffle(answers)
    
    if questionnum == 5:
        level += 1
        questionnum = 1
    elif level != 6: 
        questionnum += 1
    else:
        return redirect('/endgame/%s/%s'%(player.name,level))

    return render(request, 'gamepage.html', {
        "Player"    :player,
        "Question"  :question,
        "Answers"   :answers,
        "Level"     :level,
        "Questionnum":questionnum
        })

def endpage(request, player, level):

    player = Player.objects.get(name=player)

    if player.points != 0:

        if player.highscore < player.points:
            player.highscore = player.points
        
        
        if level>5:
            won = True

        lost = False

    else:
        lost = True

    render(request, 'endpage.html',{"Player":player,"Lost":lost,"Won":won})

# Create your views here.
