#!/usr/bin/python
# -*- coding: UTF-8 -*-

# smtplib是Python 用来发送邮件的模块
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.multipart import MIMEMultipart  # 构建邮件头信息，包括发件人，接收人，标题等
from email.mime.text import MIMEText  # 构建邮件正文，可以是text，也可以是HTML
from email.mime.application import MIMEApplication  # 构建邮件附件，理论上，只要是文件即可，一般是图片，Excel表格，word文件等
from email.header import Header  # 专门构建邮件标题的，这样做，可以支持标题中文
from email.mime.image import MIMEImage  # 处理图片信息

import time
import pandas as pd
import pymysql.cursors
import time

time_start = time.time()


