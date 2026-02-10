import os, sys
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


def get_prompt_gen_analysis_init(content_part: str):
    return f"""
【格式强制要求 - 违者任务失败】                           
程序通过精确分隔符解析输出。分隔符错误/缺失 = 无法解析 = 任务必须重做              

【三大分隔符 - 必须准确无误】:
  ① 人物分隔符: *&YLD&*
  ② 模块分隔符: ^^SHENGOOVLEI&&  （每个大模块后必须有）
  ③ 结束标记: SOLYN_AC_VER         （必须是最后六个字符）

【输出顺序 - 严格按此顺序】:
  人物分析模块 → 第一个^^SHENGOOVLEI&& →
  剧情模块 → 第二个^^SHENGOOVLEI&& → 文风模块 → 第三个^^SHENGOOVLEI&& →
  世界观模块 → 第四个^^SHENGOOVLEI&& → 【续写】内容 → SOLYN_AC_VER


# 任务目标
你是专业文学分析师，为小说建立创作模型。

# 原文输入
{content_part}


## 分析部分（严格按以下格式输出）

### 【出场人物】[列出所有重要角色名]
*&YLD&*
[角色名1]
【核心人格画像 - 三维立体解析】
[详细分析，每一点都必须有原文证据。必须包含：
1. 心理动机层（生存→安全→归属→尊重→自我实现的具体表现）
2. 道德坐标（绝对主义/功利主义/利己主义的具体表现）
3. 决策算法（面临选择时的思考优先级）
4. 情感反应模式（愤怒/悲伤/喜悦/恐惧时的具体表现）]

【动态发展轨迹 - 精确成长路径】
[详细分析，每一点都必须有原文证据。必须包含：
1. 已完成的成长弧（从[初始状态]经历[关键事件]变成[当前状态]）
2. 未解决的内心矛盾（尚未调和的价值冲突或情感困境）
3. 潜在转变触发点（可能导致角色重大改变的事件）]

【关系网络拓扑 - 动态关系图谱】
[详细分析，每一点都必须有原文证据。必须包含：
1. 强连接（与谁存在情感依赖、价值观共鸣）
2. 弱连接（与谁仅为利益合作、信息交换）
3. 对立连接（与谁存在价值观冲突或直接竞争）
4. 隐藏连接（尚未暴露但可能存在的关系线索）]
*&YLD&*
[角色名2]
[同上格式，每个角色独立成卡]
*&YLD&*
[继续其他角色...]

^^SHENGOOVLEI&&

【剧情】
1. 已发生剧情的时间线重构（超详细版）
[表格或列表形式，必须包含：
时间点 | 事件 | 涉及角色 | 直接后果 | 长期影响]

2. 多层次伏笔系统深度分析
- A级伏笔：[列出情节核心伏笔，每个必须包含：出现位置、具体内容、可能回收方向]
- B级伏笔：[列出人物相关伏笔，每个必须包含：出现位置、具体内容、可能影响]
- C级伏笔：[列出设定扩展伏笔，每个必须包含：出现位置、具体内容、可能扩展方向]
- D级伏笔：[列出情感线索伏笔，每个必须包含：出现位置、具体内容、可能发展]

3. 高潮-缓冲配比、悬念持续长度
[具体分析，必须有数据和原文证据支持]

^^SHENGOOVLEI&&

【文风】
1. **叙述视角分析**（这是最重要的部分，直接影响续写人称）：
   - 原文使用的人称视角：[第一人称/第三人称有限/第三人称全知等]
   - 视角人物是谁：[如果有固定视角人物]
   - 视角切换规律：[如果有多重视角]
   - 原文证据：[提供原文片段证明]

2. 词汇层面量化分析
   - 作者专属词典：[列出至少20个独特词汇，每个提供原文证据]
   - 动词偏好：[分析动作描写偏爱的动词类型，提供原文证据]
   - 形容词-副词使用率：[分析修饰语使用特点，提供原文证据]

3. 句式层面模式识别
   - 句式复杂度分布：[分析简单句/复合句/复杂句比例，提供原文证据]
   - 特色句式结构：[识别排比、对偶、长短句交替模式，提供原文证据]
   - 段落开头模式：[统计不同开头方式比例，提供原文证据]

4. 描写层面模式提取
   - 环境描写模式：[分析宏观→微观顺序和五感调用侧重，提供原文段落]
   - 对话推进模式：[分析对话中穿插描写/动作/心理活动的比例，提供原文证据]

5. 节奏控制层面精密测量
   - 时间流速控制：[分析不同场景的时间缩放比例，提供原文证据]
   - 信息释放曲线：[分析关键信息点出现位置规律，提供原文证据]
   - 章节收尾模式：[分析结尾方式偏好，提供原文证据]

^^SHENGOOVLEI&&

【世界观】
1. 已明确规则系统
   [逐条列出，每条必须包含：规则描述、原文证据]

2. 可推断规则
   [逐条列出，每条必须包含：规则描述、推导逻辑、原文依据]

3. 地理与组织架构
   [详细描述，每个地点/组织必须包含：位置/结构、功能、象征意义、原文证据]

^^SHENGOOVLEI&&

## 【续写】
[350-400字续写内容]

### 续写硬性要求（缺一不可）:
✓ 人称与原文100%一致
✓ 首句无缝衔接原文末句
✓ 包含: 2角色互动 + 1环境描写 + 1心理活动 + 1情节推进
✓ 文风严格模仿原文

SOLYN_AC_VER

# 质量验证清单（你必须在输出前自我检查）

## 续写部分检查：
✅ 是否严格使用原文的人称视角？
✅ 第一句话是否无缝衔接原文最后一句？
✅ 是否包含2角色互动+1环境描写+1心理活动+1情节推进？
✅ 文风是否高度模仿原文？

## 分析部分检查：
✅ 每个分析点是否有原文证据？
✅ 人物卡是否使用正确分隔符？
✅ 大模块是否使用正确分隔符？
✅ 叙述视角是否明确分析？

## 格式检查：
✅ 是否严格按照：人物→剧情→文风→世界观→续写的顺序？
✅ 是否以SOLYN_AC_VER结束？
✅ 所有分隔符是否正确使用？

现在开始执行。你必须严格遵循上述所有要求。
"""


def get_prompt_gen_analysis(prev_desc: str, content_part: str):
    return f"""
    增量更新任务 - 覆盖下方初始化指令
注意：这是一个增量更新任务，不是从头开始分析                              

## 任务状态说明
这是**第二次分析**（增量更新）。你已经：
1. 完成了第一次分析（已生成完整分析模型）
2. 现在需要基于已有分析模型和新提供的原文，进行增量更新

## 你已经拥有的信息：
1. **已有分析模型**：这是你第一次分析的结果，包含完整的人物、剧情、文风、世界观分析
2. **新增原文**：这是小说后续的内容，需要追加到已有分析模型中

## 重要原则（覆盖下方所有初始化指令）：
1. **保留所有已有内容**：不得删除或淡化已有模型中的任何重要信息
2. **追加新信息**：将新增原文中的信息追加到对应部分
3. **版本号递增**：模型版本号从v1.0更新到v1.1
4. **标注新增**：在新增内容前标注【新增】

## 增量更新指南（按以下顺序执行）：

### 第一步：读取已有分析模型
这是你第一次分析的结果：
{prev_desc}

### 第二步：分析新增原文
这是新增的小说内容：
{content_part}

### 第三步：执行增量更新

#### 一、人物系统建模更新
对每个已有角色，检查新增原文中是否有：
1. **新行为表现**：展示性格新侧面或验证已有性格分析
2. **新经历事件**：添加到该角色的成长轨迹中
3. **新关系发展**：更新关系网络拓扑
4. **新心理活动**：补充或修正心理动机层分析

**必须为每个新发现提供至少1处原文证据。**

#### 二、剧情结构与伏笔系统更新
1. **时间线扩展**：在原有时间线表格中追加新增事件
2. **伏笔状态更新**：
   - 已回收的伏笔：标记为"已回收"并注明回收章节
   - 有新进展的伏笔：补充新线索
   - 新发现的伏笔：按ABCD分类添加到对应列表

#### 三、文风指纹提取更新
检查新增原文是否：
1. 引入了新的特色词汇
2. 展示了新的句式使用习惯
3. 提供了新的描写模式实例
4. 体现了节奏控制的新特点

#### 四、世界观建模更新
检查新增原文是否：
1. 揭示了新的世界观规则
2. 扩展了已有规则的边界
3. 引入了新的地点或组织
4. 提供了已有地点/组织的新信息

### 第四步：基于更新后的完整模型进行续写
基于更新后的完整分析，创作一段无缝衔接新增原文最后一句话的续写：

**续写要求**：
- 字数：350-400字
- 起点：严格从新增原文最后一句话开始
- 人称：必须严格使用原文的叙述人称和视角
- 内容必须包含：2个角色互动 + 1处环境描写 + 1处心理活动 + 1个情节推进

### 第五步：输出更新后的完整模型
必须严格按照下方初始化提示词中的格式输出，但需注意：
1. **保留所有原有内容**：不得删除已有分析
2. **追加新增内容**：在对应部分追加【新增】标记的内容
3. **更新版本号**：从v1.0更新到v1.1
4. **续写**：基于新增原文最后一句话进行续写

## 关键提醒：
1. 你现在看到的【原文输入】是**新增原文**，不是整个小说
2. 你需要基于**已有分析模型**和**新增原文**进行增量更新
3. 输出格式必须严格按照下方初始化提示词的要求
4. 模型版本号必须从v1.0更新到v1.1

现在开始执行增量更新任务。请先读取已有分析模型，然后分析新增原文，进行增量更新，最后输出更新后的完整模型。
"""


def main():
    # model initializaition
    # params: API_KEY, client, model
    API_KEY = input("请输入你 Doubao 的 API_KEY ：")
    if not API_KEY:
        API_KEY = os.environ.get("DOUBAO_API_KEY")
        if not API_KEY:
            raise ValueError("未提供 API_KEY")
    client = OpenAI(
        api_key=API_KEY, base_url="https://ark.cn-beijing.volces.com/api/v3"
    )
    # print("选择模型：\n1. 普通聊天 (deepseek-chat)\n2. 推理 (deepseek-reasoner)\n")
    # tmp_model_idx = input("输入序号（选择 1 或 2 ，默认为 1）：")
    model = "doubao-seed-1-6-flash-250828"
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

    file_name_desc = f"{novel_name}-description.txt"
    file_name_demo = f"{novel_name}-demo.txt"
    if os.path.exists(file_name_desc):
        raise RuntimeError("以分析完毕！")

    print("正在分析第1部分...")

    # Get first response
    first_response = client.chat.completions.create(
        max_tokens=32000,
        model=model,
        messages=[
            {"role": "user", "content": get_prompt_gen_analysis_init(content_str[0])}
        ],
        stream=False,
    )

    first_reply_str = first_response.choices[0].message.content

    first_reply_str = str(first_reply_str)

    # Loop to continue if truncated
    while "SOLYN_AC_VER" not in first_reply_str:
        print("检测到响应被截断，正在续写...")
        # get last few lines to provide context
        lines = first_reply_str.split("\n")
        last_lines = "\n".join(lines[-10:]) if len(lines) > 10 else first_reply_str

        continue_prompt = """【输出被截断，需要继续完成】

你正在为一部小说进行深度文学分析（人物系统、剧情伏笔、文风指纹、世界观建模）。

## 续写要求

1. **继续输出**：从上文中断的地方继续完成分析输出
2. **不要重复**：不要重复已经输出的内容，直接从中断处继续
3. **格式完整**：确保最终输出是完整的，包含所有必要部分
4. **分隔符规则**：
   - 如果 ^^SHENGOOVLEI&& 分隔符还未完整输出（应该有2个），续写内容必须包含缺失的分隔符
   - 如果【续写】部分还未输出，续写内容必须包含第二个 ^^SHENGOOVLEI&& 和【续写】部分
5. **结束标记**：必须以 SOLYN_AC_VER 标记结束

现在，请立即从截断处继续输出。"""

        follow_up_response = client.chat.completions.create(
            max_tokens=32000,
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": get_prompt_gen_analysis_init(content_str[0]),
                },
                {"role": "assistant", "content": last_lines},
                {"role": "user", "content": continue_prompt},
            ],
            stream=False,
        )
        follow_up_content = follow_up_response.choices[0].message.content
        if follow_up_content:
            first_reply_str += follow_up_content

    # Split demo and description
    parts = first_reply_str.split("^^SHENGOOVLEI&&")
    if len(parts) < 3:
        raise ValueError(
            f"API 返回格式错误：期望至少 3 个 '^^SHENGOOVLEI&&' 分隔符，实际找到 {len(parts) - 1} 个"
        )
    first_reply_str_desc_a = parts[0]
    first_reply_str_desc_b = "^^SHENGOOVLEI&&".join(parts[1:-1])
    first_reply_str_demo = parts[-1]
    prev_reply_str_desc = (
        first_reply_str_desc_a + "^^SHENGOOVLEI&&" + first_reply_str_desc_b
    )
    # Remove END_MARKER if present
    prev_reply_str_desc = prev_reply_str_desc.replace("SOLYN_AC_VER", "").strip()
    print(f"第1部分分析完毕！示例续写：\n{first_reply_str_demo}\n")

    with open(file_name_desc, "w", encoding=encoding_format) as file:
        print(prev_reply_str_desc, file=file)
    with open(file_name_demo, "a", encoding=encoding_format) as file:
        print(first_reply_str_demo, file=file)

    if len(content_str) > 1:
        for i in range(1, len(content_str)):
            print(f"正在分析第{i + 1}部分...")

            # Get response
            response = client.chat.completions.create(
                max_tokens=32000,
                model=model,
                messages=[
                    {
                        "role": "user",
                        "content": get_prompt_gen_analysis(
                            prev_reply_str_desc, content_str[i]
                        ),
                    },
                    {
                        "role": "user",
                        "content": get_prompt_gen_analysis_init("上文给出"),
                    },
                ],
                stream=False,
            )

            reply_str = response.choices[0].message.content

            reply_str = str(reply_str)

            # Loop to continue if truncated
            while "SOLYN_AC_VER" not in reply_str:
                print("检测到响应被截断，正在续写...")
                # Get last few lines to provide context
                lines = reply_str.split("\n")
                last_lines = "\n".join(lines[-8:]) if len(lines) > 8 else reply_str

                # Build continue prompt
                continue_prompt = f"""
【输出被截断，需要继续完成】

## 续写要求

1. **继续输出**：从上文中断的地方继续完成分析输出
2. **不要重复**：不要重复已经输出的内容，直接从中断处继续
3. **格式完整**：确保最终输出是完整的，包含所有必要部分
4. **保持风格**：分析的语言风格、详细程度必须与已输出部分一致
5. **分隔符规则**：检查 ^^SHENGOOVLEI&& 分隔符是否已完整输出。如果第二个 ^^SHENGOOVLEI&& 还未输出，续写内容必须包含它和【续写】部分

## 执行说明

- 你已经完成了部分分析，现在只需继续输出剩余部分
- 必须完成整个分析模型的所有模块
- 必须以 SOLYN_AC_VER 标记结束
- 【重要】如果输出被截断在【续写】部分之前，确保 ^^SHENGOOVLEI&& 分隔符和【续写】部分都包含在续写内容中

现在，请立即从截断处继续输出。
"""

                follow_up_response = client.chat.completions.create(
                    max_tokens=32000,
                    model=model,
                    messages=[
                        {
                            "role": "user",
                            "content": get_prompt_gen_analysis(
                                prev_reply_str_desc, content_str[i]
                            ),
                        },
                        {
                            "role": "user",
                            "content": get_prompt_gen_analysis_init("上文给出"),
                        },
                        {"role": "assistant", "content": last_lines},
                        {"role": "user", "content": continue_prompt},
                    ],
                    stream=False,
                )
                follow_up_content = follow_up_response.choices[0].message.content
                if follow_up_content:
                    reply_str += follow_up_content

            # Split demo and description
            parts = reply_str.split("^^SHENGOOVLEI&&")
            if len(parts) < 3:
                raise ValueError(
                    f"API 返回格式错误：期望至少 3 个 '^^SHENGOOVLEI&&' 分隔符，实际找到 {len(parts) - 1} 个"
                )
            prev_reply_str_desc_a = parts[0]
            prev_reply_str_desc_b = "^^SHENGOOVLEI&&".join(parts[1:-1])
            reply_str_demo = parts[-1]
            prev_reply_str_desc = (
                prev_reply_str_desc_a + "^^SHENGOOVLEI&&" + prev_reply_str_desc_b
            )
            # Remove END_MARKER if present
            prev_reply_str_desc = prev_reply_str_desc.replace(
                "SOLYN_AC_VER", ""
            ).strip()
            print(f"第{i + 1}部分分析完毕！示例续写：\n{reply_str_demo}\n")
            with open(file_name_desc, "w", encoding=encoding_format) as file:
                print(prev_reply_str_desc, file=file)
            with open(file_name_demo, "a", encoding=encoding_format) as file:
                print(reply_str_demo, file=file)

    print(
        f"\n\n=======================\n分析完毕！\n分析结果已存入根目录下的{file_name_desc}.txt"
    )


# main entrance of the program
if __name__ == "__main__":
    main()
