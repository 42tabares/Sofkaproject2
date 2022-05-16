from django.shortcuts import redirect, render
from .models import *
from random import shuffle
from .scripts import get_or_none


def startpage(request):

    Players = Player.objects.all()
    players = Players.order_by('-highscore')
    
    return render(request, 'startpage.html',{"Players":players})


def startgame(request):
    
    player = request.POST.get("Player")

    #Requests the playername from the saved players, if it doesnt exists creates a new Player#
    if get_or_none(Player, name=player):
        player = Player.objects.get(name=player)
    else:
        Player.objects.create(name = player)
        player = Player.objects.get(name=player)
    
    
    #Restoring Questions called signals and player score#
    Qset = Question.objects.all()
    for q in Qset:
        q.called = False
        q.save()
    player.score = 0
    player.save()

    return redirect('/lvl/1/%s/1'%(player.name))


def answercheck(request):
    
    playername    = request.POST.get("playername")
    answer        = request.POST.get("answer")
    questionid    = request.POST.get("questionid")
    questionnum   = request.POST.get("questionnum")
    level         = request.POST.get("level")

    player   = Player.objects.get(name = playername)
    question = Question.objects.get(id = questionid)
    

    #Checks if answer matches the Question's correct respone, if not, it requests the ENDGAME#
    if answer == question.answer1:
        player.score += question.points
        player.save()
        return redirect('/lvl/%s/%s/%s/'%(level,player.name,questionnum))
    else:
        player.score = 0
        player.save()
        return redirect('/endgame/%s/%s/'%(player.name,level))


def gamepage(request, level, player, questionnum):

    questionnum=int(questionnum)
    level=int(level)
    player = Player.objects.get(name=player)

    #checks that the player hasn't got to the end yet
    if level == 6:
        return redirect('/endgame/%s/%s/'%(player.name,level)) 


    #Gets a random question of a specified difficulty level that has not been used yet#
    QSet = Question.objects.filter(called = False, difficulty = level)
    question = QSet.order_by('?').first() 
    question.called = True
    question.save()

    #Mixes up the order in which responses are displayed so that the fist answer isnt always the correct#
    answers = [question.answer1, question.answer2, question.answer3, question.answer4]
    shuffle(answers)
    
    #Keeps track of the question Number per level and the level too#

    if questionnum == 5:
        level += 1
        questionnum = 1
    else:
        questionnum += 1

    return render(request, 'gamepage.html', {
        "Player"    :player,
        "Question"  :question,
        "Answers"   :answers,
        "Level"     :level,
        "Questionnum":questionnum
        })

def endpage(request, player, level):

    player = Player.objects.get(name=player)
    won = False


    #Sets up the ENDPAGE for the three posible cases: lost, retired or won#
    if player.score != 0:
        
        if player.highscore < player.score:
            player.highscore = player.score
            player.save()
        
        level=int(level)
        if level>5:
            won = True

        lost = False

    else:
        lost = True

    return render(request, 'endpage.html',{"Player":player,"Lost":lost,"Won":won})

# Create your views here.
