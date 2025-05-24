from django.contrib.auth import get_user_model
user = get_user_model()


def Create_user(data): 
    return user.objects.create_user(
        username=data.get('username') , 
        email= data.get('email') , 
        password= data.get('password')
    )
