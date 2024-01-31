build:
	docker build -f Scrappy/Dockerfile -t "scrappy:latest" Scrappy
	sam build --use-container

invoke:
	sam local invoke ScrappyFunction --event event.json > site.json
