# yande_rss_subscriber

Yande.re RSS订阅器
订阅特定关键词，定时读取RSS，将更新图片下载到指定目录

## 使用方法

```bash
python main.py --save_folder save_folder --config_folder config_folder --interval 21600
```

## 参数说明

- `--save_folder`：图片保存目录
- `--config_folder`：配置文件保存目录
- `--interval`：RSS刷新间隔（秒），默认21600秒（6小时）

## config.json文件使用方法

```json
{
  "name": "yande_rss_manager",
  "keywords": ["keyword1", "keyword2", "keyword3"],
  "interval": 21600,
  "save_folder": "save_folder/",
  "config_folder": "config_folder/"
}
```

- `name`：配置文件名称
- `keywords`：关键词列表
- `interval`：RSS刷新间隔（秒）
- `save_folder`：图片保存目录
- `config_folder`：配置文件保存目录