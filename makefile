install:
	pip install -r Scrappy/requirements.txt
	pip install -r tests/requirements.txt

build:
	docker build -f Scrappy/Dockerfile -t "scrappy:latest" Scrappy
	sam build --use-container

invokeclub:
	sam local invoke ScrappyFunction --event event_clubv1.json > site.json

invokebrs:
	sam local invoke ScrappyFunction --event event_brs.json > site.json

deploy:
	sam build --use-container
	sam deploy --profile speakcloud