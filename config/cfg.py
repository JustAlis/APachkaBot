HOST = '127.0.0.1'
PORT = 6666

BOT_TOKEN = ""

#Dont touch! These are not supposed to be changed!
BASE_API_URL = 'https://api.pachca.com/api/shared/v1'
AUTH_VIA_BOT_TOKEN = "Bearer "+BOT_TOKEN
HEADERS_AUTH = {"Authorization": AUTH_VIA_BOT_TOKEN}

#Api routs
MESSEGE_URL = BASE_API_URL+'/messages/'
TASK_URL = BASE_API_URL+'/tasks/'