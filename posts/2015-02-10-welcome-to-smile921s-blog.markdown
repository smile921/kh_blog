---
title:  Welcome to smile921's blog!
date:   2015-02-11 23:52:38
categories: Demo  
---

### awesome 数据可视化收集

数据可视化的类型 [http://www.datavizcatalogue.com/](http://www.datavizcatalogue.com/)
文本可视化案例集 [http://textvis.lnu.se/](http://textvis.lnu.se/)
时间型数据可视化案例集 [http://survey.timeviz.net/](http://survey.timeviz.net/)
树的可视化案例集 [http://vcg.informatik.uni-rostock.de/~hs162/treeposter/poster.html](http://vcg.informatik.uni-rostock.de/~hs162/treeposter/poster.html)
弦的可视化案例集 [http://www.datavizcatalogue.com/](http://www.datavizcatalogue.com/)
 Mike bostock[http://bost.ocks.org/mike/](http://bost.ocks.org/mike/)
TODO

代码高亮

{% highlight ruby %}
# -*-coding:utf-8-*-
file_object = open('oo.txt','r')
headerFiles = open('out.txt','w') 
try:
     #all_the_text = file_object.read( )
	 #读每行
     #list_of_all_the_lines = file_object.readlines( )
     #如果文件是文本文件，还可以直接遍历文件对象获取每行：
	i = 5;	
	for line in file_object:
		#print line
		ii = '%d' %i;
		i = i + 1
		line_alt = ''+ii+'. ['+line.strip()+']()\n'
		headerFiles.write(line_alt)		 
finally:
     file_object.close()
     headerFiles.close()
{% endhighlight %}

TODO

---
   tcpdump host 10.88.1.207 -i eth1 -vv -s 0 -X
   mkdir -p /opt/woobuntu/dict
	cd /opt/woobuntu/dict
	wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_100.txt
	wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_500.txt
	wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_1000.txt
	wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_10000.txt
	wget https://raw.githubusercontent.com/danielmiessler/SecLists/master/Passwords/10_million_password_list_top_100000.txt
	cd /root
---

[jekyll-gh]: https://github.com/jekyll/jekyll
[jekyll]:    http://jekyllrb.com
