FROM anibali/pytorch:2.0.0-cuda11.8
EXPOSE 8501
WORKDIR /model
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
COPY . .
CMD streamlit run main.py