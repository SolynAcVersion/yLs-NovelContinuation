import os, json
from typing import Tuple, Union
import prompt_manager
import db_manager
from openai import OpenAI


def split_string(s, n):
    """Split string s into pieces (each contains n chars)

    Args:
        s (str): origin string
        n (int): length of each substr in the final output

    Returns:
         array of string: result
    """
    return [s[i : i + n] for i in range(0, len(s), n)]


def _process_output_single(cmd: str, db: db_manager.NovelDB):
    _cmd, _path, _content = cmd.split(" ", 2)
    if _cmd == "C":
        return db.add(_path, json.loads(_content))

    elif _cmd == "R":
        _table_name, _record_id = _path.split("/", 1)
        res = db.read(_table_name, _record_id)
        return res
    elif _cmd == "U":
        _table_name, _record_id = _path.split("/", 1)
        return db.update(_table_name, _record_id, json.loads(_content))

    else:
        return False, "命令格式错误！"


def process_output(output: str, db: db_manager.NovelDB):
    cmds = output.split("\n")
    ret = []
    for cmd in cmds:
        res_bool, ret_str = _process_output_single(cmd, db)
        if cmd.startswith("R"):
            d_ret = cmd + "\n" + str(ret_str)
            ret.append(d_ret)
        else:
            if not res_bool:
                d_ret = cmd + "\n" + str(ret_str)
                ret.append(ret_str)
    return ret


def main():
    pm = prompt_manager.prompt_manager()
    # model initializaition
    # params: API_KEY, client, model
    API_KEY = input("请输入你 Deepseek 的 API_KEY ：")
    if not API_KEY:
        API_KEY = os.environ.get("DEEPSEEK_API_KEY")
        if not API_KEY:
            raise ValueError("未提供 API_KEY")
    client = OpenAI(api_key=API_KEY, base_url="https://api.deepseek.com")
    # print("选择模型：\n1. 普通聊天 (deepseek-chat)\n2. 推理 (deepseek-reasoner)\n")
    # tmp_model_idx = input("输入序号（选择 1 或 2 ，默认为 1）：")
    model = "deepseek-reasoner"
    # if tmp_model_idx == 2:
    #    model = "deepseek-reasoner"

    ## novel selection
    # params: novel_paths, novel_name
    print(
        "请输入小说文件路径（目前仅支持 txt 文件）\n多个文件之间请用空格隔开\n【示例：C:\\Users\\shengoovlei\\Desktop\\小说名.txt\n"
    )
    NOVEL_PATH = input(">>")

    # === FOR DEBUG USE ONLY ===

    NOVEL_PATH = "./text.txt"

    # === DELETE IF RELEASED ===

    if not NOVEL_PATH:
        raise ValueError("未提供小说路径")
    tmp_novel_paths = [i.strip() for i in NOVEL_PATH.split()]
    novel_paths = []

    #   check if paths are valid
    for path in tmp_novel_paths:
        if not os.path.exists(path):
            print(f"文件{path}不存在！")
        else:
            novel_paths.append(path)
    if not novel_paths:
        raise ValueError("未提供小说路径")

    # refuse multi-files requests (why so cruel)
    if len(novel_paths) != 1:
        print("目前暂不支持多文本小说 qwq")
        raise RuntimeError

    novel_name, _ = novel_paths[0].split(".txt", 1)

    dm = db_manager.NovelDB(f"{novel_name}.db")

    print("请输入小说文档的编码格式：\n默认 utf-8\n【示例：ansi】\n")
    encoding_format = input(">>")
    if not encoding_format:
        encoding_format = "utf-8"

    # pre-process text in file
    # params: content_str_whole, content_len, content_str
    content_str_whole = ""
    try:
        with open(novel_paths[0].strip(), "r", encoding=encoding_format) as file:
            content_str_whole = file.read()
    except Exception as _:
        raise UnicodeError(f"使用的编码{encoding_format}不正确")
    # TERMINATE SPACE
    content_str_whole = content_str_whole.replace(" ", "")
    content_len = len(content_str_whole)

    # split the origen string if it is too long
    content_str = []
    if content_len > 20000:
        content_str = split_string(content_str_whole, 20000)
    else:
        content_str.append(content_str_whole)
    print(f"小说拆分后共{len(content_str)}个部分\n")

    if os.path.exists(f"{novel_name}.db"):
        raise RuntimeError("以分析完毕！")

    print("正在分析第1部分...")

    # Get first response
    first_response = client.chat.completions.create(
        max_tokens=32000,
        model=model,
        messages=[
            {"role": "user", "content": pm.get_prompt_gen_analysis_init(content_str[0])}
        ],
        stream=False,
    )

    first_reply_str = first_response.choices[0].message.content

    first_reply_str = str(first_reply_str)


if __name__ == "__main__":
    main()
