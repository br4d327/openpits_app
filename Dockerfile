FROM anibali/pytorch:2.0.0-cuda11.8

ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN sudo apt-get update \
 && sudo apt-get install -y libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
 && sudo rm -rf /var/lib/apt/lists/*

EXPOSE 8501
WORKDIR model
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install dvc[gdrive]
RUN pip install PyDrive2
COPY . .

RUN sudo chmod -R 777 data/
RUN sudo chmod -R 777 models/
RUN sudo chmod -R 777 .dvc
RUN sudo chmod -R 777 .dvcignore
RUN sudo chmod -R 777 .git
RUN sudo chmod -R 777 .github
RUN sudo chmod -R 777 .gitignore
RUN sudo chmod -R 777 main.py
RUN sudo chmod -R 777 model_train.py
RUN sudo chmod -R 777 test_example/

RUN sudo git config user.email "bassertils@gmail.com"
RUN sudo git config user.name "Basserti"

CMD echo 'DOCKER START'
