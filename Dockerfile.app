FROM centos:8

RUN yum update -y && \
    yum install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p $HOME/miniconda && \
    $HOME/miniconda/bin/conda install -y bokeh

COPY bokeh/test_app.py /root/test_app.py

CMD [ "/root/miniconda/bin/bokeh", "serve", "/root/test_app.py", "--port", "8888", "--allow-websocket-origin=localhost:80"]