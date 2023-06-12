FROM anibali/pytorch:2.0.0-cuda11.8

ENV TZ=UTC
RUN sudo ln -snf /usr/share/zoneinfo/$TZ /etc/localtime

RUN sudo apt-get update \
 && sudo apt-get install -y libgl1-mesa-glx libgtk2.0-0 libsm6 libxext6 \
 && sudo rm -rf /var/lib/apt/lists/*

RUN sudo apt-get install git  

RUN sudo wget \
       https://dvc.org/deb/dvc.list \
       -O /etc/apt/sources.list.d/dvc.list 
RUN sudo wget -qO - https://dvc.org/deb/iterative.asc | gpg --dearmor > packages.iterative.gpg 
RUN sudo install -o root -g root -m 644 packages.iterative.gpg /etc/apt/trusted.gpg.d/ 
RUN rm -f packages.iterative.gpg 
RUN sudo apt-get update 
RUN sudo apt-get install dvc

EXPOSE 8501
WORKDIR model
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
RUN pip install dvc
COPY . .

RUN sudo dvc pull
RUN sudo chmod 777 data/
RUN sudo chmod 777 models/
RUN ls -la
RUN python3 model_train.py
RUN ls -la
RUN ./script.sh
RUN ls -la

CMD streamlit run main.py
