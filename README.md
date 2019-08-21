# ast_confbridge
  script for asterisk confbridge, use python(agi/ami) or shell(dial plan)  
  关于asterisk confbridge的一些脚本，大体分为python(agi/ami)实现跟shell(dial plan)实现，可供后台调用

---
## 简单配置
### extensions.conf

  * 请查看**asterisk_etc/extensions.conf**文件
  * 将其内容选择性更改并添加到**asterisk**的**extensions.conf**文件中
  * **python**部分是属于通用性的（也可以自行更改成非通用性的）
  * **shell**部分应由后台根据会议室的名称、参数自行修改相关内容，并自动添加到**asterisk**的**extensions.conf**文件中
  * **2001只是本人调试时使用的号码，请自行替换**

### confbridge.conf

  * 请查看**asterisk_etc/confbridge.conf**文件  
  * **\[volume_ctrl_menu\]** 属于python版（测试用），对应**python/confbridgeConf_1001.json**中的**Basic=>Menu**字段  
  * 其他部分属于**shell**版本，作为格式参考应由后台生成并自动添加
  * **请将2001改为会议室号码**

### manager.conf

  * 请查看**asterisk_etc/manager.conf**文件  
  * 由于回忆控制采用**AMI**技术，所以请将该文件上的内容追加到**asterisk**的**manager.conf**中，或者更改action.py\/action.sh中的账号密码
  * 由于action.sh使用的是**ami over http**，所以请将asterisk的**http服务开启**。（http.conf）
  * 监听端口均采用默认端口，若使用其他端口请自行更改
  * **ami的权限暂未测试**
  
### Python依赖
  * python使用**python3**版本，且需要安装pyst2、asterisk-ami模块
  ```
  $ pip install pyst2
  $ pip install asterisk-ami
  ```
### confbridgeConf_XXXX.json
  * 位于python/目录底下供python版使用，其作为XXXX（会议室电话号码）的配置文件，若在会议邀请的时候没有该文件，则会自动生成
  
---
## 简单使用
  python与shell实现的功能跟效果是一样的，只是在设计和使用上有细微的差别
  
### 会议邀请

#### Python
  * **语法** ：./invite.py   _conf_num_   _participant_num\[,participant_num2,···\]_ 
  * **_conf_num_** ：会议室**号码**
  * **_participant_num_** ：与会者号码
  ``` 
  $ cd python
  $ ./invite.py 1001 10001
  ```
  
#### Shell
  * **语法** ：./invite.sh  *conf_name*  _conf_num_  _participant_num\[,participant_num2,···\]_ 
  * **_conf_name_** ：会议室**名称**
  * **_conf_num_** ：会议室**号码**
  * **_participant_num_** ：与会者号码
  ```
  $ cd shell
  $ ./invite.sh OpenVox 2001 10001,10002,10003
  ```
  
### 定时会议（一次性）
#### Python
  * **语法** ：./invite.py   _conf_num_   _participant_num\[,participant_num2,···\]_ _hh:mm\[:ss\]_ _\[yyyy\-mm\-dd\]_
  * **_conf_num_** ：会议室**号码**
  * **_participant_num_** ：与会者号码
  * **_hh:mm\[:ss\]_** ：时间，其中秒可以省略
  * **_\[yyyy\-mm\-dd\]_** ：日期，可选，其中年份可以省略
  ``` 
  $ cd python
  $ ./invite.py 1001 10001 12:00 10-6
  ```
 #### Shell
  * **语法** ：./invite.sh  *conf_name*  _conf_num_  _participant_num\[,participant_num2,···\]_ _hh:mm\[:ss\]_ _\[yyyy\-mm\-dd\]_
  * **_conf_name_** ：会议室**名称**
  * **_conf_num_** ：会议室**号码**
  * **_participant_num_** ：与会者号码
  * **_hh:mm\[:ss\]_** ：时间，其中秒可以省略
  * **_\[yyyy\-mm\-dd\]_** ：日期，可选，其中年份可以省略
  ``` 
  $ cd shell
  $ ./invite.sh OpenVox 2001 10001 12:00 2020-6-6
  ``` 
### 定时会议（周期性）
* **语法** ：./cronJob.sh _hh:mm_ _dayOfWeek_ _dayOfMonth_ "_arg1 arg2···_"
* **_hh:mm_** ：时间，无法指定秒级
* **_dayOfWeek_** ：每周几，零为不启用
* **_dayOfMonth_** ：每月几，零为不启用
* **"_arg1 arg2···_"** ：具体参数，即调用invite.py\/invite.sh时使用的参数（会根据个数调整为python版或shell版），用双引号包围，内部用空格符间隔
```
  $./cronJob.sh 10:30 4 0 "1001 10001"  #调用Python，每周四10:30执行一次
  $./cronJob.sh 11:30 0 1 "'OpenVox' 2001 10001,10002"  #调用Shell，每月1号11:30执行一次
```
### 会议控制

#### Python
  * **语法** ：./action.py  _conf_num_  _command_  _\[participant_num\[,participant_num2\]\]_   
  * **_conf_num_** ：会议室**号码**
  * **_command_** ：可选mute、unmute、kick、lock、unlock、startRecord、stopRecord，分别对应静音、取消静音、踢出会议室、封锁会议室、解锁会议室、开始录音、结束录音  
  * **_participant_num_** ：与会者号码  
  * **注意** ：针对与会者的操作（静音、踢出等）必须提供与会者的号码（*participant_num*）
  ```
  $ cd python
  $ ./action.py 1001 mute 10001,10002
  $ ./action.py 1001 kick 10003
  $ ./action.py 1001 lock
  ```
  
#### Shell
  * **语法** ：./action.sh  _conf_name_   _command_   _\[participant_num\[,participant_num2\]\]_   
  * **_conf_name_** ：会议室**名称**
  * **_command_** ：可选mute、unmute、kick、lock、unlock、startRecord、stopRecord，分别对应静音、取消静音、踢出会议室、封锁会议室、解锁会议室、开始录音、结束录音  
  * **_participant_num_** ：与会者号码
  *  **注意** ：针对与会者的操作（静音、踢出等）必须提供与会者的号码（*participant_num*）
  ```
  $ cd shell
  $ ./action.sh "OpenVox" mute 10001,10002
  $ ./action.sh "OpenVox" kick 10003
  $ ./action.sh "OpenVox" lock
  ```
  
### 他人加入会议
####  直接加入
  * 直接拨打会议号码即可加入
#### 与会者邀请加入
  * 采用menu的方式，按0键听从指示即可。详情请参考manager.conf和confbridge.conf
