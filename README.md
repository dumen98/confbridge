# ast_confbridge
  script for asterisk confbridge, use python(agi/ami) or shell(dial plan)  
  关于asterisk confbridge的一些脚本，大体分为python(agi/ami)实现跟shell(dial plan)实现，可供后台调用  

---
## 一些简单配置
### extensions.conf
  请查看__asterisk_etc/extensions.conf__文件  
  将其内容选择性更改并添加到asterisk的extensions.conf文件中  
  python部分是属于通用性的（也可以自行更改成非通用性的）  
  shell部分应由后台根据会议室的名称、参数自行修改相关内容，并自动添加到asterisk的extensions.conf文件中（2001只是本人调试时使用的号码，请自行替换）  
### confbridge.conf
  请查看asterisk_etc/confbridge.conf文件  
  \[volume_ctrl_menu\]属于python版本，对应python/confbridgeConf_1001.json中的Basic=>Menu字段  
  其他部分属于shell版本，作为格式参考应由后台生成并自动添加（请将2001改为会议室号码）  
