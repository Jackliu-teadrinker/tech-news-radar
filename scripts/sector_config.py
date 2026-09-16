#!/usr/bin/env python3
"""Sector configuration for Tech Radar — 8 大板块观察地图。

每个板块包含：
- id / name / aliases（用于前端 tab 与 URL 路由）
- keywords：命中即把 item 归入该板块（匹配前全部小写）
- points：前端可显示的"该板块在看什么"观察点

扩充新板块/加公司/调观察点，只改本文件，不用动 update_news.py。
"""

from __future__ import annotations

SECTORS: list[dict] = [
    # ─────────────────────────────────────────────────────────────
    {
        "id": "ai_compute",
        "name": "AI算力基础设施",
        "aliases": ["算力", "超节点", "万卡", "智算"],
        "keywords": [
            # 国产算力芯片/超节点
            "寒武纪", "海光", "燧原", "沐曦", "摩尔线程", "壁仞",
            "cann", "万卡", "超节点", "智算集采", "智算中心",
            "nvidia", "英伟达", "gb200", "gb300", "rubin", "h100", "h200",
            "hbm", "hbm4", "hbm3e",
            # 先进封装/存力
            "chiplet", "2.5d", "3d ic", "先进封装", "长鑫", "长存", "ymtc",
            "cxmt", "存储", "nvme", "cxl",
            # 光通信/CPO
            "1.6t", "800g", "光模块", "光芯片", "eml", "硅光",
            "npo", "cpo", "co-packaged optics", "光互连", "eoptolink",
            # PCB/CCL/元器件
            "pcb", "ccl", "覆铜板", "mlcc", "被动元件", "高频高速", "lcp",
            # 液冷/供配电/数据中心
            "liquid cooling", "液冷", "冷板", "浸没", "cd", "power supply",
            "ups", "供电", "预制化机房", "3d数据中心", "data center",
            "数据中心", "机柜", "kwh",
            # 算力指标
            "算力", "tpu", "token 单价", "token单价", "上架率",
            "gpu", "npu", "asic", "推理芯片", "训练芯片", "智算",
        ],
        "points": [
            "国产算力芯片/超节点：万卡扩展效率、CANN/算子适配、智算集采复购",
            "先进封装/存力：HBM、Chiplet、长鑫/长存存储、算力存力运力电力协同",
            "光通信/CPO：1.6T 光模块放量、EML/InP 上游瓶颈、硅光 NPO",
            "PCB/CCL：AI 服务器高阶 PCB/覆铜板/MLCC 涨价链，产能+长协验证",
            "液冷/供配电：单柜 100-200kW，冷板/浸没、CDU、UPS、预制化机房",
            "调研增量：单十万卡集群价值量拆解、液冷 CDU 毛利率、先进封装产能分配",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "semiconductor",
        "name": "半导体国产替代",
        "aliases": ["半导体", "晶圆", "fab", "扩产"],
        "keywords": [
            # 设备
            "刻蚀", "薄膜沉积", "c", "dep", "al", "涂胶显影", "量测",
            "减薄", "键合", "清洗设备",
            "北方华创", "中微", "拓荆", "盛美", "华海清科", "中科飞测",
            "amats", "lam", "k", "东京电子", "ulvac",
            # 材料
            "光刻胶", "resist", "电子特气", "特气", "cmp", "抛光液",
            "硅片", "单晶硅", "多晶硅", "靶材",
            # EDA/IP
            "eda", "synopsys", "cadence", "mentum", "risc-v", "arm",
            "ip 授权", "analog", "模拟芯片", "rfic", "射频",
            # 晶圆厂/扩产
            "中芯国际", "smic", "联", "umc", "tsmc", "台积电",
            "intel foundry", "晶圆厂", "fab", "wafer",
            # 国产替代
            "半导体", "国产替代", "国产芯片", "国产化", "良率", "封测",
            "集成电路", "chip", "芯片",
        ],
        "points": [
            "设备：刻蚀/CVD/ALD/涂胶显影/量测，按细分验证（北方华创/中微/拓荆/盛美/华海清科）",
            "材料：光刻胶/电子特气/CMP/靶材/硅片，看国产线验证导入而非送样",
            "EDA/IP：先进封装+系统级设计拉动国产 EDA；RISC-V/ARM 分开看",
            "传感器/模拟/射频：车规、工业、卫星链复用",
            "避坑：只写突破封锁无订单无良率的不做独家；问零部件国产化率、扩产资本开支、验收周期",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "ai_apps",
        "name": "AI应用与智能终端",
        "aliases": ["Agent", "端侧AI", "智能眼镜"],
        "keywords": [
            # 大模型/Agent
            "gemini", "gpt", "claude", "anthropic", "openai", "豆包",
            "通义", "deepseek", "智谱", "月之暗面", "kimi", "glm", "qwen",
            "agent", "智能体", "mcp", "tool use", "function calling",
            "copilot", "cursor", "codex", "claude code",
            # 办公/企服
            "feishu", "飞书", "钉钉", "企业微信", "wps", "用友", "金蝶",
            "虚拟员工", "s", "seat 收费", "s",
            # 端侧 AI 手机/PC/眼镜
            "天玑", "联发科", "media", "骁龙", "qualcomm",
            "magicos", "荣耀", "vivo", "蓝心", "努比亚",
            "端侧大模型", "npu", "lpddr", "端侧 ai",
            "智能眼镜", "ar 眼镜", "vr", "xr", "硅基oled", "光波导",
            "低功耗s", "多模态", "ai 手机", "ai pc", "手机直连",
            "车载", "industrial", "适老", "文旅",
        ],
        "points": [
            "大模型与 Agent：Gemini/OpenAI/Claude vs 豆包/通义/DeepSeek/智谱/月之暗面；企业级 Copilot 式 Agent",
            "办公/企服：飞书+豆包、钉钉、企业微信、WPS、用友/金蝶智能体；虚拟员工按 seat 还是 task 收费",
            "端侧 AI 手机/PC/眼镜：天玑 9600 Pro、骁龙新旗舰、荣耀 MagicOS、vivo 蓝心、努比亚实体 AI 键",
            "可穿戴/AR/VR/智能眼镜：硅基 OLED、光波导、低功耗 SoC、多模态交互",
            "公众号/虎嗅角度：系统层 Agent 是否架空 App；企业买 Agent 还是买 SaaS 席位",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "space",
        "name": "商业航天/卫星互联网/太空算力",
        "aliases": ["火箭", "星座", "千帆", "朱雀"],
        "keywords": [
            # 火箭
            "朱雀", "蓝箭", "引力一号", "引力二号", "东方空间", "长征",
            "快", "天兵", "深蓝", "星河",
            "发射", "launch", "orbital", "回收", "一箭多星", "火箭",
            # 卫星/星座
            "千帆", "垣信", "卫星", "星座", "starlink", "星网", "遥感",
            "中国卫星", "上海瀚讯", "铖昌", "天银", "臻镭",
            "leo", "小卫星", "m",
            # 地面段/终端
            "地面站", "相控阵", "基带", "手机直连卫星", "车载卫星",
            "北斗", "bei", "卫星通信", "终端",
            # 太空算力（前沿）
            "星算", "国星宇航", "在轨", "on-orbit", "太空算力",
            "satellite ai", "on-orbit inference", "太空数据",
        ],
        "points": [
            "火箭：朱雀（蓝箭）、引力（东方空间）、长征商业型号；看发射频次、一箭多星、回收、保险费率",
            "卫星/星座：千帆（垣信）、国网（星网）、遥感/物联网小星座；中国卫星总装 + 上海瀚讯/铖昌/天银/臻镭配套",
            "地面段/终端：信关站、相控阵、基带、手机直连、车规卫星通信",
            "太空算力（前沿）：国星宇航星算在轨大模型推理、太空算力控地面机器人；仍在试验/专网阶段",
            "独家增量：垣信/国网年度发包量、民营火箭复飞周期、单星 BOM 国产化率、在轨到营收转化周期",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "autonomous_vehicle",
        "name": "智能车与自动驾驶",
        "aliases": ["智驾", "VLA", "FSD", "车路云"],
        "keywords": [
            # 智驾芯片/域控
            "地平线", "黑芝麻", "华为mdc", "mdc", "nvidia drive",
            "自研芯片", "fsd", "cyber", "物理ai", "physical ai", "域控",
            "tesla", "特斯拉", "xiaopeng", "小鹏", "零跑", "问界", "赛力斯",
            "智驾", "智能驾驶", "autonomous", "oem",
            # 传感器
            "激光雷达", "禾赛", "速腾", "图达通", "robosense", "毫米波",
            "camera", "惯导", "lidar", "4d mmwave",
            # 整车/渠道
            "赛力斯", "赛", "零跑", "leapmotor", "世界模型", "byd", "比亚迪",
            "固态", "智驾", "smart driving", "autonomous",
            "ad", "level", "o",
            # 车路云/北斗
            "v", "路侧单元", "高精地图", "高精度地图", "北斗",
            "商用车", "fleet", "车路云",
        ],
        "points": [
            "智驾芯片/域控：英伟达、地平线、黑芝麻、华为 MDC、小鹏自研、特斯拉 FSD 对照",
            "传感器：激光雷达（禾赛/速腾/图达通）、4D 毫米波、摄像头、惯导",
            "整车与渠道：问界/赛力斯分账、小鹏 VLA、零跑世界模型、比亚迪智能化与固态节奏",
            "车路云/北斗：路侧单元、高精地图、北斗终端、商用车队管理",
            "独家角度：智驾从功能堆料转订阅收入+数据闭环；问界类渠道事件看技术授权费、流量费、门店成本重定价",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "robotics",
        "name": "机器人与具身智能",
        "aliases": ["人形机器人", "具身", "灵巧手"],
        "keywords": [
            # 人形/工业具身
            "优必选", "宇树", "智元", "乐聚", "东风", "humanoid",
            "具身", "工业机器", "万台产线", "故障率", "t",
            "ubtech", "unitree", "zhiyuan",
            # 核心部件
            "减速器", "谐波", "行星", "滚柱", "servo", "伺服",
            "力矩传感器", "torque", "灵巧手", "im",
            "端侧控制器", "绿的", "鸣志", "柯力", "昊志",
            "harmonic", "actuator", "motor", "微电机",
            # 仿真/数据/模型
            "遥操", "sim", "vla", "视觉", "数据闭环",
            "仿真", "simulation", "digital twin", "数字孪生",
            "机器人", "robot", "embodied", "四足", "灵巧",
        ],
        "points": [
            "人形/工业具身：优必选、宇树、智元、乐聚、东风；看万台产线、节拍、故障率、单台 TCO",
            "核心部件：减速器、伺服、力矩传感器、灵巧手、IMU、端侧控制器（绿的/鸣志/柯力/昊志）",
            "仿真/数据/模型：遥操数据、Sim2Real、VLA 模型，与太空算力/边缘算力协同",
            "独家增量：工厂场景 ROI 回收期 >1 年还是 <2 年；算法自研比例；车企/互联网/本体厂谁掌握数据",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "energy",
        "name": "能源电子/储能/算电协同",
        "aliases": ["储能", "电池", "电力", "算电协同"],
        "keywords": [
            # 储能/电池
            "lithium", "锂电", "lithium battery", "sodium", "钠", "固态电池",
            "储能", "ess", "逆变器", "光伏", "solar", "组件", "动力电池",
            "宁德", "国轩", "byd", "回收", "recycling",
            # 数据中心电力
            "ups", "hvdc", "si", "ga", "变压器", "微网", "microgrid",
            "机房用电", "电力", "备用电源",
            # 算电协同
            "pue", "绿", "绿电", "renewable", "token 成本", "机柜功率",
            "kwh", "电价", "data center power", "算电协同",
        ],
        "points": [
            "储能/电池：锂电储能、钠电、固态（比亚迪/宁德/国轩）；世界动力电池大会+回收标准催化",
            "数据中心电力：UPS、HVDC、SiC/GaN 功率、变压器、柴油/燃气备用、微网",
            "光伏/组件/逆变器：光伏出清+海外储能对冲，偏周期修复",
            "算电协同：Token 成本→机柜功率→电价/PUE→液冷+绿电，适合做 AI 能耗账单深度",
        ],
    },
    # ─────────────────────────────────────────────────────────────
    {
        "id": "policy",
        "name": "政策/安全/合规",
        "aliases": ["十五五", "AI治理", "数据出境"],
        "keywords": [
            # 十五五电子信息规划
            "十五五", "集成电路", "先进计算", "消费电子", "基础电子",
            "能源电子", "光子", "risc-v", "开源鸿蒙", "harmony", "鸿蒙",
            "全栈", "规划",
            # AI 治理
            "ai 治理", "agent 权限", "数据出境", "模型安全", "合规",
            "网安周", "安恒", "启明", "永信", "政企订单",
            # 平台/数据
            "数据资产", "入表", "反垄断", "在线平台", "平台合规",
            "不正当竞争",
        ],
        "points": [
            "十五五电子信息规划：集成电路、先进计算、消费电子、基础电子、能源电子、光子、RISC-V、开源鸿蒙、AI 硬件全栈",
            "AI 治理：Agent 权限、数据出境、模型安全评估；网安周框架 3.0 带动安全合规（安恒/启明/永信按政企订单看）",
            "平台/数据：数据资产入表、反垄断与不正当竞争、在线平台合规；偏媒体选题多于硬件调研",
        ],
    },
]

SECTOR_BY_ID = {s["id"]: s for s in SECTORS}

# 前端展示顺序 = SECTORS 顺序
SECTOR_ORDER = [s["id"] for s in SECTORS]


def get_keywords_for(sector_id: str) -> list[str]:
    """Return the lower-cased keyword list for a sector."""
    s = SECTOR_BY_ID.get(sector_id)
    if not s:
        return []
    return [k.lower() for k in s["keywords"]]


def get_all_keywords() -> dict[str, list[str]]:
    """Map sector_id -> lower-cased keyword list."""
    return {sid: get_keywords_for(sid) for sid in SECTOR_ORDER}


def sector_display_meta() -> list[dict]:
    """Return lightweight display metadata (no keyword lists) for UI payloads."""
    out = []
    for s in SECTORS:
        out.append({
            "id": s["id"],
            "name": s["name"],
            "aliases": s.get("aliases", []),
            "points": s.get("points", []),
        })
    return out
