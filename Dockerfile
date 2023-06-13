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

RUN sudo chmod 777 data/
RUN sudo chmod 777 models/
RUN cd ..
RUN ls -la

RUN sudo git config user.email "bassertils@gmail.com"
RUN sudo git config user.name "Basserti"

CMD echo 'DOCKER START'
