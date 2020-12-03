FROM centos:8

RUN yum update -y && \
    yum install -y wget && \
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && \
    bash ~/miniconda.sh -b -p $HOME/miniconda && \
    $HOME/miniconda/bin/conda install -y bokeh pandas matplotlib

COPY bokeh /root/app

CMD [ "/root/miniconda/bin/bokeh", "serve", "/root/app/data", "/root/app/map_visualization", "--port", "8888", "--allow-websocket-origin=toxic-metals.dartmouth.edu:80"]
