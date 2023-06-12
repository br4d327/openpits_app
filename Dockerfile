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
COPY . .
RUN pwd
RUN cat /etc/group | grep user
RUN sudo chmod 777 data/
RUN chown -R user /app/model
CMD streamlit run main.py
