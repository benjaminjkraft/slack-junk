deploy:
	pip install -r requirements.txt -t lib
	gcloud app deploy app.yaml --project slack-junk --account benjaminjkraft@gmail.com
