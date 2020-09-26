from rest_framework import serializers
from .models import tweet
from django.contrib.auth import get_user_model
from rest_framework_jwt.settings import api_settings
from .permission import AlreadyAuthenticated
User = get_user_model()

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER


class Register(serializers.ModelSerializer):
    # password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)
    token = serializers.SerializerMethodField(read_only=True)
    message = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = User
        fields = ["username", "email", "password",
                  "password2", "token", "message"]

    def validate(self, data):
        # print(data)
        pw2 = data.pop("password2")
        pw1 = data.get("password")
        # print(data)
        if(pw2 == pw1):
            return data
        else:
            raise serializers.ValidationError("Sorry Password should match")

    def get_message(self, obj):
        context = self.context
        name = context["request"]
        return (str(name)+" Thanks for registering..")

    def get_token(self, obj):
        user = obj
        payload = jwt_payload_handler(user)
        token = jwt_encode_handler(payload)
        return token

        # {"username":"ProperToken","email":"Chivo@gmail.com",
        # "password":"pbkdf2_sha256$180000$4sS1RvrERTip$lD79+hoooXNwDrZIWALz8sK6nHqm2SZPjmIyhG1oyVA=",
        # "token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxNSwidXNlcm5hbWUiOiJQcm9wZXJUb2tlbiIsImV4cCI6MTU5NDA2OTUzMCwiZW1haWwiOiJDaGl2b0BnbWFpbC5jb20ifQ.Do72-GaylbrL853XNp1qWUVVTlHG-7R45IMvVdK1JAc"
        #  ,"message":"AnonymousUser Thanks for registering.."}

        # get_fieldname will add the fields into the final return Response with username email password and our getToken

    def validate_username(self, value):
        if(value == "ABC"):
            raise serializers.ValidationError("Sorry Username should valid")
        else:
            return value

    def create(self, validated_data):
        print(validated_data)
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
        ]


class BestTweetUserSerializer(serializers.ModelSerializer):
    Tweet = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "Tweet"
        ]

    def get_Tweet(self, obj):
        # qs = User.objects.prefetch_related("tweet_set").all()
        # print(qs)
        qs = obj.tweet_set.all()
        print(qs)
        ser = tweetSerialize(qs, many=True)
        recent = obj.tweet_set.all().order_by("-id")
        re = tweetSerialize(recent.first()).data
        # print("hello")
        print(recent)
        Tweets = {
            "uri": "listapi/"+str(obj.id),
            "Recent_tweet": re,
            "All_Tweets": ser.data
        }
        return Tweets


class tweetUserSerialize(serializers.ModelSerializer):
    User = UserSerializer()

    class Meta:
        model = tweet
        fields = [
            "id",
            "User",
            "Title",
            "content",
            "image",
        ]

    def validate_Title(self, value):
        if(len(value) < 5):
            raise serializers.ValidationError(
                "Sorry Title for tweeting is too short")
        return value

    def validate_content(self, value):
        if(len(value) > 100):
            raise serializers.ValidationError(
                "Sorry Content is too long")
        return value

    def validate(self, data):
        # checking=self.validated_data.get("Title",None)
        # print(checking)
        checking = data.get("Title", None)
        content = data.get("content", None)
        if(checking != content):
            pass
        else:
            raise serializers.ValidationError("Sorry No Luck")
        print(data)
        return data


class tweetSerialize(serializers.ModelSerializer):
    class Meta:
        model = tweet
        fields = [
            "id",
            "Title",
            "content",
            "image",
        ]

    def validate_Title(self, value):
        if(len(value) < 5):
            raise serializers.ValidationError(
                "Sorry Title for tweeting is too short")
        return value

    def validate_content(self, value):
        if(len(value) > 100):
            raise serializers.ValidationError(
                "Sorry Content is too long")
        return value

    def validate(self, data):
        # checking=self.validated_data.get("Title",None)
        # print(checking)
        checking = data.get("Title", None)
        content = data.get("content", None)
        if(checking != content):
            pass
        else:
            raise serializers.ValidationError("Sorry No Luck")
        print(data)
        return data
