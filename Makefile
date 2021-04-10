test:
	pytest test.py

venv:
	(python -m venv venv && source venv/Scripts/activate && pip install -r requirements.txt)

clean:
	rm -rf ./venv

request:
	curl -X POST -H "Content-Type: application/json" -d "{ \"key1\": \"value1\" }" http://127.0.0.1:5000/  

serve:
	FLASK_APP=application.py FLASK_ENV=development flask run