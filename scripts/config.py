"""
内容日历配置
推广链接改为运行时从 API 获取（scripts/fetch_affiliates.py）
"""

import datetime
import os

# ============================================================
# 内容类型定义（每天动态生成本日话题，不再写死 49 个话题）
# 类型轮换保证 40% 推广 / 60% 干货 的平衡
# ============================================================

# 每一天的类型定义（顺序按天循环，保证类型分布均匀）
CONTENT_TYPE_CYCLE = [
    {"type": "buying_guide",   "style": "guide",      "category": "网络加速", "promotional": True},
    {"type": "review",         "style": "review",     "category": "网络加速", "promotional": True},
    {"type": "ai_tutorial",    "style": "tutorial",   "category": "AI",       "promotional": False},
    {"type": "guide",          "style": "guide",      "category": "网络加速", "promotional": False},
    {"type": "comparison",     "style": "comparison", "category": "网络加速", "promotional": True},
    {"type": "troubleshooting","style": "guide",      "category": "网络加速", "promotional": False},
    {"type": "guide",          "style": "experience", "category": "AI",       "promotional": False},
]

# 话题生成模板（DeepSeek API 不可用时的备用方案）
TOPIC_TEMPLATES = {
    "buying_guide": [
        "网络加速服务选购指南：怎么找到最适合自己的",
        "不同预算怎么选？从入门到高端的网络加速方案",
        "新手买网络加速服务防坑指南",
        "{affiliates} 这几家怎么选？真实对比告诉你",
    ],
    "review": [
        "深度体验分享：最近在用的网络加速服务",
        "长期使用后的真实感受：好坏都说清楚",
        "{affiliate} 用了几个月的真实评测",
    ],
    "comparison": [
        "主流网络加速服务横向对比：哪家更适合你",
        "线路类型大对比：专线 vs IEPL vs 中转 vs 家宽",
        "几家热门服务商实测对比：谁才是性价比之王",
    ],
    "guide": [
        "网络加速客户端配置教程：新手也能看懂",
        "多设备共享网络加速的最佳方案",
        "从零开始配置网络加速工作流",
    ],
    "ai_tutorial": [
        "近期值得关注的 AI 工具推荐",
        "AI 工具组合工作流：效率翻倍的秘诀",
        "2026年热门 AI 工具使用教程",
    ],
    "troubleshooting": [
        "网络加速常见问题排查手册",
        "晚高峰卡顿怎么办？实用技巧汇总",
        "网络加速突然用不了？一步步排查",
    ],
}

# 旧日历话题存档（仅用于 is_duplicate 检测，不再用于选择话题）
_CONTENT_CALENDAR_ARCHIVE = [
    {"topic": "2026年网络加速服务选购指南：教你找到最适合自己的"},
    {"topic": "月付10元 vs 月付50元：不同价位的网络加速差别有多大"},
    {"topic": "学生党怎么选网络加速服务？预算有限也能用好"},
    {"topic": "外贸打工人必备的网络加速工具推荐"},
    {"topic": "2026年新手买网络加速服务防坑指南"},
    {"topic": "自由猫 Freecat 深度测评：用了半年的真实体验"},
    {"topic": "奈云 IEPL 专线体验：168元年付到底值不值"},
    {"topic": "一枝红杏10年老牌机场评测：老品牌还值得信赖吗"},
    {"topic": "万达云 vs 龙猫云：两家同价位服务商对比实测"},
    {"topic": "悠兔 YouTu 低调运营的优质机场开箱测评"},
    {"topic": "ChatGPT 国内使用完整教程 2026"},
    {"topic": "Claude 3.5 中文使用指南：比ChatGPT强在哪"},
    {"topic": "Cursor AI 编程工具入门：不会代码也能写程序"},
    {"topic": "Midjourney 2026 最新使用指南：从注册到出图"},
    {"topic": "2026年必装的10个AI工具，提升工作效率200%"},
    {"topic": "用 AI 写公众号文章的完整工作流"},
    {"topic": "Perplexity AI 搜索工具使用教程：比Google更好用"},
    {"topic": "我用了3年网络加速服务，总结出这5条经验"},
    {"topic": "Clash Verge 客户端配置教程：小白也能看懂"},
    {"topic": "2026年主流客户端对比：Clash vs Sing-Box vs Surge"},
    {"topic": "iOS/iPad 上最好的网络加速工具推荐"},
    {"topic": "Android 手机网络加速配置教程"},
    {"topic": "Mac 上配置网络加速的几种方式对比"},
    {"topic": "常见网络加速连接失败问题排查手册"},
    {"topic": "晚高峰卡顿怎么办？5个技巧提升速度"},
    {"topic": "网络加速服务突然用不了？先别急着重装"},
    {"topic": "如何测试你的网络加速服务速度"},
    {"topic": "2026年十大主流网络加速服务横向评测"},
    {"topic": "IEPL专线 vs 普通中转：到底差在哪"},
    {"topic": "年付套餐值不值？帮你算一笔账"},
    {"topic": "2026年 AI 工具发展趋势：哪些值得关注"},
    {"topic": "DeepSeek 2026 使用指南：国产AI的进步"},
    {"topic": "2026年主流网络加速服务线路类型横向评测：专线、IEPL、中转、家宽全解析"},
    {"topic": "从0到1搭建自己的网络加速工作流：客户端选择与配置最佳实践"},
    {"topic": "AI效率工具组合：用Perplexity搜索+ChatGPT写作+Claude润色的完整内容生产链"},
    {"topic": "专线服务商深度体验：连续使用三个月的网络延迟数据对比"},
    {"topic": "2026年使用Sora生成视频完整教程：从注册到出片"},
    {"topic": "家庭多设备共享网络加速的最佳方案：路由器端配置详解"},
    {"topic": "三大入门级IEPL服务商横向对比：自由猫、奈云、MESL实测数据大公开"},
    {"topic": "不会写代码也能制作Clash配置文件？ChatGPT帮你搞定"},
    {"topic": "2026年入门级专线服务商深度横评：便宜也有好货？实测六家百元级年付服务商"},
    {"topic": "外贸行业专用网络加速配置指南：如何同时访问多个海外AI工具且不卡顿？"},
    {"topic": "家宽线路真的比专线慢吗？悠兔家宽一个月深度体验报告"},
    {"topic": "月付5元能买到什么样的网络加速？新华云NewHua99低价套餐实测"},
    {"topic": "闪狐云 vs 贝贝云：两家热门中转线路服务商横向对比"},
    {"topic": "iOS端网络加速工具横评：Surge、Quantumult X、Stash三款付费工具实测"},
    {"topic": "网络加速后依然被屏蔽？DNS泄露自查与修复指南"},
    {"topic": "手动搭建网络加速服务 vs 商业服务：成本与隐私的全面对比"},
    {"topic": "零隐私泄露的网络加速方案：手动配置让你的数据完全自主可控"},
]

# 兼容旧代码：CONTENT_CALENDAR 指向类型循环
CONTENT_CALENDAR = CONTENT_TYPE_CYCLE

# ============================================================
# 内容生成策略配置
# ============================================================
WRITING_STRATEGY = {
    "tone": "像一个真实付费用户分享经验，而非营销号",
    "trust_builders": [
        "强调真实付费使用",
        "主动列出缺点（反直觉坦诚建立信任）",
        "分享踩坑经历（拉近距离）",
        "建议先月付试用（劝用户谨慎）",
    ],
    "banned_words": ["翻墙", "梯子", "VPN", "科学上网", "富强"],
    "safe_alternatives": {
        "翻墙": "访问外网",
        "梯子": "网络加速工具",
        "VPN": "网络加速服务",
        "科学上网": "访问国际网络",
        "节点": "接入点",
        "机场": "网络服务商",
    },
    "affiliate_placement": "在推荐具体服务商时使用推广链接，非推荐类内容不使用",
}

# ============================================================
# 话题生成
# ============================================================

PROJECT_START_DATE = datetime.date(2026, 5, 25)

# DeepSeek API 配置（用于动态生成话题）

# DeepSeek API 配置（用于动态生成话题）
DEEPSEEK_API_URL = "https://api.deepseek.com/v1/chat/completions"

PROMOTIONAL_TYPES = {"buying_guide", "review", "comparison"}
EDUCATIONAL_TYPES = {"ai_tutorial", "guide", "troubleshooting"}


def is_promotional(topic):
    """判断话题是否为推广向"""
    return topic.get("type") in PROMOTIONAL_TYPES


def get_available_affiliate_names(affiliates=None):
    """获取可用的推广商名称列表（排除不推荐的）"""
    if not affiliates:
        return []
    names = []
    for name, info in affiliates.items():
        if name in ("Test",):
            continue
        note = info.get("note", "")
        if "不推荐" in note or "一般般" in note:
            continue
        names.append(name)
    return names


def _generate_topic_via_api(content_type, style, category, affiliate_names, days_since_start):
    """
    调用 DeepSeek API 生成新鲜话题
    返回话题名称字符串，失败返回 None
    """
    api_key = os.environ.get("DEEPSEEK_API_KEY", "")
    if not api_key:
        return None

    promo_types = {"buying_guide": "选购指南", "review": "评测", "comparison": "对比评测"}
    edu_types = {"ai_tutorial": "AI工具教程", "guide": "实用指南", "troubleshooting": "故障排查"}
    type_name = promo_types.get(content_type) or edu_types.get(content_type, content_type)

    # 构建推广商上下文
    aff_context = ""
    if affiliate_names:
        aff_context = f"可用的推广服务商：{'、'.join(affiliate_names[:8])}\n（如果内容类型适合，可以自然地推荐其中1-2家）"

    # 从运行历史中获取已生成过的话题
    already_used = set()
    try:
        from scripts.content_tracker import get_all_generated_topics
        already_used = set(get_all_generated_topics())
    except Exception:
        pass
    # 只排除过去7天的，避免重复
    try:
        from scripts.content_tracker import load_history
        hist = load_history()
        cutoff = len(hist) - 7
        recent_used = set(r["topic"] for r in hist[cutoff:] if cutoff > 0) if hist else set()
        if hist and cutoff <= 0:
            recent_used = set(r["topic"] for r in hist)
    except Exception:
        recent_used = set()

    recent_context = ""
    if recent_used:
        recent_context = f"最近已发布的内容：{'、'.join(list(recent_used)[:5])}\n请避免生成完全相同的话题。"

    prompt = f"""你是一个中文内容编辑，请为一个科技博客生成一个今日话题。

【内容类型】{type_name}
【写作风格】{style}
【品类】{category}

{aff_context}
{recent_context}

要求：
1. 生成一个吸引人的中文话题标题（15-30字）
2. 话题要贴合当前的科技趋势和热门话题（现在是{datetime.date.today().isoformat()}）
3. 要有实质内容，不要空洞
4. 如果是推广类（选购/评测/对比），要自然地结合推广服务商
5. 如果是干货类（教程/指南/排查），要实用、有信息量
6. 只需要返回话题标题本身，不要加引号、序号、额外说明

示例输出：Claude 全新功能体验：AI 写作能力到底有多强
"""

    try:
        import requests
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}",
        }
        payload = {
            "model": os.environ.get("DEEPSEEK_MODEL", "deepseek-v4-flash"),
            "messages": [
                {"role": "system", "content": "你是一个科技博客的编辑，擅长生成吸引人且有实际内容的中文话题标题。"},
                {"role": "user", "content": prompt},
            ],
            "temperature": 0.85,
            "max_tokens": 100,
        }
        resp = requests.post(DEEPSEEK_API_URL, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        topic = resp.json()["choices"][0]["message"]["content"].strip()
        # 清理：去掉可能的引号、序号、多余空格
        topic = topic.strip('"\'„"”「」『』').strip()
        # 去掉开头的数字序号如 "1." "1、" "1."
        import re
        topic = re.sub(r'^\d+[\.\、\．]\s*', '', topic)
        if topic:
            return topic
    except Exception as e:
        print(f"[Config] Topic API failed: {e}")

    return None


def _generate_topic_fallback(content_type, style, category, affiliate_names):
    """
    备用方案：用模板生成话题
    加入日期和推广商名字使每次略有不同
    """
    import random
    templates = TOPIC_TEMPLATES.get(content_type, ["{type}相关话题"])
    rng = random.Random(datetime.date.today().toordinal())

    template = rng.choice(templates)
    year = datetime.date.today().year
    month = datetime.date.today().month

    # 如果有推广商名字，随机选一个填入
    aff_name = rng.choice(affiliate_names) if affiliate_names else ""

    topic = template.format(
        year=year,
        month=month,
        affiliate=aff_name,
        affiliates=aff_name,
        type=content_type,
    )
    return topic


def get_current_topic(affiliates=None):
    """
    获取今天应该写的内容（每天动态生成新鲜话题）

    流程：
    1. 从类型循环中选出今天的 content_type
    2. 先用 DeepSeek API 生成新鲜话题（结合当前趋势）
    3. API 失败时回退到模板生成
    4. 模板也无法匹配时用最后的兜底标题
    """
    days = (datetime.date.today() - PROJECT_START_DATE).days
    index = days % len(CONTENT_TYPE_CYCLE)
    type_def = CONTENT_TYPE_CYCLE[index]

    content_type = type_def["type"]
    style = type_def["style"]
    category = type_def.get("category", "网络加速")

    # 获取推广商名字（用于话题生成上下文）
    affiliate_names = get_available_affiliate_names(affiliates)

    # 第1步：尝试 API 生成
    topic = _generate_topic_via_api(content_type, style, category, affiliate_names, days)

    # 第2步：API 失败，用模板回退
    if not topic:
        topic = _generate_topic_fallback(content_type, style, category, affiliate_names)

    # 第3步：最终兜底
    if not topic:
        type_labels = {
            "review": "网络加速服务评测",
            "buying_guide": "网络加速选购指南",
            "comparison": "网络加速服务对比",
            "guide": "网络加速配置教程",
            "ai_tutorial": "AI工具使用指南",
            "troubleshooting": "网络加速问题排查",
        }
        topic = f"{datetime.date.today().isoformat()} {type_labels.get(content_type, '网络加速相关内容')}"

    description_map = {
        "review": f"真实评测分享：{topic}",
        "buying_guide": f"选购指南：教你怎么选{topic}",
        "comparison": f"多维度对比分析：{topic}",
        "guide": f"手把手教程：{topic}",
        "ai_tutorial": f"AI工具教程：{topic}",
        "troubleshooting": f"问题排查指南：{topic}",
    }

    return {
        "type": content_type,
        "topic": topic,
        "style": style,
        "description": description_map.get(content_type, topic),
        "image_label": type_def.get("image_label", content_type),
        "category": category,
        "week_num": days // 7,
        "cycle_index": index + 1,
        "total_cycles": len(CONTENT_TYPE_CYCLE),
    }


def get_output_filename(topic_info):
    """生成输出文件名"""
    date_str = datetime.date.today().isoformat()
    safe_name = topic_info["topic"].replace(" ", "_").replace("?", "").replace("：", "_").replace(":", "_")
    # 截断过长文件名
    if len(safe_name) > 80:
        safe_name = safe_name[:80]
    return f"{date_str}_{safe_name}"
