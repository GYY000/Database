import os
import time
import sys
option = sys.argv[1]

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
    'NAME': 'tempdb',
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
    print("数据已经下载到本地！")
else:
    print("非法命令")