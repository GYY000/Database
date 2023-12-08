import os
import time

# 云端数据库配置
cloud_db_config = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'db21373122',
    'USER': '21373122',
    'PASSWORD': 'Aa108174',
    'HOST': '120.46.80.149',
    'PORT': '',
}

# 本地数据库配置
local_db_config = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'db_homework',
        'USER': 'root',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '3306'
    },
}


option = 'download'

if option == 'upload':
    os.system("python manage.py dumpdata > data.json")
    db_settings_file = open("WGZForce/db_settings.py", "w")
    db_settings_file.write('''
now_database = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'db21373122',
    'USER': '21373122',
    'PASSWORD': 'Aa108174',
    'HOST': '120.46.80.149',
    'PORT': '',
}
''')
    db_settings_file.close()
    os.system("python.exe manage.py makemigrations")
    os.system("python manage.py migrate")
    os.system("manage.py loaddata data.json")
    print("数据已经迁移到云端！")

elif option == 'download':
    os.system("python manage.py dumpdata > data.json")
    db_settings_file = open("WGZForce/db_settings.py", "w")
    db_settings_file.write('''
now_database = {
    'ENGINE': 'django.db.backends.mysql',
    'NAME': 'db_homework',
    'USER': 'root',
    'PASSWORD': '123456',
    'HOST': 'localhost',
    'PORT': '3306'
}
''')
    db_settings_file.close()
    os.system("python.exe manage.py makemigrations")
    os.system("python manage.py migrate")
    os.system("manage.py loaddata data.json")
    print("数据已经下载到云端！")