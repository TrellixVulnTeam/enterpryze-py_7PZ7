title Installing dependencies for EnterpRyze
call env\Scripts\activate.bat
cls
pip install -U discord.py[voice]
pip install pymongo
pip install pynacl
pip install youtube_dl
pause