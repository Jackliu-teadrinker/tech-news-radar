#!/usr/bin/env python3
"""Direction + company configuration for Tech Radar — 10 个新闻方向 + 四层框架。

每条新闻会同时被打上：
- direction: 10 个新闻方向之一（"" = 未命中）
- direction_hits: 全部命中的方向（含次级）
- companies: 命中的关注企业清单

四层框架（framework_layer）：
- hardware: 硬件底座
- software: 软件应用
- terminal: 终端场景
- frontier: 未来前沿（低权重观察）

扩充方向/加企业/调关键词，只改本文件。
关键词匹配规则：长度 >= 2（中文 >= 1）才算有效；过短的 ASCII 词会被分类器自动忽略。
"""

from __future__ import annotations

FRAMEWORK_LAYERS: list[dict] = [
    {"id": "hardware", "name": "硬件底座", "description": "芯片、封测、设备、材料、光、电、航天硬件、能源电力"},
    {"id": "software", "name": "软件应用", "description": "大模型、Agent、B 端落地、数据与 AI 治理"},
    {"id": "terminal", "name": "终端场景", "description": "手机/PC/眼镜/车载/机器人整机，端侧推理与交互"},
    {"id": "frontier", "name": "未来前沿", "description": "量子、光计算、太空计算、6G、脑机、核聚变（低权重观察）"},
]

DIRECTIONS: list[dict] = [
    # ═══════════════ 硬件底座 ═══════════════
    {
        "id": "compute_dc",
        "name": "算力与数据中心基建",
        "framework_layer": "hardware",
        "companies": [
            "寒武纪", "海光", "燧原", "沐曦", "摩尔线程", "壁仞", "天数智芯",
            "nvidia", "英伟达", "amd", "intel", "博通", "broadcom", "marvell",
            "中际旭创", "新易盛", "旭创", "coherent", "光迅科技", "天孚通信",
            "沪电股份", "深南电路", "生益科技", "胜宏科技",
            "浪潮信息", "中科曙光", "超聚变", "新华三", "超微电脑",
            "英维克", "申菱环境", "佳力图",
        ],
        "keywords": [
            # 国产算力芯片/超节点
            "寒武纪", "海光", "燧原", "沐曦", "摩尔线程", "壁仞", "天数智芯",
            "万卡", "超节点", "智算", "智算中心", "ai 服务器", "推理芯片",
            "训练芯片", "算力芯片", "cann", "昇腾", "ascend",
            # 高速互连/光模块
            "光模块", "光芯片", "cpo", "co-packaged", "硅光",
            "1.6t", "800g", "光互连", "infiniband", "高速互连",
            "lpo", "eml", "中际旭创", "新易盛", "光迅",
            # PCB/CCL
            "pcb", "ccl", "覆铜板", "mlcc", "高频高速", "lcp",
            "hdi", "背板", "高速板", "沪电", "深南电路",
            # HBM/存储
            "hbm", "hbm4", "hbm3e", "cxl", "存储", "ddr",
            "nvme", "ymtc", "长存", "cxmt", "长鑫",
            # 液冷/供配电
            "liquid cooling", "液冷", "冷板", "浸没", "cd", "ups",
            "供配电", "预制化机房", "hvdc", "microgrid", "机房",
            # 数据中心
            "data center", "数据中心", "机柜", "pue",
            "算力", "tpu", "gpu", "npu", "asic", "inference",
            "nvidia", "rtx", "geforce", "数据中心电力",
        ],
        "points": [
            "国产训练/推理芯片、超节点、高速互连",
            "光模块/CPO、PCB/CCL、HBM 与存储",
            "液冷 CDU、供配电/UPS/电源、预制化机房",
        ],
    },
    {
        "id": "semiconductor",
        "name": "半导体与电子基础",
        "framework_layer": "hardware",
        "companies": [
            "nvidia", "英伟达", "amd", "intel", "高通", "博通", "联发科",
            "海光", "寒武纪", "华为海思", "marvell",
            "中芯国际", "smic", "联", "tsmc", "台积电",
            "日月光", "长电科技", "通富微电", "华天科技", "晶方科技",
            "北方华创", "中微", "拓荆", "盛美", "华海清科", "中科飞测",
            "amats", "东京电子", "asml",
            "沪硅产业", "立昂微", "sumco", "信越", "jmc",
            "synopsys", "cadence",
            "村田", "三环", "风华",
            "禾赛", "速腾", "图达通",
        ],
        "keywords": [
            # ① 芯片设计
            "cpu", "gpu", "asic", "fpga", "soc", "存储芯片",
            "analog", "模拟", "sensor", "传感", "risc-v", "ip 授权",
            "芯片", "die", "foundry", "晶圆代工",
            # ② 制造与先进封装
            "fab", "晶圆", "wafer", "成熟制程", "先进制程",
            "co", "cowos", "3d", "三维集成",
            "chiplet", "先进封装", "封测", "osat",
            # ③ 设备/材料/EDA
            "光刻", "光刻机", "asml", "涂胶显影",
            "量测", "刻蚀", "c", "p", "cmp", "光刻胶",
            "硅片", "电子特气", "靶材", "eda",
            # ④ 元器件/光子
            "mlcc", "mems", "光芯片", "光收发", "光模块",
            "激光雷达", "光电", "高频高速", "光电器件",
            "半导体", "集成电路", "国产替代", "国产化", "良率",
        ],
        "points": [
            "芯片设计（CPU/GPU/ASIC/存储/模拟/传感）",
            "制造与先进封装（成熟+先进制程、CoWoS 类、三维集成）",
            "设备/材料/EDA（刻蚀、薄膜、量测、光刻胶、硅片）",
            "元器件与光子（MLCC、MEMS、光芯片、光收发、激光雷达）",
        ],
    },
    {
        "id": "space_hardware",
        "name": "商业航天/卫星/时空信息（硬件）",
        "framework_layer": "hardware",
        "companies": [
            "蓝箭", "朱雀", "东方空间", "引力", "快",
            "天兵", "深蓝", "星河", "谷神星",
            "垣信", "千帆", "星网", "中国卫星", "上海瀚讯", "铖昌",
            "天银机电", "臻镭", "海格通信", "华测导航", "北斗星通",
            "星测星联",
        ],
        "keywords": [
            # 火箭
            "火箭", "rocket", "发射", "launch", "orbital", "回收",
            "一箭多星", "海上发射", "可复用", "朱雀", "引力", "长征",
            "快", "深蓝", "天兵", "星河",
            # 卫星总装与载荷
            "卫星", "satellite", "载荷", "payload",
            "相控阵", "starlink",
            "千帆", "垣信", "星网", "中国卫星", "上海瀚讯", "铖昌",
            "天银", "臻镭", "星敏", "星载", "信关站",
            "基带", "手机直连", "手机直连卫星", "车规卫星", "北斗",
            "卫星互联网", "北斗芯片",
        ],
        "points": [
            "火箭（可回收、一箭多星、海上发射）",
            "卫星总装与载荷、T/R/星敏/电源/相控阵",
            "地面信关站、北斗芯片与终端、手机直连卫星",
        ],
    },
    {
        "id": "autonomous_hardware",
        "name": "智能车硬件（传感器/域控）",
        "framework_layer": "hardware",
        "companies": [
            "nvidia", "英伟达", "地平线", "黑芝麻", "华为",
            "禾赛", "速腾", "图达通", "robosense", "robotechnik",
            "经纬恒润", "德赛西威", "均胜电子",
        ],
        "keywords": [
            # 智驾芯片/域控
            "智驾", "驾驶芯片", "域控", "nvidia drive", "oem",
            # 传感器
            "激光雷达", "禾赛", "速腾", "图达通", "毫米波",
            "camera", "惯导", "lidar",
            # 车路云
            "车路云", "路侧单元", "高精地图", "高精度地图",
            "v2x", "cooperative", "北斗", "商用车",
        ],
        "points": [
            "智驾芯片/域控（英伟达、地平线、黑芝麻、华为 MDC）",
            "激光雷达/4D 毫米波/相机（禾赛、速腾、图达通）",
            "高精地图/车路云（路侧单元、北斗终端）",
        ],
    },
    {
        "id": "robotics_hardware",
        "name": "机器人核心部件",
        "framework_layer": "hardware",
        "companies": [
            "绿的", "鸣志", "柯力", "昊志", "汇川",
            "harmonic", "step",
            "安川", "mazda",
        ],
        "keywords": [
            # 核心部件
            "减速器", "谐波", "行星", "滚柱", "harmonic",
            "servo", "伺服", "力矩传感器", "torque", "im",
            "灵巧手", "端侧控制器", "微电机", "actuator",
            "绿的", "鸣志", "柯力", "昊志", "汇川",
            # 工业机器人
            "工业机器", "四足", "无人机", "无人车",
            "机器人", "robot",
        ],
        "points": [
            "减速器、伺服、力矩/视觉/IMU 传感器、控制器",
            "灵巧手、端侧控制器、微电机",
            "工业机器人、四足、无人车/无人机",
        ],
    },
    {
        "id": "energy_hardware",
        "name": "能源电子与算电协同（电力硬件）",
        "framework_layer": "hardware",
        "companies": [
            "宁德时代", "宁德", "国轩", "比亚迪", "孚能", "亿纬", "鹏辉",
            "阳光电源", "华为数字能源", "士兰微", "斯达", "时代电气",
        ],
        "keywords": [
            # 储能/电池
            "lithium", "锂电", "lithium battery", "sodium", "钠",
            "固态电池", "all", "液流", "flow",
            "储能", "ess", "inverter", "逆变器", "光伏", "solar",
            "组件", "光伏组件", "钙钛矿", "perovskite", "动力电池",
            "电池回收", "recycling",
            # 数据中心电力
            "ups", "hvdc", "si", "ga", "变压器",
            "generator", "microgrid", "机房用电", "电力",
            "备用电源", "绿电", "renewable",
            # 算电协同
            "pue", "绿电", "token 成本", "机柜功率",
            "kwh", "电价", "data center power", "算电协同",
        ],
        "points": [
            "储能、固态/钠电/液流、光伏与钙钛矿、电池回收",
            "数据中心电力（HVDC、SiC/GaN、变压器、绿电微网）",
        ],
    },
    # ═══════════════ 软件应用 ═══════════════
    {
        "id": "ai_models_apps",
        "name": "AI 大模型与软件应用",
        "framework_layer": "software",
        "companies": [
            "openai", "anthropic", "google", "gemini", "deepseek",
            "豆包", "字节", "通义", "阿里", "智谱", "月之暗面", "kimi",
            "minimax", "阶跃", "零一万物", "商汤", "百度", "腾讯",
            "cursor", "perplexity", "meta",
        ],
        "keywords": [
            # 基础层：大模型迭代
            "gemini", "gpt", "claude", "deepseek", "豆包", "通义", "qwen",
            "智谱", "glm", "kimi", "月之暗面", "mistral", "llama",
            "llm", "大模型", "foundation model", "推理成本", "inference cost",
            "token", "多模态", "multimodal", "agent", "智能体",
            "mcp", "tool use", "function calling", "reasoning",
            # 应用层：B 端落地
            "办公", "客服", "研发", "code", "编程", "财务",
            "制造", "医疗", "教育", "enterprise", "s",
            "vertical ai", "copilot", "虚拟员工", "工单", "知识库",
            "openai", "anthropic", "cursor", "codex", "claude code",
            "github", "copilot", "ai 助手", "ai assistant", "融资", "funding",
            "task", "seat",
        ],
        "points": [
            "基础层：大模型迭代、推理成本、多模态、Agent 工作流",
            "应用层：办公、客服、研发、财务、制造、医疗、教育 B 端落地",
        ],
    },
    {
        "id": "security_governance",
        "name": "网络安全/数据/AI 治理",
        "framework_layer": "software",
        "companies": [
            "安恒", "启明", "永信", "奇安信", "深信服", "绿盟", "天融信",
            "360", "亚信", "中孚", "电科网安",
        ],
        "keywords": [
            # AI 治理
            "ai", "模型安全", "agent 权限", "agentic",
            "data", "数据出境", "privacy", "隐私", "compliance", "合规",
            "deepfake", "深伪", "自动驾驶责任",
            "等保", "classified", "靶场", "range", "合规测评",
            "网安周", "安恒", "启明", "永信",
            # 数据
            "数据资产", "入表", "数据确权", "反垄断", "在线平台",
            "平台合规", "不正当竞争", "数据安全",
            "vulnerability", "漏洞", "exploit", "ransomware", "cyber",
            "零信任", "zero trust", "siem", "soc",
        ],
        "points": [
            "模型安全、Agent 权限、数据出境、隐私",
            "AI 侵权/深伪/自动驾驶责任",
            "等保/靶场/合规测评",
        ],
    },
    # ═══════════════ 终端场景 ═══════════════
    {
        "id": "ai_terminal",
        "name": "端侧 AI 与消费电子",
        "framework_layer": "terminal",
        "companies": [
            "苹果", "apple", "iphone", "华为", "荣耀", "vivo", "oppo",
            "小米", "三星", "samsung", "魅族", "联想",
            "meta", "vision", "ray", "xreal", "rokid", "影目", "雷鸟",
            "科大讯飞", "安克", "anker",
        ],
        "keywords": [
            # 端侧 AI 手机/PC
            "iphone", "ipad", "mac", "macbook", "pixel", "galaxy",
            "骁龙", "qualcomm", "联发科", "media", "天玑",
            "荣耀", "vivo", "oppo", "小米", "三星", "samsung", "魅族",
            "努比亚", "nubia", "联想", "手机", "pc",
            "端侧", "on-device", "npu", "lpddr", "端侧大模型", "端侧 ai",
            "ai 手机", "手机直连", "车载", "工业",
            # 智能眼镜/AR/VR
            "智能眼镜", "眼镜", "ar", "vr", "xr", "vision", "ray",
            "xreal", "rokid", "影目", "硅基oled", "光波导", "波导",
            "低功耗", "wearable", "可穿戴", "watch",
            # 视听终端
            "视听", "speaker", "camera", "display", "oled",
            "micro-ole", "laser",
            # OS/端侧 Agent
            "系统", "agent", "跨app", "跨应用", "自动执行",
            "隐私", "harmony", "鸿蒙", "magicos", "aosp",
            "android", "ios", "windows", "端侧大模型",
        ],
        "points": [
            "手机、PC、AI 眼镜/AR、可穿戴、视听终端、车载/工业/商业终端",
            "端侧推理芯片、NPU、LPDDR/存储、OS",
            "端侧大模型与 Agent、隐私与跨 App 自动执行",
        ],
    },
    {
        "id": "autonomous_vehicle",
        "name": "智能车与自动驾驶（整车/软件）",
        "framework_layer": "terminal",
        "companies": [
            "特斯拉", "tesla", "fsd", "小鹏", "xiaopeng", "理想",
            "li auto", "蔚来", "nio", "华为", "问界", "赛力斯",
            "零跑", "leapmotor", "比亚迪", "byd", "小米汽车", "极氪",
            "地平线", "黑芝麻", "momenta",
        ],
        "keywords": [
            # 整车与渠道
            "赛力斯", "零跑", "leapmotor", "世界模型",
            "byd", "比亚迪", "固态", "智驾", "smart driving",
            "autonomous", "ad", "oem",
            "特斯拉", "tesla", "fsd", "cyber", "小鹏", "xiaopeng",
            "理想", "蔚来", "nio", "华为", "问界", "小米汽车", "极氪",
            # 软件分账/订阅
            "渠道分账", "分账", "软件订阅", "subscription", "销量结构",
            "库存", "销售费用", "毛利", "软件毛利", "tco", "ota",
            "座舱", "cabin", "座舱 agent", "vla", "大模型智驾",
            "world model", "物理ai", "physical ai",
        ],
        "points": [
            "大模型智驾 VLA、座舱 Agent",
            "整车看渠道分账、软件订阅、销量结构、库存与销售费用率",
        ],
    },
    {
        "id": "robotics",
        "name": "机器人与具身智能（整机）",
        "framework_layer": "terminal",
        "companies": [
            "优必选", "ubtech", "宇树", "unitree", "智元", "zhiyuan",
            "乐聚", "legue", "东风", "小米", "figure",
            "bo", "agibot",
        ],
        "keywords": [
            # 人形/工业具身
            "优必选", "宇树", "智元", "乐聚", "东风", "humanoid",
            "具身", "工业机器", "万台产线", "节拍", "故障率",
            "figure", "bo", "bo", "小米",
            # 仿真/数据/模型
            "遥操", "sim", "vla", "视觉", "数据闭环",
            "仿真", "simulation", "digital twin", "数字孪生",
            "robot", "robotics", "embodied", "四足", "灵巧", "人形",
            "协作", "cooperative",
        ],
        "points": [
            "人形、工业机器人、无人车/无人机",
            "仿真/数据/模型：遥操数据、Sim2Real、VLA",
            "看万台产线、节拍、故障率、单台 TCO",
        ],
    },
    # ═══════════════ 未来前沿（低权重观察） ═══════════════
    {
        "id": "frontier",
        "name": "前沿未来产业",
        "framework_layer": "frontier",
        "weight": "low",
        "companies": [
            "quantinuum", "ionq", "rigetti", "国盾", "本源", "quantum",
            "国星宇航", "星算", "starlink",
            "neuralink", "强脑", "脑虎",
            "低空", "e", "verde",
            "能量奇点", "星环聚能", "诺瓦聚变",
        ],
        "keywords": [
            # 量子
            "quantum", "量子", "量子计算", "量子计算机", "qubit", "superconducting",
            "光计算", "photonics", "类脑", "neuromorphic",
            "存算一体", "compute-in-memory",
            # 太空计算
            "space computing", "space ai", "星算", "国星宇航",
            "在轨", "on-orbit", "satellite ai", "on-orbit inference",
            "太空算力", "太空数据",
            # 6G
            "6g", "thz", "terahertz", "integrated sensing",
            # 脑机接口
            "bci", "brain", "脑机", "neuralink", "强脑", "脑虎",
            # 低空
            "低空", "evtol", "e", "verde", "无人机",
            "drone", "vertol",
            # 核聚变
            "fusion", "核聚变", "可控核聚变", "tokamak", "stellar",
            "能量奇点", "星环聚能", "诺瓦聚变",
        ],
        "points": [
            "量子计算、光计算/类脑/存算一体",
            "太空计算、6G、脑机接口",
            "低空飞行器、可控核聚变",
        ],
    },
]

DIRECTION_BY_ID = {d["id"]: d for d in DIRECTIONS}
DIRECTION_ORDER = [d["id"] for d in DIRECTIONS]

# 四层框架 → 方向映射
LAYER_TO_DIRECTIONS: dict[str, list[str]] = {}
for _d in DIRECTIONS:
    LAYER_TO_DIRECTIONS.setdefault(_d["framework_layer"], []).append(_d["id"])


def get_direction_keywords() -> dict[str, list[str]]:
    """Map direction_id -> valid (len>=2 ascii / len>=1 cjk) keyword list."""
    out = {}
    for d in DIRECTIONS:
        valid = []
        for k in d["keywords"]:
            kl = k.lower()
            # skip single-char ascii (too generic); keep single CJK char
            if kl.isascii() and len(kl) < 2:
                continue
            valid.append(kl)
        out[d["id"]] = valid
    return out


def get_company_keywords() -> dict[str, list[str]]:
    """Map lower-cased company name -> [display variants]. De-duped globally."""
    seen: dict[str, list[str]] = {}
    for d in DIRECTIONS:
        for c in d.get("companies", []):
            lc = c.lower().strip()
            if not lc or (lc.isascii() and len(lc) < 2):
                continue
            seen.setdefault(lc, []).append(c)
    return seen


def direction_meta_payload() -> list[dict]:
    out = []
    for d in DIRECTIONS:
        out.append({
            "id": d["id"],
            "name": d["name"],
            "framework_layer": d.get("framework_layer", ""),
            "weight": d.get("weight", "normal"),
            "companies": d.get("companies", []),
            "points": d.get("points", []),
        })
    return out


def framework_layers_payload() -> list[dict]:
    out = []
    for layer in FRAMEWORK_LAYERS:
        out.append({
            **layer,
            "direction_ids": LAYER_TO_DIRECTIONS.get(layer["id"], []),
        })
    return out


def layer_of(direction_id: str) -> str:
    return DIRECTION_BY_ID.get(direction_id, {}).get("framework_layer", "")
