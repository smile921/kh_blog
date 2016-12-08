**第1篇 Git**

**第2篇 从零搭建本地代码仓库**

这篇完全面向入门者。我假设你从零开始创建一个项目并且想用Git来进行版本控制，我们会讨论如何在你的个人项目中使用Git，比如如何初始化你的项目，如何管理新的或者已有的文件，如何在远端仓库中储存你的代码。

- **第1章** [快速指南](https://github.com/geeeeeeeeek/git-recipes/wiki/2.1-%E5%BF%AB%E9%80%9F%E6%8C%87%E5%8D%97)
- **第2章** [创建代码仓库](https://github.com/geeeeeeeeek/git-recipes/wiki/2.2-%E5%88%9B%E5%BB%BA%E4%BB%A3%E7%A0%81%E4%BB%93%E5%BA%93)
- **第3章** [保存你的更改](https://github.com/geeeeeeeeek/git-recipes/wiki/2.3-%E4%BF%9D%E5%AD%98%E4%BD%A0%E7%9A%84%E6%9B%B4%E6%94%B9)
- **第4章** [检查仓库状态](https://github.com/geeeeeeeeek/git-recipes/wiki/2.4-%E6%A3%80%E6%9F%A5%E4%BB%93%E5%BA%93%E7%8A%B6%E6%80%81)
- **第5章** [检出之前的提交](https://github.com/geeeeeeeeek/git-recipes/wiki/2.5-%E6%A3%80%E5%87%BA%E4%B9%8B%E5%89%8D%E7%9A%84%E6%8F%90%E4%BA%A4) 
- **第6章** [回滚错误的修改](https://github.com/geeeeeeeeek/git-recipes/wiki/2.6-%E5%9B%9E%E6%BB%9A%E9%94%99%E8%AF%AF%E7%9A%84%E4%BF%AE%E6%94%B9)
- **第7章** 重写项目历史

**第3章 远程团队协作和管理**

- **第1章** 快速指南  **第2章** 同步代码  **第3章** 创建Pull Request  **第4章** 使用分支  **第5章** 几种工作流

**第4篇 Git命令详解**

- **第1章** [图解Git命令](https://github.com/geeeeeeeeek/git-recipes/wiki/4.1-%E5%9B%BE%E8%A7%A3Git%E5%91%BD%E4%BB%A4)
  
  如果你稍微理解git的工作原理，这篇文章能够让你理解的更透彻。

**第5篇 Git实用贴士**

- **第1章** [代码合并：Merge、Rebase的选择](https://github.com/geeeeeeeeek/git-recipes/wiki/5.1-%E4%BB%A3%E7%A0%81%E5%90%88%E5%B9%B6%EF%BC%9AMerge%E3%80%81Rebase%E7%9A%84%E9%80%89%E6%8B%A9)
  
  `git rebase` 和`git merge` 都是用来合并分支，只不过方式不太相同。`git rebase` 经常被人认为是一种Git巫术，初学者应该避而远之。但如果使用得当，它能省去太多烦恼。在这篇文章中，我们会通过比较找到Git工作流中所有可以使用rebase的机会。
  
- **第2章** [代码回滚：Reset、Checkout、Revert的选择](https://github.com/geeeeeeeeek/git-recipes/wiki/5.2-%E4%BB%A3%E7%A0%81%E5%9B%9E%E6%BB%9A%EF%BC%9AReset%E3%80%81Checkout%E3%80%81Revert%E7%9A%84%E9%80%89%E6%8B%A9)
  
  git reset、git checkout和git revert都是用来撤销代码仓库中的某些更改，所以我们经常弄混。在这篇文章中，我们比较最常见的用法，分析在什么场景下该用哪个命令。
  
- **第3章** [Git log高级用法](https://github.com/geeeeeeeeek/git-recipes/wiki/5.3-Git-log%E9%AB%98%E7%BA%A7%E7%94%A8%E6%B3%95)
  
  任何一个版本控制系统设计的目的都是为了记录你代码的变化——谁贡献了什么，找出bug是什么时候引入的，以及撤回一些有问题的更改。`git log` 可以格式化commit输出的形式，或过滤输出的commit从而找到项目中你需要的任何信息。
  
- **第4章** [Git钩子：自定义你的工作流](https://github.com/geeeeeeeeek/git-recipes/wiki/5.4-Git%E9%92%A9%E5%AD%90%EF%BC%9A%E8%87%AA%E5%AE%9A%E4%B9%89%E4%BD%A0%E7%9A%84%E5%B7%A5%E4%BD%9C%E6%B5%81)
  
  Git钩子是在Git仓库中特定事件发生时自动运行的脚本。它可以让你自定义Git内部的行为，在开始周期中的关键点触发自定义的行为，自动化或者优化你开发工作流中任意部分。
  
- **第5章** [Git提交引用和引用日志](https://github.com/geeeeeeeeek/git-recipes/wiki/5.5-Git%E6%8F%90%E4%BA%A4%E5%BC%95%E7%94%A8%E5%92%8C%E5%BC%95%E7%94%A8%E6%97%A5%E5%BF%97)
  
  提交是Git的精髓所在，你无时不刻不在创建和缓存提交、查看以前的提交，或者用各种Git命令在仓库间转移你的提交。在这章中，我们研究提交的各种引用方式，以及涉及到的Git命令的工作原理。我们还会学到如何使用Git的引用日志查看看似已经删除的提交。

**第6篇 Git应用实践：用GitLab搭建一个课程教学仓库**

- **第1章** 教师和学生的最佳实践指南
  
  GitLab本身的权限管理和组织结构已经满足了教学中课程创建、学生管理、收发作业、通知统计等需求。不过，在实践中我们要尤其注意各处的权限和命名规范。因此，我总结了一份教师和学生的最佳实践指南，保证各门课程能够顺畅地进行。
  
- **第2章** 在上层搭建一个Classroom应用
  
  在实践中，我们要手动地导入大量学生、创建分支以及在Gitlab复杂的页面中穿梭。显然我们可以做得更好，那就是在GitLab上再搭建一层Classroom应用。在这章中，我会介绍我们是如何抽取需求，以及构建这个应用的。