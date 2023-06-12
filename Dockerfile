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

RUN sudo git config user.email "bassertils@gmail.com"
RUN sudo git config user.name "Basserti"

RUN mkdir -p /home/user/.cache/pydrive2fs/710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com/

CMD echo '{"access_token": "ya29.a0AWY7CkliiUGTq3jzv52nHU7RRkpriHWQ6_Hjxqhzlun6KWVXSXAbJ9IlYhEGXA9lHNv10zz9RL-6dlVhrGdgLEOGetue2BYZTNAN6y915uhfz1xfAi_qt3YVesY_x7U2cYQCYs5xJQAKaPK9lPdU0K4OkayXYPVoaCgYKAcgSARISFQG1tDrpBOJ6zY_gB24ivs2i9WUC8w0167", "client_id": "710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com", "client_secret": "a1Fz59uTpVNeG_VGuSKDLJXv", "refresh_token": "1//0cGkRHqUJKz8aCgYIARAAGAwSNwF-L9IruPGFRBgQ5ROyIhmgyrkaZyaGTXLhnEnItE-hv6V3f8hqnOP_yWLh80zkamvtsUu-y9g", "token_expiry": "2023-06-12T15:37:30Z", "token_uri": "https://oauth2.googleapis.com/token", "user_agent": null, "revoke_uri": "https://oauth2.googleapis.com/revoke", "id_token": null, "id_token_jwt": null, "token_response": {"access_token": "ya29.a0AWY7CkliiUGTq3jzv52nHU7RRkpriHWQ6_Hjxqhzlun6KWVXSXAbJ9IlYhEGXA9lHNv10zz9RL-6dlVhrGdgLEOGetue2BYZTNAN6y915uhfz1xfAi_qt3YVesY_x7U2cYQCYs5xJQAKaPK9lPdU0K4OkayXYPVoaCgYKAcgSARISFQG1tDrpBOJ6zY_gB24ivs2i9WUC8w0167", "expires_in": 3599, "scope": "https://www.googleapis.com/auth/drive.appdata https://www.googleapis.com/auth/drive", "token_type": "Bearer"}, "scopes": ["https://www.googleapis.com/auth/drive", "https://www.googleapis.com/auth/drive.appdata"], "token_info_uri": "https://oauth2.googleapis.com/tokeninfo", "invalid": false, "_class": "OAuth2Credentials", "_module": "oauth2client.client"}' >> /home/user/.cache/pydrive2fs/710796635688-iivsgbgsb6uv1fap6635dhvuei09o66c.apps.googleusercontent.com/default.json && dvc pull && ls /app/model/data/train -la  && python3 model_train.py
