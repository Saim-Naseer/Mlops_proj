Now in order to run

just do

```
sudo systemctl start docker

sudo docker-compose up --build
```

after this on localhost:3000 there will be frontend to add data and it will generate prediction by contacting backend at localhost:8000 interacting with mlflow ui at localhost:5000