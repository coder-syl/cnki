# cnki
#知网爬虫 及 可视化
- 1：下载安装virtualenv 
- 2：进入第一层的cnki ,使用virtualenv venv 
- 3:下载安装 redis  使用redis-server启动redis
- 4:进入cnki，启动 venv ：source venv/bin/activate 
- 5:然后再进入cnki，rq worker 启动消息队列，python manager.py runserver启动服务器
- 6:想要爬关键词，先打开chrome到知网输入关键词，然后打开开发者工具，找到network面板，刷新找到任意一个请求的cookie，把cookie复制到crawler.py里，运行python crawler.py ‘关键词’，（crawler.py在cnki外面一层）这时关键词分页面信息（论文标题和论文链接）就开始爬取了。
- 然后在浏览器访问http://127.0.0.1:5000/consume 这时论文详情页就开始爬取了。
- 7:记得修改数据库的配置