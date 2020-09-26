import requests
import json
data = {
    "id": 4,
    "User": 1,
    "Title": "Title From the Post requests Changed using put",
    "content": "This Content is Changed using put",
}
# data = { Ued this for patch request trying to patch the Title in the respective id
#     "id": 10,
#     "User": 1, this is manadatory field need to pass this compulsory other wise field required will pop
#     "Title": "Title From the Post requests Changed using Patch",
# }
headers = {"content-type": "application/json"}
jsonData = json.dumps(data)
primary_URL = "http://127.0.0.1:8000/"
EndPoint = "comm/1/"
AuthEndPoint2 = "auth/"
id = 2
# res = requests.delete(primary_URL+EndPoint,
#                    data=jsonData, headers=headers)
# res = requests.get(primary_URL+EndPoint,
#                    data=jsonData, headers=headers)  # returns authentication required
# due to we set auth classess we cannot access django rest with extenral thing meant
#    other that django
# res = requests.get(primary_URL+EndPoint+"?id="+str(id),data = jsonData, headers = headers) if request.GET.get("id",None)
# if you need to pass your kwargs thru URL Not in Json
# print(res)
# print(res.text)

# how to autheticate my external python requests with django restapi

# basicauthetication of django restapi will not wotk only works if access thru django
# so we are going to use thirdparty package jwt(json Web Authentication)
# Library we are using was djangorestframework-jwt check the site and set things then

AuthEndPoint = "api-token-auth/"

# Login_data = {
#     "username": "chivo2",
#     "password": "Chivo@07"
# }
# register_data = {
#     "username": "ProperToken6",
#     "password": "Chivo@07",
#     "password2": "Chivo@07",
#     "email": "Chivo@gmail.com"
# }
login_data = {
    "username": "ProperToken",
    "password": "Chivo@07"
}
data = {
    "id": 1,
    "Title": "This can be Updated if you are an owner"
}
jsonData = json.dumps(data)
# headers1 = {
#     "content-type": "application/json",
#     # note: Single Space must present btwn JWT and Token
#     "Authorization": "JWT "+"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxOSwidXNlcm5hbWUiOiJQcm9wZXJUb2tlbjUiLCJleHAiOjE1OTQwNzI2NjcsImVtYWlsIjoiQ2hpdm9AZ21haWwuY29tIn0.Ukdo1TOvvqwwWPiTAJ20O77Eqi22mQHrGwVxVjvmaI0",
# } #{"detail":"Sorry You are already authenticated"} --->CustomPermisiions this view can only access by new users
# do going to post this credential to that apitoken view to check its valid
# this view going to take input of username and pwd from external source if correct it will generate a token
# If wrong cred it will raise not able to login

check = requests.post(primary_URL+AuthEndPoint2,
                      data=login_data)  # , headers=headers1
print(check.text)
tokenGen = check.json()
tokenGen = tokenGen["token"]
print(tokenGen)
# print(check.text)
# if valid return this
# {"token":"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxLCJ1c2VybmFtZSI6ImNoaXZvIiwiZXhwIjoxNTkzOTQ1Njk0LCJlbWFpbCI6IiJ9.fRpRdZOEOJ9y4Yg2yCpvgRqLuykLwVU1veMGcUk4XWE"}
# if not valid cred response is {"non_field_errors":["Unable to log in with provided credentials."]}
# so before accessing the RESTAPI we should send these tokens with our post data through headers

headers1 = {
    "content-type": "application/json",
    # note: Single Space must present btwn JWT and Token
    "Authorization": "JWT "+tokenGen,
}
# print(headers1["Authorization"])
res = requests.put(primary_URL+EndPoint,
                   data=jsonData, headers=headers1)
print(res.text)
