from neutrino.account.models import DefaultUser , InfoProfileUser

def get_username_info(username): 
    response = InfoProfileUser.objects.only( # TODO add validation for sql injection
    "profile_info" , 'posts_count' , 'subscriber_count' , 'subscription_count' , 'bio'
    ).get(
        profile_info__username = username

    ) 
    return response 

    