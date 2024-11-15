echo "BUILD START"
python3.9 -m pip3 install -r requirements.txt
python3.9 -m manage.py collectstatic -r --noinput --clear
echo "BUILD END"