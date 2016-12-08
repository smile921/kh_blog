
---
title:  使用ipython notebook 及其一些杂记!
date:   2016-03-25 11:52:38
categories: 笔记,Awesome 
---

# 使用ipython notebook 及其一些杂记!




### 初学者CSS 小技巧
设置圆角block代码块儿

~~~~css
pre {   
    font-family: Consolas, Monaco, 'Andale Mono', monospace;
    -moz-border-radius: 1em;
    -webkit-border-radius: 1em;
    border-radius: 1em;
	}
~~~~

设置链接的鼠标为十字星型

~~~~css
a {
     cursor: crosshair;   
}
~~~~

### 初学使用docker记录

* 启动
~~~~bash
sudo docker run -it --name openresty -p 8001:8001 -v ~/Projects/Nginx_Lua:/tmp 10.88.1.229:5000/centos-openresty /bin/bash
~~~~

* 退出 ctrl p ctrl q

* 再次连接上
sudo docker attach openresty
* 彻底停止
sudo docker stop <9951920216ee>
* 再次运行
sudo docker start <9951920216ee>
* 删除
sudo docker rm <9951920216ee>
* 删除image
sudo docker rmi <image id>

<br> <br>
* #### 实例
* sudo docker run -it --name openresty -p 8001:8001 -v /home/zjex/zjex-projects/zjex-nginx/:/tmp 10.88.1.229:5000/centos-openresty /bin/bash

## Docker Registry
1. .使用registry启动私有仓库的容器
~~~~bash
docker run -d -e SETTINGS_FLAVOR=dev -e STORAGE_PATH=/tmp/registry -v /opt/data/registry:/tmp/registry  -p 5000:5000 registry
~~~~
说明：若之前没有安装registry容器则会自动下载并启动一个registry容器，创建本地的私有仓库服务。默认情况下，会将仓库创建在容器的/tmp/registry目录下，可以通过 -v 参数来将镜像文件存放在本地的指定路径上（例如，放在本地目录/opt/data/registry下）。<br>
1. ### 推送本地镜像到私有仓库
##### 给container取另外一个名字
~~~~bash
docker tag 68edf809afe7 10.88.1.229:5000/centos-jdk
~~~~
##### 最后将新的docker images推送到私服上
~~~~bash
docker push 10.88.1.229:5000/centos-jdk
~~~~
1. ### 私有仓库查询方法
~~~~bash
curl -X GET http://10.88.1.229:5000/v1/search
~~~~
说明：使用curl查看仓库10.88.1.229:5000中的镜像。返回类似如下结果
{"num_results": 1, "query": "", "results": [{"description": "", "name": "library/centos-jdk"}]}
1. ### 在其他的机器上访问和下载私有仓库的镜像
~~~~bash
docker pull 10.88.1.229:5000/centos-jdk
~~~~
1. ### docker client的https问题
修改Docker配置文件
~~~~bash
vim /etc/default/docker
~~~~
增加以下一行
~~~~bash
DOCKER_OPTS="$DOCKER_OPTS --insecure-registry=10.88.1.229:5000"
~~~~
重启Docker
~~~~bash
sudo service docker restart
~~~~bash
1. ### To do
后续在Registry中加入https
参考资料
https://segmentfault.com/a/1190000000801162

<br>
### zjex 服务处理尝试
* 启动微服务并测试 [http://10.88.1.215:8763/1/pifBorrow/pif/get/b201409041126098830](http://10.88.1.215:8763/1/pifBorrow/pif/get/b201409041126098830)
* 启动gateway 通过gateway访问微服务提供的API [http://10.88.1.215:8900/openapi/1/pifBorrow/pif/get/b201409041126098830](http://10.88.1.215:8900/openapi/1/pifBorrow/pif/get/b201409041126098830)
* 启动openresty 通过nginx 访问gateway在访问微服务的API [http://10.88.1.215:9988/zjex_rest/1/pifBorrow/pif/get/b201409041126098830](http://10.88.1.215:9988/zjex_rest/1/pifBorrow/pif/get/b201409041126098830)
* 启动docker，在docker中启动nginx 在访问微服务[http://10.88.1.227:8001/zjex_rest/1/pifBorrow/pif/get/b201409041126098830](http://10.88.1.227:8001/zjex_rest/1/pifBorrow/pif/get/b201409041126098830)
*
*
* http://127.0.0.1:8763/1/pifBorrow/pif/get/b201409041126098830
* http://10.88.1.215:8763/1/pifBorrow/pif/get/b201409041126098830 

## Let’s Encrypt CA 
项目，计划为网站提供免费的基本 SSL 证书，以加速互联网从 HTTP 向 HTTPS 过渡。Let’s Encrypt CA 将由非赢利组织 Internet Security Research Group (ISRG) 运营，计划于 2015 年夏天开始向任何需要加密证书的网站自动发放免费的 SSL 证书。


部署 HTTPS 的最大障碍是 HTTPS 所需的证书。对很多服务器运行者而言，即便是获取和部署一个基本的服务器证书也是很繁琐的事情，而且费用不低。并且部署过程容易出错，需要升级的时候就更麻烦。Let’s Encrypt 项目的目标就是解决这些问题，将会设计和部署一个协作、免费、开放的系统，让任何有需要的人都可以通过简单的鼠标点击来部署基本的服务器加密证书。

Let’s Encrypt 的原则是：

* 免费：任何域名所有者都可以零费用申请到一个针对其域名的有效证书。
* 自动：整个证书注册过程在服务器安装或配置过程中可以简单实现，而更新过程更是可以在后台自动执行。
* 安全：Let’s Encrypt 将会提供业界最新的安全技术和最好的实践。
* 透明：所有关于证书发放、撤销的记录都会向任何需要调查的人员开放。
* 开放：自动化执行的发放和更新协议将会是开放标准，软件也尽可能使用开源软件。
* 合作：与现有的互联网协议本身很相似，Let’s Encrypt 是一个对整个社区都有益的联合行动，不由任何一个组织控制。

## nbconvert 使用notebook 制作slide 

~~~~dos
jupyter-nbconvert --to slides How-to.ipynb --reveal-prefix '//cdn.bootcss.com/reveal.js/3.2.0' --output slides
~~~~
<br>
<br>
<br>


```python

```
