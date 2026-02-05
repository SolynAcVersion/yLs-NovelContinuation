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
    return [s[i:i + n] for i in range(0, len(s), n)]




def get_prompt_gen_analysis_init(content_part: str):
    return f"""
核心指令
你是一个资深文学分析师，现在要为一部长篇小说建立专业级、可操作的创作模型。你的分析必须超越表面，深入到作者的创作思维层面，建立可复现的叙事引擎。
原文:
{content_part}
一、人物系统建模（每位重要角色需完成以下全部）
1. 核心人格画像
心理动机层：生存需求→安全需求→归属需求→尊重需求→自我实现（马斯洛需求层次定位）
道德坐标：个人道德体系（绝对主义/功利主义/利己主义）及具体表现
决策算法：面临选择时的思考优先级（如：亲友安危＞个人理想＞集体利益＞风险规避）
情感反应模式：愤怒/悲伤/喜悦/恐惧时的特定表现组合
2. 动态发展轨迹
已完成的成长弧：从[初始状态]经历[关键事件]变成[当前状态]
未解决的内心矛盾：尚未调和的价值观冲突或情感困境
潜在转变触发点：哪些事件可能导致该角色发生重大改变
3. 关系网络拓扑
强连接（深度关系）：与谁存在情感依赖、价值观共鸣
弱连接（功能性关系）：与谁仅为利益合作、信息交换
对立连接：与谁存在价值观冲突或直接竞争
隐藏连接：尚未暴露但可能存在的关系线索
二、剧情结构与伏笔系统
1. 已发生剧情的时间线重构
时间点 | 事件 | 涉及角色 | 直接后果 | 长期影响
[精确到章节] | [核心动作] | [谁参与] | [立即结果] | [对后续的潜在影响]
2. 多层次伏笔分类
A级伏笔（情节核心）：直接影响主线走向的未解之谜
B级伏笔（人物相关）：角色背景、能力、关系的未揭露部分
C级伏笔（设定扩展）：世界观中已提及但未详述的设定
D级伏笔（情感线索）：埋藏的情感线发展可能
3. 叙事节奏模式分析
章节信息密度：每章推进几个情节单位（1个情节单位=1个明确的事件进展）
高潮-缓冲配比：紧张章节与舒缓章节的排列规律
悬念持续长度：平均每个悬念跨越多少章节才揭晓
三、文风指纹提取
1. 词汇层面
作者专属词典：作品中独创或高频使用的独特词汇
动词偏好：动作描写偏爱哪类动词（强烈动作/微妙变化/心理动词）
形容词-副词使用率：描写中修饰语的比例及特色
2. 句式层面
句式复杂度分布：简单句/复合句/复杂句的比例
特色句式结构：排比句、对偶句、长短句交替的固定模式
段落开头模式：环境描写开头/对话开头/动作开头/心理描写开头的使用频率
3. 描写层面
环境描写模式：宏观→微观的描写顺序，五感调用的侧重（视觉/听觉/嗅觉/触觉/味觉的比例）
战斗描写模板（如有）：招式命名规律、动作分解粒度、胜负判定逻辑
对话推进模式：对话中穿插描写/动作/心理活动的比例和插入点规律
4. 节奏控制层面
时间流速控制：不同场景下主观时间与客观时间的缩放比例
信息释放曲线：每章内关键信息点（新设定、新线索、情感爆发）的出现位置规律（如：25%-50%-75%位置）
章节收尾模式：悬念式结尾/情感式结尾/总结式结尾的使用偏好
四、世界观建模
1. 已明确规则系统
物理/魔法/异能规则：已有表现中可归纳的底层逻辑
社会运行规则：权力结构、经济体系、道德法律
成长体系规则：角色变强的路径、瓶颈、代价
2. 可推断规则
未言明但可推导：从已有事件中可逻辑推导出的必然规则
规则边界：已展示能力的极限和可能的限制条件
3. 地理与组织架构
已出现地点：详细位置关系、功能、象征意义
已出现组织：目标、结构、行事风格、内部矛盾
验证任务：风格模拟测试

五、续写要求
基于你的深度分析，创作一段无缝衔接原文的续写：
字数：350-400字
起点：严格从原文最后一句话开始
必须包含：
至少2个人物的互动（符合其关系模式）
至少1处环境描写（符合描写模式）
至少1处心理活动（符合该角色思维习惯）
至少推进1个情节单位（或设置1个新悬念）
严格遵循：所有已分析出的文风特征、人物行为逻辑、世界观规则


输出格式（必须严格遵守）
```text
【续写】

### 测试续写
[在此放置350-400字的续写内容]


^^SHENGOOVLEI&&

## 【小说创作深度模型 v1.0】

### 一、人物系统全档案
[按出场重要性排序，每位重要角色独立成节，包含全部深度分析内容]

### 二、剧情结构与伏笔图谱
1. **精确时间线**
[表格形式呈现]

2. **伏笔分类与状态**
- A级伏笔：[列表，每个伏笔包含：出现章节、当前状态、可能回收方向]
- B级伏笔：[同上]
- C级伏笔：[同上]
- D级伏笔：[同上]

3. **叙事节奏分析结果**
[具体数据和规律总结]

### 三、文风指纹全记录
1. **词汇层**：[作者专属词典、动词偏好等详细列表]
2. **句式层**：[句式复杂度统计、特色句式模板]
3. **描写层**：[各类场景的描写模板总结]
4. **节奏层**：[时间控制、信息释放、章节收尾的具体规律]

### 四、世界观规则手册
1. **已明确规则**：[逐条列出]
2. **可推断规则**：[逐条列出]
3. **地理与组织图**：[清晰结构]

### 五、创作者思维推断
1. **核心创作偏好**：[基于文本推断作者最擅长/最喜爱的创作元素]
2. **叙事价值观**：[通过情节安排体现的作者价值取向]
3. **读者预期管理策略**：[作者如何操控读者情绪和期待]

SOLYN_AC_VER
```
分析标准
证据链要求：每个分析结论必须引用至少2处原文证据
优先级排序：先分析已明确信息，再推导潜在模式
系统思维：注意各元素之间的关联性（如：人物性格如何影响其对话风格）
续写标准
无缝衔接：第一句话必须自然承接原文最后一句的语气和情境
避免创新：此阶段只模仿，不创新作者未使用的表达方式
完整性：续写段落本身应有微型的起承转合
输出标准
结构严格：必须使用指定标题和分隔符
语言专业：分析语言保持客观、精准
完整性：确保每个要求的分析维度都得到覆盖
结束标记：分析完成后必须在最后输出 SOLYN_AC_VER 标记
现在开始深度分析，并输出完整结果。
    """

def get_prompt_gen_analysis(prev_desc: str, content_part: str):
    return f"""
你是一个资深文学分析师，现在要为一部长篇小说建立专业级、可操作的创作模型。你的分析必须超越表面，深入到作者的创作思维层面，建立可复现的叙事引擎。
这是增量更新任务。 你之前已经分析过这部小说的部分内容，并生成了一个分析模型。现在你将看到：
之前生成的分析模型和新增的小说原文
你的任务是：
基于已有分析模型和新增原文，进行扩展和补充分析，生成一个更新后的、更完整的模型。
重要原则：
保留所有已有内容：不得删除或淡化已有模型中的任何重要信息，特别是人物经历、剧情事件、伏笔记录等，也不要试图总结优化那段经历等。
保留所有已有内容：不得删除或淡化已有模型中的任何重要信息，特别是人物经历、剧情事件、伏笔记录等，也不要试图总结优化那段经历等。
追加新信息：将新增原文中的信息追加到对应部分，使模型更完整
版本号递增：更新模型版本号（如v1.0→v1.1）
标注新增：在新增内容前标注【新增】或类似标记
原有分析：
{prev_desc}
新增原文：
{content_part}
增量分析指南
请按照以下维度，在已有模型的基础上进行扩展分析：
一、人物系统建模更新
对每个已有角色，检查新增原文中是否有：
新行为表现：展示性格新侧面或验证已有性格分析
新经历事件：添加到该角色的成长轨迹中
新关系发展：更新关系网络拓扑
新心理活动：补充或修正心理动机层分析
如有新角色出现，请为其建立完整档案，格式与已有角色一致。
二、剧情结构与伏笔系统更新
时间线扩展：在原有时间线表格中追加新增事件
伏笔状态更新：
已回收的伏笔：标记为"已回收"并注明回收章节
有新进展的伏笔：补充新线索
新发现的伏笔：按ABCD分类添加到对应列表
叙事节奏验证：检查新增章节是否符合作者原有的节奏模式
三、文风指纹提取更新
检查新增原文是否：
引入了新的特色词汇
展示了新的句式使用习惯
提供了新的描写模式实例
体现了节奏控制的新特点
如有新发现，补充到对应部分。
四、世界观建模更新
检查新增原文是否：
揭示了新的世界观规则
扩展了已有规则的边界
引入了新的地点或组织
提供了已有地点/组织的新信息
验证任务：风格模拟测试
五、续写要求
基于更新后的完整分析，创作一段无缝衔接新增原文最后一句话的续写：
字数：350-400字
起点：严格从新增原文最后一句话开始
必须包含：
至少2个人物的互动（符合其关系模式）
至少1处环境描写（符合描写模式）
至少1处心理活动（符合该角色思维习惯）
至少推进1个情节单位（或设置1个新悬念）
严格遵循：所有已分析出的文风特征、人物行为逻辑、世界观规则
输出格式（必须严格遵守）
```text
【续写】

### 测试续写
[在此放置350-400字的续写内容]

^^SHENGOOVLEI&&

## 【小说创作深度模型 vX.X】（更新版本号，如v1.1）

### 一、人物系统全档案
[按出场重要性排序，每位重要角色独立成节。已有内容完全保留，新增内容用【新增】标记]

### 二、剧情结构与伏笔图谱
1. **精确时间线**
[原有表格完全保留，新增事件追加在下方，用【新增】标记]

2. **伏笔分类与状态**
- A级伏笔：[原有列表完全保留，新增伏笔用【新增】标记，状态有更新的伏笔用【更新】标记]
- B级伏笔：[同上]
- C级伏笔：[同上]
- D级伏笔：[同上]

3. **叙事节奏分析结果**
[原有分析完全保留，新增观察用【新增】标记]

### 三、文风指纹全记录
1. **词汇层**：[原有内容完全保留，新增观察用【新增】标记]
2. **句式层**：[原有内容完全保留，新增观察用【新增】标记]
3. **描写层**：[原有内容完全保留，新增观察用【新增】标记]
4. **节奏层**：[原有内容完全保留，新增观察用【新增】标记]

### 四、世界观规则手册
1. **已明确规则**：[原有内容完全保留，新增规则用【新增】标记]
2. **可推断规则**：[原有内容完全保留，新增推断用【新增】标记]
3. **地理与组织图**：[原有内容完全保留，新增内容用【新增】标记]

### 五、创作者思维推断
[原有内容完全保留，新增观察用【新增】标记]

### 六、版本更新日志
- 首次分析：[日期]，原文[字数]，建立基础模型 v1.0
- 本次更新：[日期]，新增[字数]，更新重点：[简要说明新增内容]

SOLYN_AC_VER
```
现在开始分析。请先读取已有模型，然后结合新增原文，进行增量分析并输出更新后的完整模型。
注意：必须在分析最后输出 SOLYN_AC_VER 标记表示分析完成。
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
        api_key=API_KEY,
        base_url='https://ark.cn-beijing.volces.com/api/v3'
    )
    # print("选择模型：\n1. 普通聊天 (deepseek-chat)\n2. 推理 (deepseek-reasoner)\n")
    # tmp_model_idx = input("输入序号（选择 1 或 2 ，默认为 1）：")
    model = "doubao-seed-1-6-flash-250828"
    #if tmp_model_idx == 2:
    #    model = "deepseek-reasoner"
    
    
    ## novel selection
    # params: novel_paths, novel_name
    print("请输入小说文件路径（目前仅支持 txt 文件）\n多个文件之间请用空格隔开\n【示例：C:\\Users\\shengoovlei\\Desktop\\小说名.txt\n")
    NOVEL_PATH = input(">>")
    
    
    
    
    
# === FOR DEBUG USE ONLY ===
    
    NOVEL_PATH = 'C:\\Users\\2300\\Desktop\\mcpPro\\deepseek_v3_tokenizer\\text.txt'
    
# === DELETE IF RELEASED ===
    
    
    
    
    
    if not NOVEL_PATH:
        raise ValueError("未提供小说路径")
    tmp_novel_paths = [i.strip() for i in NOVEL_PATH.split()]
    novel_paths = []
    
    #   check if paths are valid
    for path in tmp_novel_paths:
        if not os.path.exists(path):
            print(f"文件不存在！")
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
        encoding_format = 'utf-8'
    
    
    # pre-process text in file
    # params: content_str_whole, content_len, content_str
    content_str_whole = ""
    try:
        with open(novel_paths[0].strip(), 'r', encoding=encoding_format) as file:
            content_str_whole = file.read()
    except Exception as e:
        raise UnicodeError(f"使用的编码{encoding_format}不正确")
    # TERMINATE SPACE
    content_str_whole = content_str_whole.replace(' ', '')
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
        messages=[{"role": "user", "content": get_prompt_gen_analysis_init(content_str[0])}],
        stream=False
    )

    first_reply_str = first_response.choices[0].message.content
    
    first_reply_str = str(first_reply_str)

    # Loop to continue if truncated
    while "SOLYN_AC_VER" not in first_reply_str:
        print("检测到响应被截断，正在续写...")
        # get last few lines to provide context
        lines = first_reply_str.split('\n')
        last_lines = '\n'.join(lines[-5:]) if len(lines) > 5 else first_reply_str

        continue_prompt = f"""你正在为一部小说进行深度文学分析（人物系统、剧情伏笔、文风指纹、世界观建模）。

你的最后输出是:
{last_lines}

请从停止的地方继续完成分析，要求：
1. 继续输出完整的分析内容（人物、剧情、文风、世界观等）
2. 不要重复【续写】部分或 ^^SHENGOOVLEI&& 分隔符
3. 必须以 SOLYN_AC_VER 标记结束"""

        follow_up_response = client.chat.completions.create(
            max_tokens=32000,
            model=model,
            messages=[
                {"role": "user", "content": get_prompt_gen_analysis_init(content_str[0])},
                {"role": "assistant", "content": first_reply_str},
                {"role": "user", "content": continue_prompt}
            ],
            stream=False
        )
        follow_up_content = follow_up_response.choices[0].message.content
        if follow_up_content:
            first_reply_str += follow_up_content

    # Split demo and description
    first_reply_str_demo, prev_reply_str_desc = first_reply_str.split("^^SHENGOOVLEI&&", 1)
    # Remove END_MARKER if present
    prev_reply_str_desc = prev_reply_str_desc.replace("SOLYN_AC_VER", "").strip()
    print(f"第1部分分析完毕！示例续写：\n{first_reply_str_demo}\n")
    
    
    with open(file_name_desc, 'w', encoding=encoding_format) as file:
        print(prev_reply_str_desc, file=file)
    with open(file_name_demo, 'a', encoding=encoding_format) as file:
        print(first_reply_str_demo, file=file)
    
    if len(content_str) > 1:
        for i in range(1, len(content_str)):
            print(f"正在分析第{i + 1}部分...")

            # Get response
            response = client.chat.completions.create(
                max_tokens=32000,
                model=model,
                messages=[{"role": "user", "content": get_prompt_gen_analysis(prev_reply_str_desc, content_str[i])}],
                stream=False
            )

            reply_str = response.choices[0].message.content

            # Loop to continue if truncated
            while "SOLYN_AC_VER" not in reply_str:
                print("检测到响应被截断，正在续写...")
                # Get last few lines to provide context
                lines = reply_str.split('\n')
                last_lines = '\n'.join(lines[-5:]) if len(lines) > 5 else reply_str

                # Build continue prompt
                continue_prompt = f"""你正在为一部小说进行深度文学分析（人物系统、剧情伏笔、文风指纹、世界观建模）。

你的最后输出是:
{last_lines}

请从停止的地方继续完成分析，要求：
1. 继续输出完整的分析内容（人物、剧情、文风、世界观等）
2. 不要重复【续写】部分或 ^^SHENGOOVLEI&& 分隔符
3. 必须以 SOLYN_AC_VER 标记结束"""

                follow_up_response = client.chat.completions.create(
                    max_tokens=32000,
                    model=model,
                    messages=[
                        {"role": "user", "content": get_prompt_gen_analysis(prev_reply_str_desc, content_str[i])},
                        {"role": "assistant", "content": reply_str},
                        {"role": "user", "content": continue_prompt}
                    ],
                    stream=False
                )
                follow_up_content = follow_up_response.choices[0].message.content
                if follow_up_content:
                    reply_str += follow_up_content

            # Split demo and description
            reply_str_demo, prev_reply_str_desc = reply_str.split("^^SHENGOOVLEI&&", 1)
            # Remove END_MARKER if present
            prev_reply_str_desc = prev_reply_str_desc.replace("SOLYN_AC_VER", "").strip()
            print(f"第{i + 1}部分分析完毕！示例续写：\n{reply_str_demo}\n")
            with open(file_name_desc, 'w', encoding=encoding_format) as file:
                print(prev_reply_str_desc, file=file)
            with open(file_name_demo, 'a', encoding=encoding_format) as file:
                print(reply_str_demo, file=file)
    
    print(f'\n\n=======================\n分析完毕！\n分析结果已存入根目录下的{file_name_desc}.txt')



# main entrance of the program
if __name__ == "__main__":
    main()