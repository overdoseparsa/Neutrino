
LOGGING = {
       'version': 1,

       'disable_existing_loggers': False,

       'formatters': {
           'verbose': {
               'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
               'style': '{',
           },
           'simple': {
               'format': '{levelname} {asctime} {message}',
               'style': '{',
           },

       },

       'handlers': {
           'console_otp_logs': {
               'level': 'INFO',
               'class': 'logging.StreamHandler',
               'formatter': 'simple'
           },
           'sms_file_otp_logs': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'logs/otp_sms.log',
               'formatter': 'verbose'
           },
            'mail_file_otp_logs': {
               'level': 'DEBUG',
               'class': 'logging.FileHandler',
               'filename': 'logs/otp_mail.log',
               'formatter': 'verbose'
           },
            'middleware_logs_file':{
                'level':'DEBUG' ,
                'class': 'logging.FileHandler',
                'filename': 'logs/middleware.log',
                'formatter': 'verbose'  ,
            }
            
       },
       'loggers': {
           'Mailotp': {
               'handlers': ['console_otp_logs', 'mail_file_otp_logs'],
               'level': 'DEBUG',
               'propagate': True,
           },
            'SmsOtp': {
               'handlers': ['console_otp_logs', 'sms_file_otp_logs'],
               'level': 'DEBUG',
               'propagate': True,
           },
            'middlewarelogs': {
               'handlers': ['middleware_logs_file'],
               'level': 'DEBUG',
               'propagate': True,
           },
       
            'SmsSendApilogs':{
                'handlers':['console_otp_logs'] ,
                'level':'DEBUG', 
                'propagate':True} , 

       
       },
   }


"""
{} style logs 
{}  handeler for logs 


"""
