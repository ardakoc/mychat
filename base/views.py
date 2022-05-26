import json
import random

from time import time

from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from agora_token_builder import RtcTokenBuilder

from .models import RoomMember

# Create your views here.

def getToken(request):
  appId = '2b77f51824144fdc91de0fa5d840b172'
  appCertificate = 'd1df85e9b0ea48379375996b9df82ae6'
  channelName = request.GET.get('channel')
  uid = random.randint(1,230)
  role = 1 # set this 1 for host and 2 for guest
  expirationTimeInSeconds = 3600 * 24
  currentTimeStamp = time()
  privilegeExpiredTs = currentTimeStamp + expirationTimeInSeconds

  token = RtcTokenBuilder.buildTokenWithUid(appId, appCertificate, channelName, uid, role, privilegeExpiredTs)
  return JsonResponse({'token': token, 'uid': uid}, safe=False)


def lobby(request):
  return render(request, 'base/lobby.html')


def room(request):
  return render(request, 'base/room.html')


@csrf_exempt
def createMember(request):
  data = json.loads(request.body)
  member, created = RoomMember.objects.get_or_create(
    name = data['name'],
    uid = data['UID'],
    room_name = data['room_name'],
  )
  return JsonResponse({'name': data['name']}, safe=False)


def getMember(request):
  uid = request.GET.get('UID')
  room_name = request.GET.get('room_name')

  member = RoomMember.objects.get(
    uid=uid,
    room_name=room_name, 
  )

  name = member.name
  return JsonResponse({'name': name}, safe=False)

@csrf_exempt
def deleteMember(request):
  data = json.loads(request.body)
  member = RoomMember.objects.get(
    name = data['name'],
    uid = data['UID'],
    room_name = data['room_name'],
  )
  member.delete()
  return JsonResponse(member + ' was deleted.', safe=False)