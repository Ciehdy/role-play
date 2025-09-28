### 配置
在 七牛云 获取 [API_KEY](https://portal.qiniu.com/ai-inference/api-key) 以及 [AK & SK](https://portal.qiniu.com/developer/user/key)<br>
在项目根目录添加 [.env](.env) 文件，写入以下内容
```
OPENAI__API_KEY=your_api_key
QINIU__ACCESS_KEY=your_ak
QINIU__SECRET_KEY=your_sk
```
在 [roles.json](roles.json) 中添加自定义角色, 在 [voice/list](https://openai.qiniu.com/v1/voice/list) 选择 `tts_voice_type`
```json
{
  "xiao_yan": {
    "name": "萧炎",
    "description": "斗破苍穹的主角。",
    "prompt": "像正常聊天一样，不要添加动作或心理描写。",
    "tts_voice_type": "qiniu_zh_male_wncwxz",
    "tts_speed_ratio": 1.0
  }
}

```

### 运行
使用 [uv](https://docs.astral.sh/uv/) 安装依赖
```shell
uv venv
uv sync
```
在项目根目录执行以下命令
```shell
fastapi dev src/main.py
```
在浏览器打开 `http://127.0.0.1:8000` 进入聊天界面