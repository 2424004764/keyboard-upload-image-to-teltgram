# keyboard-upload-image-to-teltgram
按下指定的组合键时将剪切板中的图片上传至telegram服务器并将图片地址写到剪切板并发出windows通知

本项目上传的服务为 https://github.com/cf-pages/Telegraph-Image 搭建，如何该项目不可用，可使用我的fork：https://github.com/2424004764/Telegraph-Image
将上述服务搭建起来以后会有一个域名


将域名修改到main.py的12行，并修改日志文件的路径为你自己的文件系统的路径即可


其中run-upload-image-to-telegram.bat为系统自启文件，将该文件按照说明中的路径放置即可在windows开机时自动运行该程序，该bat脚本中的pythonw文件和py文件根据自己的文件实际位置而定
