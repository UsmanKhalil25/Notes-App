from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status
from .models import Note
from .serializers import NoteSerializer
# Create your views here.
@api_view(["GET"])
def getRoutes(request):
    routes = [
        {
            "Endpoint":"/notes/",
            "method":"GET",
            "body":None,
        },
        {
            "Endpoint":"/notes/id",
            "method":"GET",
            "body":None,
        },
        {
            "Endpoint":"/notes/create/",
            "method":"POST",
            "body":{"body":""},
        },
        {
            "Endpoint":"/notes/id/update/",
            "method":"POST",
            "body":{"body":""},
        },
        {
            "Endpoint":"/notes/id/delete/",
            "method":"DELETE",
            "body":None
        },

    ]

    return Response(routes)


@api_view(["GET"])
def getNotes(request):
    notes = Note.objects.all().order_by("-updated")
    serializer = NoteSerializer(notes,many = True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["GET"])
def getNote(request,pk):
    try:
        note = Note.objects.get(id = pk)
    except Note.DoesNotExist:
        return Response({"Error":"Not found"},status=status.HTTP_404_NOT_FOUND)
    serializer =NoteSerializer(note,many = False)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["POST"])
def createNote(request):
    data = request.data
    note = Note.objects.create(
        body = data['body']
    )
    serializer = NoteSerializer(note,many = False)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data,status=status.HTTP_200_OK)
    return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


@api_view(["PUT"])
def updateNote(request,pk):
    data = request.data
    try:
        note= Note.objects.get(id = pk)
    except Note.DoesNotExist:
        return Response({"Error":"Not found"}, status=status.HTTP_404_NOT_FOUND)
    serializer = NoteSerializer(instance = note,data=data,many = False)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data,status.HTTP_200_OK)

@api_view(["DELETE"])
def deleteNote(request,pk):
    try:
        note = Note.objects.get(id = pk)
    except Note.DoesNotExist:
        Response({"Error":"Not Found"},status = status.HTTP_404_NOT_FOUND)

    note.delete()
    return Response({"Message":"Note deleted"},status=status.HTTP_200_OK)
    