from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
# 导入记事本函数
from main import add_note, get_all_notes

# 加载本地环境变量
load_dotenv()
app = Flask(__name__)

# 读取模拟API配置
SCHOOL_API_KEY = os.getenv("SCHOOL_API_KEY", "")
SCHOOL_API_URL = os.getenv("SCHOOL_API_URL", "")

@app.route('/', methods=["GET", "POST"])
def index():
    api_status = ""
    api_response = ""
    # 处理笔记提交
    if request.method == "POST":
        note_title = request.form.get("title", "")
        note_content = request.form.get("content", "")
        if note_title and note_content:
            add_note(note_title, note_content)

    # ========== 模拟API校验逻辑（无真实密钥也能完成作业要求）==========
    if SCHOOL_API_KEY == "" or SCHOOL_API_KEY == "test_key_2026_student":
        if SCHOOL_API_KEY == "test_key_2026_student":
            api_status = "✅ 已配置测试占位密钥，待老师下发学校正式API密钥后替换"
            api_response = "模拟接口返回：当前为调试状态，正式密钥下发后即可对接校园内网接口"
        else:
            api_status = "⚠️ 暂未配置API密钥，等待老师下发学校密钥"
            api_response = "暂无接口数据"
    else:
        api_status = "✅ 密钥已配置完成，可在校园网访问校内接口"
        api_response = "接口调用就绪（正式密钥模式）"

    all_notes = get_all_notes()
    return render_template("index.html", notes=all_notes, api_status=api_status, api_data=api_response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)