FROM centos

MAINTAINER maojingwen  mao_jingwen@icekredit.com

WORKDIR /home/ICS

RUN cp /usr/share/zoneinfo/Asia/Shanghai /etc/localtime && echo 'Asia/Shanghai' >/etc/timezone

RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LANG zh_CN.UTF-8
ENV LC_ALL zh_CN.utf8

#RUN export TZ='Asia/Shanghai'
#RUN source ~/.bashrc
#RUN rm -f /etc/localtime
#RUN ln -s /usr/share/zoneinfo/Asia/ShangHai /etc/localtime

RUN yum -y install python-devel
RUN yum -y install gcc
RUN yum -y install libffi-devel
RUN yum -y install openssl-devel
RUN yum -y install libxml2-devel
RUN yum -y install libxslt-devel
RUN yum -y install mysql-devel
RUN yum -y  install fontconfig
RUN yum -y  install freetype
RUN yum -y  install libfreetype.so.6
RUN yum -y  install libfontconfig.so.1
RUN yum -y  install libstdc++.so.6

COPY google-chrome.repo /etc/yum.repos.d/google-chrome.repo
RUN yum -y install google-chrome-stable --nogpgcheck

COPY chromedriver /opt/google/chrome/chromedriver
RUN chmod +x /opt/google/chrome/chromedriver

RUN yum -y install epel-release
RUN yum -y install python-pip
RUN yum -y install vim
RUN yum -y install lrzsz
RUN yum -y install nodejs

RUN pip install --upgrade pip
RUN pip install lxml
RUN pip install requests
RUN pip install pyexecjs
RUN pip install beautifulsoup4
RUN pip install DBUtils
RUN pip install redis
RUN pip install selenium
RUN pip install mysql-python
RUN pip install pymongo
RUN pip install sqlalchemy
RUN pip install crypto
RUN pip install cryptography
RUN pip install readability
RUN pip install auth
RUN pip install msgpack
RUN pip install gevent
RUN pip install pycrypto
RUN pip install happybase
RUN pip install tornado
RUN pip install pika
RUN pip install retry==0.9.2
RUN pip install celery==4.1.1
RUN pip install apscheduler