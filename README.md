### 项目结构
```text
.
├── config.toml          # 全局配置文件（数据库、S3、服务参数等）
├── .gitignore           # Git 忽略文件
├── pyproject.toml       # 依赖与构建配置（uv）
├── .python-version      # Python 版本
├── README.md            # 项目说明文档
├── roles.json           # 聊天角色配置文件
├── uv.lock              # 依赖锁定文件
├── templates/           # 前端模板（Jinja2）
│   └── chat.html
├── src/                 # 核心代码目录
│   ├── core/            # 核心配置与基础设施
│   │   ├── __init__.py
│   │   └── settings.py  # 配置加载（读取 config.toml / 环境变量）
│   ├── domain/          # 领域层
│   │   ├── chat/        # 聊天相关功能
│   │   │   ├── asr.py       # 语音识别 (faster_whisper ASR)
│   │   │   ├── session.py   # 聊天会话管理
│   │   │   └── tts.py       # 语音合成 (qiniu TTS)
│   │   ├── __init__.py
│   │   └── role/
│   │       └── models.py    # 角色模型定义
│   ├── main.py          # 应用入口（FastAPI Web 服务）
│   └── utils/           # 工具层（第三方服务封装）
│       └── s3.py        # 对象存储（qiniu）
└── .vscode/             # 开发环境配置
    ├── extensions.json  # 插件
    └── settings.json    # VSCode 设置

```
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
在 [config.toml](config.toml) 中修改全局配置<br>
`asr` 详见 [faster-whisper](https://github.com/SYSTRAN/faster-whisper)<br>
`qiniu.bucket` 详见 [qiniu kodo bucket](https://portal.qiniu.com/kodo/bucket)
```toml
[openai]
base_url = "https://openai.qiniu.com/v1"
[qiniu]
bucket_name = "role-play"
[asr]
model = "turbo"
language = "zh"
device = "cpu"
compute_type = "float32"
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

### 效果演示
[demo.mp4](demp.mp4)
[![demo.mp4](demo.mp4)](https://github.com/user-attachments/assets/a00a24f9-dcc8-4f03-897d-640dbe9b9b75)
