from django.shortcuts import render
from firstRESTapi.serializers import tweetSerialize, Register, tweetUserSerialize, BestTweetUserSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import tweet
from django.http import Http404
from .forms import TweetForm
from django.http import HttpResponse
from rest_framework_jwt.settings import api_settings
from django.contrib.auth import authenticate, get_user_model
# Create your views here.
import json
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from .permission import AlreadyAuthenticated, IsOwnerOrReadOnly
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.mixins import CreateModelMixin, RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.generics import (ListAPIView, CreateAPIView, UpdateAPIView, RetrieveAPIView, DestroyAPIView,
                                     ListCreateAPIView, RetrieveUpdateDestroyAPIView)

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


def formcheck(request):
    template = "Form.html"
    form = TweetForm(request.POST or None)
    context = {"form": form}
    if form.is_valid():
        print(form)
        f = form.save(commit=False)
        f.User = request.user
        f.save()
        return HttpResponse("Yeah done")
    return render(request, template, context)


class Authview(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        print(request.user)
        print(request.user.is_authenticated)
        if request.user.is_authenticated:
            return Response({"Detail": "User is already Autheticated go ahead use other API's"})
        else:
            username = request.POST.get("username", None)
            password = request.POST.get("password", None)
            Email = request.POST.get("email", None)
            user = authenticate(
                request, username=username or Email, password=password)
            if user is not None:
                payload = jwt_payload_handler(user)
                token = jwt_encode_handler(payload)
                tokenized = {
                    "token": token
                }
        return Response(tokenized)


class registerview(APIView):
    permission_classes = [AlreadyAuthenticated]

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return Response({"Detail": "Sorry alreadrregistered and authenticated"})
        else:
            user = get_user_model()
            data = request.data
            obj = user.objects.create(username=data.get(
                "username", None), email=data.get(
                "email", None))
            obj.set_password(data.get("password", None))
            obj.save()
            print(obj)
            payload = jwt_payload_handler(obj)
            token = jwt_encode_handler(payload)
            tokenized = {
                "token": token
            }
        return Response({"token": tokenized})


class registerserview(CreateAPIView):
    permission_classes = [AlreadyAuthenticated]
    serializer_class = Register

    def get_serializer_context(self, *args, **kwargs):
        return({"request": self.request.user})


class GetListObj(APIView):
    # authentication_classes = [SessionAuthentication, BasicAuthentication]
    # if user is not auth it will return
    # permission_classes = [IsAuthenticated]
    # permission_classes = [IsAuthenticatedOrReadOnly]
    # it will allow the user to readonly they cant post,put,patch,delete
    # {
    #     "detail": "Authentication credentials were not provided."
    # }
    # If not specified, this setting defaults to allowing unrestricted access:
    # Default Permission is AllowAny [AllowAny]

    def get(self, request, format=None):
        qs = tweet.objects.all()
        serialized = tweetSerialize(qs, many=True)
        return Response(serialized.data)


user = get_user_model()


class listapi(ListAPIView):
    # Tweet serializer have nestedSerializers a user model
    serializer_class = BestTweetUserSerializer
    # queryset = tweet.objects.all()

    def get_queryset(self, *args, **kwargs):
        qs = user.objects.all()
        return qs


class create(CreateAPIView):
    serializer_class = tweetSerialize  # only tweet Serializer
    queryset = tweet.objects.filter(Title__icontains="ooooo")


class UpdateViews(UpdateAPIView):
    serializer_class = tweetSerialize
    queryset = tweet.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "Title"

    # def get_queryset(self):
    #     querset = tweet.objects.filter(Title__icontains="My")
    #     return querset

    # def get_object(self, *args, **kwargs):
    #     qs = self.get_queryset()
    #     try:
    #         obj = qs.get(id=self.kwargs["Title"])
    #     except:
    #         obj = None
    #         raise Http404("No object found matching this query")
    #     return obj


class detail(RetrieveAPIView):
    serializer_class = tweetSerialize
    queryset = tweet.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "fun"


class deletes(DestroyAPIView):
    serializer_class = tweetSerialize
    queryset = tweet.objects.all()
    lookup_field = "id"
    lookup_url_kwarg = "fun"


class listcreate(ListCreateAPIView):
    queryset = tweet.objects.all()
    serializer_class = tweetSerialize


class mixinlistCreate(CreateModelMixin, ListAPIView):
    queryset = tweet.objects.all()
    serializer_class = tweetSerialize

    def post(self, request, *args, **kwargs):
        # if we use mixin we need to ue the http methods and return inbuilt methods of drf
        return self.create(request, *args, **kwargs)


class retUpdDel(RetrieveUpdateDestroyAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    queryset = tweet.objects.all()
    serializer_class = tweetSerialize
    lookup_field = "id"
    lookup_url_kwarg = "common"


class oneEndpoint(DestroyModelMixin, UpdateModelMixin, RetrieveModelMixin, CreateModelMixin, ListAPIView):
    permission_classes = [IsOwnerOrReadOnly]
    serializer_class = tweetSerialize

    def get_queryset(self, *args, **kwargs):
        qs = tweet.objects.all()
        return qs

    def get_object(self, *args, **kwargs):
        getRequest = self.request.GET.get("id", None)
        # getJson = json.loads(self.request.body)
        getJson = self.request.data
        getData = getJson.get("id", None)
        finalData = getRequest or getData
        if(finalData is not None):
            try:
                getobj = tweet.objects.get(id=finalData)
                # self.check_object_permissions(self.request, getobj)
                print(getobj.Owner)
                print(self.request.user)
            except:
                print("Came inside Not Found")
                raise Http404("NotFound")
        return getobj

    def get(self, request, *args, **kwargs):
        print(request.GET)
        # print(request.data)
        # django.http.request.RawPostDataException: You cannot access body after reading from request's data stream
        # meant cannot use request.body after using request.data
        # request.Data-->Will automatically change the format which python required
        # if input jsonstring request.data will automatically change to dict not needed to use json.loads()
        print(request.data)
        print(type(request.data))  # dict
        # print(type(request.body)) #bytes (JsonString)
        # request.body will not change the format of the input data to the datatype which python can handle Say
        # input jsonstring has to loaded with json.loads() for the python dtype Dict
        # getJson = json.loads(request.body)
        # print(getJson)
        getJson = request.data
        getData = getJson.get("id", None)
        print(getData)
        getRequest = request.GET.get("id", None)
        # jsonreq=
        finalData = getRequest or getData
        if(finalData is not None):
            return self.retrieve(request, *args, **kwargs)
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)
