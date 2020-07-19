IMG_NAME = tuiplot
CONTAINER_NAME = tuiplot

build:
	docker build -t $(IMG_NAME) .

run:
	docker run -td --name $(CONTAINER_NAME) $(IMG_NAME)
	docker cp src $(CONTAINER_NAME):/root
	-docker exec -it $(CONTAINER_NAME) python src/main.py
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)

start:
	docker run -td --name $(CONTAINER_NAME) $(IMG_NAME)
	docker cp src $(CONTAINER_NAME):/root
	docker exec -it $(CONTAINER_NAME) python src/main.py

stop:
	docker stop $(CONTAINER_NAME)
	docker rm $(CONTAINER_NAME)
