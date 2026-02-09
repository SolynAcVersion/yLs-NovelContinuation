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
    你是一名专业的文学分析师，现在要为一部长篇小说建立完整的创作模型。这是第一次分析，你将获得连续的原文内容。

你必须严格按照以下格式和标准执行分析，不得偏离。你的分析必须是详细、深入、有据可依的。

原文输入

{content_part}
分析要求（必须执行）
一、人物分析要求
对每个重要角色（有独立人格、推动情节发展的角色）进行以下深度分析：

人物卡必须包含以下三个部分：

核心人格画像 - 三维立体解析

心理动机层：分析角色的马斯洛需求层次定位，给出具体证据

道德坐标：确定角色的道德体系（绝对主义/功利主义/利己主义），给出具体表现例子

决策算法：分析角色面临选择时的思考优先级模式

情感反应模式：详细描述角色在愤怒、悲伤、喜悦、恐惧时的具体表现

必须为每个分析点提供至少1处原文例子。

动态发展轨迹 - 精确成长路径

已完成的成长弧：描述角色从初始状态到当前状态的变化，列出关键事件

未解决的内心矛盾：识别角色尚未调和的价值冲突或情感困境

潜在转变触发点：推测可能导致角色重大改变的事件

必须为成长弧提供至少2处关键事件的原文证据。

关系网络拓扑 - 动态关系图谱

强连接：分析角色的深度关系，给出具体互动例子

弱连接：分析角色的功能性关系

对立连接：分析角色的冲突关系，给出冲突事件例子

隐藏连接：推测可能存在的隐藏关系，给出推理依据

必须为强连接和对立连接提供至少1处原文证据。

二、剧情分析要求
已发生剧情的时间线重构

按照时间顺序列出所有重要事件

每个事件必须包含：时间点、事件描述、涉及角色、直接后果、长期影响

时间线必须是完整的，不能有遗漏

必须为每个重要事件提供章节位置或原文线索。

多层次伏笔系统深度分析

A级伏笔（情节核心）：列出直接影响主线走向的未解之谜

B级伏笔（人物相关）：列出角色背景、能力、关系的未揭露部分

C级伏笔（设定扩展）：列出世界观中已提及但未详述的设定

D级伏笔（情感线索）：列出埋藏的情感线发展可能

必须为每个伏笔提供出现位置和原文例子。

叙事节奏模式分析

高潮-缓冲配比：分析紧张章节与舒缓章节的排列规律

悬念持续长度：分析平均每个悬念跨越的章节数

必须提供具体数据和原文例子支持分析。

三、文风分析要求
词汇层面量化分析

作者专属词典：列出作品中独创或高频使用的独特词汇

动词偏好：分析动作描写的动词类型偏好

形容词-副词使用率：分析修饰语的使用特点

必须为每个分析点提供至少3个原文例子。

句式层面模式识别

句式复杂度分布：分析简单句、复合句、复杂句的比例

特色句式结构：识别排比句、对偶句、长短句交替的固定模式

段落开头模式：统计环境描写开头、对话开头、动作开头、心理描写开头的使用频率

必须为特色句式结构提供至少2个原文例子。

描写层面模式提取

环境描写模式：分析宏观→微观的描写顺序，五感调用的侧重

对话推进模式：分析对话中穿插描写、动作、心理活动的比例和插入点规律

必须为环境描写模式提供至少1个完整的原文段落例子。

节奏控制层面精密测量

时间流速控制：分析不同场景下主观时间与客观时间的缩放比例

信息释放曲线：分析每章内关键信息点的出现位置规律

必须提供具体数据和原文例子。

四、世界观分析要求
已明确规则系统

物理/魔法/异能规则：归纳已有表现中的底层逻辑

社会运行规则：分析权力结构、经济体系、道德法律

成长体系规则：分析角色变强的路径、瓶颈、代价

必须为每个规则提供至少1处原文证据。

可推断规则

未言明但可推导：从已有事件中逻辑推导出的必然规则

规则边界：分析已展示能力的极限和可能的限制条件

必须提供推导逻辑和原文依据。

地理与组织架构

已出现地点：详细描述位置关系、功能、象征意义

已出现组织：分析目标、结构、行事风格、内部矛盾

必须提供具体位置描述和组织行为原文例子。

五、续写要求
基于你的深度分析，创作一段无缝衔接原文的续写：

字数：350-400字

起点：严格从原文最后一句话开始

必须包含：至少2个人物的互动、至少1处环境描写、至少1处心理活动

至少推进1个情节单位或设置1个新悬念

严格遵循所有已分析出的文风特征、人物行为逻辑、世界观规则

输出格式（必须严格遵守）

【出场人物】角色A、角色B、角色C、角色D
*&YLD&*
角色A
【核心人格画像 - 三维立体解析】
[详细分析，包含原文例子]

【动态发展轨迹 - 精确成长路径】
[详细分析，包含原文例子]

【关系网络拓扑 - 动态关系图谱】
[详细分析，包含原文例子]
*&YLD&*
角色B
[同上格式]
*&YLD&*
角色C
[同上格式]
*&YLD&*
角色D
[同上格式]

^^SHENGOOVLEI&&

【剧情】
1. 已发生剧情的时间线重构（超详细版）
[表格或列表形式，包含时间点、事件、涉及角色、直接后果、长期影响]

2. 多层次伏笔系统深度分析
- A级伏笔：[列表，每个伏笔包含出现位置、具体内容、当前状态]
- B级伏笔：[同上]
- C级伏笔：[同上]
- D级伏笔：[同上]

3. 高潮-缓冲配比、悬念持续长度
[具体分析，包含数据和原文例子]


【文风】
1. 词汇层面量化分析
[详细分析，包含原文例子]

2. 句式层面模式识别
[详细分析，包含原文例子]

3. 描写层面模式提取
[详细分析，包含原文例子]

4. 节奏控制层面精密测量
[详细分析，包含原文例子]


【世界观】
1. 已明确规则系统
[逐条列出，每条包含规则描述和原文证据]

2. 可推断规则
[逐条列出，每条包含规则描述和推导逻辑]

3. 地理与组织架构
[详细描述，包含具体信息和原文例子]

^^SHENGOOVLEI&&

【续写】
[350-400字的续写内容]

SOLYN_AC_VER

执行指令
现在开始分析。注意：

严格按照上述格式输出，不得添加额外内容

每个分析点都必须有原文证据支持，没有证据的分析不得包含在报告中

人物分析必须详细深入，不能只是简单描述

续写必须高度模仿原文风格，达到难以区分的程度

所有分隔符必须正确使用：人物卡之间用*&YLD&*分隔，大模块之间用^^SHENGOOVLEI&&分隔

如果无法完成上述要求，请明确说明缺少什么信息。

**重要：输出必须以 SOLYN_AC_VER 标记结束。**

开始分析。
    """


def get_prompt_gen_analysis(prev_desc: str, content_part: str):
    return f"""
【重要指令】你的输出必须包含特殊分隔符 ^^SHENGOOVLEI&& ，程序将根据此分隔符拆分你的输出。如果缺少此分隔符，将导致解析失败。

你是一个资深文学分析师，现在要为一部长篇小说建立专业级、可操作的创作模型。

这是增量更新任务。你之前已经分析过这部小说的部分内容，并生成了一个分析模型。现在你将看到：
1. 之前生成的分析模型（在下方提供）
2. 新增的小说原文（在下方提供）

你的任务是：
基于已有分析模型和新增原文，进行扩展和补充分析，生成一个更新后的、更完整的模型。

重要原则：
1. 保留所有已有内容：不得删除或淡化已有模型中的任何重要信息，特别是人物经历、剧情事件、伏笔记录等，也不要试图总结优化那段经历等。
2. 追加新信息：将新增原文中的信息追加到对应部分，使模型更完整
3. 版本号递增：更新模型版本号（如v1.1→v1.2）
4. 标注新增：在新增内容前标注【新增】或类似标记

原有分析：
{prev_desc}

新增原文：
{content_part}

# 增量分析指南（必须严格执行）

## 一、人物系统建模更新
对每个已有角色，检查新增原文中是否有：
1. **新行为表现**：展示性格新侧面或验证已有性格分析
2. **新经历事件**：添加到该角色的成长轨迹中
3. **新关系发展**：更新关系网络拓扑
4. **新心理活动**：补充或修正心理动机层分析

**必须为每个新发现提供至少1处原文证据。**

如有新角色出现，请为其建立完整档案，格式与已有角色一致。

## 二、剧情结构与伏笔系统更新
1. **时间线扩展**：在原有时间线表格中追加新增事件
2. **伏笔状态更新**：
   - 已回收的伏笔：标记为"已回收"并注明回收章节
   - 有新进展的伏笔：补充新线索
   - 新发现的伏笔：按ABCD分类添加到对应列表
3. **叙事节奏验证**：检查新增章节是否符合作者原有的节奏模式

**必须为每个伏笔更新提供原文位置。**

## 三、文风指纹提取更新
检查新增原文是否：
1. 引入了新的特色词汇
2. 展示了新的句式使用习惯
3. 提供了新的描写模式实例
4. 体现了节奏控制的新特点

**必须为每个文风发现提供至少1处原文例子。**

## 四、世界观建模更新
检查新增原文是否：
1. 揭示了新的世界观规则
2. 扩展了已有规则的边界
3. 引入了新的地点或组织
4. 提供了已有地点/组织的新信息

**必须为每个世界观更新提供原文证据。**

# 验证任务：风格模拟测试

## 续写要求
基于更新后的完整分析，创作一段无缝衔接新增原文最后一句话的续写：

### 基本要求：
- 字数：350-400字
- 起点：严格从新增原文最后一句话开始
- 严格遵循：所有已分析出的文风特征、人物行为逻辑、世界观规则

### 内容要求：
1. **人物互动**：至少2个人物的互动，符合其关系模式
2. **环境描写**：至少1处环境描写，符合描写模式
3. **心理活动**：至少1处心理活动，符合该角色思维习惯
4. **情节推进**：至少推进1个情节单位或设置1个新悬念

# 输出格式（必须严格遵守）

你的输出必须严格按照以下格式，不能有任何偏差：
【出场人物】角色A、角色B、角色C、角色D
*&YLD&*
角色A
【核心人格画像 - 三维立体解析】
[原有内容完全保留，新增内容用【新增】标记，必须提供原文例子]

【动态发展轨迹 - 精确成长路径】
[原有内容完全保留，新增经历事件用【新增】标记，必须提供原文证据]

【关系网络拓扑 - 动态关系图谱】
[原有内容完全保留，新关系发展用【新增】标记，必须提供原文例子]
*&YLD&*
角色B
[同上格式，保持所有原有内容]
*&YLD&*
[继续其他角色...]

^^SHENGOOVLEI&&

【剧情】

已发生剧情的时间线重构（超详细版）
[原有时间线完全保留，新增事件追加在下方，用【新增】标记]

多层次伏笔系统深度分析

A级伏笔：[原有列表完全保留，新增伏笔用【新增】标记，状态有更新的伏笔用【更新】标记]

B级伏笔：[同上]

C级伏笔：[同上]

D级伏笔：[同上]

高潮-缓冲配比、悬念持续长度
[原有分析完全保留，新增观察用【新增】标记，必须提供原文例子]


【文风】

词汇层面量化分析
[原有内容完全保留，新增特色词汇用【新增】标记，必须提供原文例子]

句式层面模式识别
[原有内容完全保留，新增句式习惯用【新增】标记，必须提供原文例子]

描写层面模式提取
[原有内容完全保留，新增描写模式用【新增】标记，必须提供原文例子]

节奏控制层面精密测量
[原有内容完全保留，新增节奏特点用【新增】标记，必须提供原文例子]


【世界观】

已明确规则系统
[原有规则完全保留，新增规则用【新增】标记，必须提供原文证据]

可推断规则
[原有推断完全保留，新增推断用【新增】标记，必须提供推导逻辑]

地理与组织架构
[原有内容完全保留，新增内容用【新增】标记，必须提供具体信息]

^^SHENGOOVLEI&&

【续写】
[350-400字的续写内容，严格从新增原文最后一句话开始]

SOLYN_AC_VER

# 执行要求

1. **严格保留**：已有模型中的所有内容必须完整保留，不得删除、简化或重新组织
2. **精确追加**：新增内容必须精确追加到对应位置，用【新增】标记清楚
3. **证据充分**：所有新增分析必须提供原文证据或具体例子
4. **格式正确**：必须使用指定的分隔符（*&YLD&* 和 ^^SHENGOOVLEI&&）
5. **版本更新**：在模型开头更新版本号（如v1.1→v1.2）

# 版本更新记录
在输出最后添加版本更新记录：
- 首次分析：[日期]，原文[字数]，建立基础模型 v1.0
- 上次更新：[上次日期]，新增[上次字数]，更新重点：[上次重点]
- 本次更新：[当前日期]，新增[当前字数]，更新重点：[详细说明本次新增内容]

# 错误示例（不要这样做）：
❌ 删除原有的人物经历
❌ 合并或简化原有的事件描述
❌ 重新组织原有内容的结构
❌ 不提供原文证据的新增分析

# 正确示例（要这样做）：
原有内容一字不改保留
新增内容用【新增】标记追加
每个新增分析都有原文证据
严格按照指定格式输出

现在开始分析。请先读取已有模型，然后结合新增原文，进行增量分析并输出更新后的完整模型。

注意：必须严格按照指定格式输出，不得有任何偏差。

**重要：输出必须以 SOLYN_AC_VER 标记结束。**
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
                    }
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
