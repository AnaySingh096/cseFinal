import random

numOfParticipants =3
lengthOfPassword = 10

list = ['1','2','3','4','5','6','7','8','9','0',"q","w","e","r",'t','y','u','i','o','p','a','s','d','f','g','h','j','k','l','z','x','c','v','b','n','m','Q','W','E','R','T','Y','U','I','O','P','A','S','D','F','G','H','J','K','L','Z','X','C','V','B','N','M']

for i in range(0,numOfParticipants,1):
    password = ""
    for j in range(0, lengthOfPassword, 1):
        password = password+ random.choice(list)
    print(password)