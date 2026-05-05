# How to run
1. pip install -r requirements.txt
 edit the password in database.py line 11
mysql -u root -p < schema.sql
mysql -u root -p < data.sql
python main.py