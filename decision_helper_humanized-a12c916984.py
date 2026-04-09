#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策辅助工具 - 人性优化版本
用途：更人性、通俗、更具备常用价值的决策辅助工具
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd
import uuid
from collections import defaultdict


# 页面配置
st.set_page_config(
    page_title="AI决策小助手",
    page_icon="🤔",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 自定义样式
st.markdown("""
<style>
/* 全局样式 */
body {
    font-family: 'PingFang SC', 'Microsoft YaHei', sans-serif;
}

/* 按钮样式 */
.stButton>button {
    border-radius: 8px;
    border: none;
    background-color: #4CAF50;
    color: white;
    padding: 10px 24px;
    text-align: center;
    text-decoration: none;
    display: inline-block;
    font-size: 16px;
    margin: 4px 2px;
    cursor: pointer;
    transition-duration: 0.4s;
}

.stButton>button:hover {
    background-color: #45a049;
    transform: translateY(-2px);
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.2);
}

/* 卡片样式 */
.stCard {
    border-radius: 12px;
    box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
    padding: 20px;
    margin-bottom: 20px;
    transition: 0.3s;
}

.stCard:hover {
    box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
}

/* 进度条样式 */
.stProgress > div > div {
    background-color: #4CAF50;
}

/* 侧边栏样式 */
.css-1d391kg {
    background-color: #f8f9fa;
    border-right: 1px solid #e9ecef;
}

/* 标题样式 */
.css-10trblm {
    font-size: 28px;
    font-weight: 600;
    color: #2c3e50;
}

/* 文本样式 */
.css-16huue1 {
    font-size: 16px;
    line-height: 1.6;
    color: #34495e;
}

/* 成功提示 */
.stSuccess {
    background-color: #d4edda;
    border-left: 4px solid #155724;
    padding: 10px;
    border-radius: 4px;
}

/* 警告提示 */
.stWarning {
    background-color: #fff3cd;
    border-left: 4px solid #856404;
    padding: 10px;
    border-radius: 4px;
}

/* 信息提示 */
.stInfo {
    background-color: #d1ecf1;
    border-left: 4px solid #0c5460;
    padding: 10px;
    border-radius: 4px;
}

</style>
""", unsafe_allow_html=True)


# 预设决策场景
DECISION_SCENARIOS = {
    "职业选择": {
        "dimensions": [
            "💰 收入高低",
            "📈 发展前景",
            "⚖️ 工作生活平衡",
            "🧠 学习成长",
            "🏢 公司氛围",
            "🌍 城市吸引力",
            "⏰ 工作时间",
            "😀 工作开心度"
        ],
        "description": "找工作、换工作、创业、职业规划等",
        "emoji": "💼",
        "color": "#3498db"
    },
    "感情选择": {
        "dimensions": [
            "❤️ 彼此喜欢",
            "🤝 价值观一致",
            "💬 沟通顺畅",
            "🛡️ 安全感",
            "👨👩👧👦 家庭支持",
            "📈 共同成长",
            "💰 经济匹配",
            "😊 相处开心"
        ],
        "description": "谈恋爱、结婚、分手、感情问题等",
        "emoji": "💖",
        "color": "#e74c3c"
    },
    "生活选择": {
        "dimensions": [
            "🏠 居住舒适度",
            "💰 经济压力",
            "🚗 交通便利性",
            "📚 教育资源",
            "⚕️ 医疗资源",
            "🎭 生活娱乐",
            "👥 社交圈子",
            "😌 生活幸福感"
        ],
        "description": "买房、租房、搬家、城市选择等",
        "emoji": "🏠",
        "color": "#f39c12"
    },
    "消费选择": {
        "dimensions": [
            "💰 价格高低",
            "⚖️ 性价比",
            "🎯 功能需求",
            "🎨 外观颜值",
            "⚡ 使用频率",
            "⏳ 使用年限",
            "🔧 售后服务",
            "😊 购买开心度"
        ],
        "description": "买手机、电脑、家电、衣服等",
        "emoji": "🛍️",
        "color": "#9b59b6"
    },
    "其他选择": {
        "dimensions": [
            "👍 喜欢程度",
            "💰 成本高低",
            "⏳ 花费时间",
            "🎯 达成目标",
            "😌 内心感受",
            "🤔 后悔概率",
            "👥 他人看法",
            "✨ 独特价值"
        ],
        "description": "其他各种选择",
        "emoji": "🎯",
        "color": "#1abc9c"
    }
}


# 用户使用限制
FREE_USER_LIMIT = 3  # 免费用户每月限3次


def get_user_id():
    """获取或创建用户ID"""
    if 'user_id' not in st.session_state:
        st.session_state.user_id = str(uuid.uuid4())
    return st.session_state.user_id


def check_user_premium():
    """检查用户是否为付费用户"""
    if 'user_premium' not in st.session_state:
        st.session_state.user_premium = False
    return st.session_state.user_premium


def get_user_usage_count():
    """获取用户使用次数"""
    if 'usage_count' not in st.session_state:
        st.session_state.usage_count = 0
    return st.session_state.usage_count


def increment_usage_count():
    """增加用户使用次数"""
    st.session_state.usage_count = get_user_usage_count() + 1


# 数据统计功能
def init_user_data():
    """初始化用户数据存储"""
    if 'user_analytics' not in st.session_state:
        st.session_state.user_analytics = {
            "total_users": 0,
            "total_decisions": 0,
            "premium_conversions": 0,
            "scenario_usage": defaultdict(int),
            "user_actions": [],
            "conversion_events": [],
            "revenue": {
                "total": 0,
                "monthly": 0,
                "yearly": 0
            }
        }


def track_user_event(event_type, event_data):
    """记录用户行为事件"""
    if 'user_analytics' not in st.session_state:
        init_user_data()
    
    event = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user_id": get_user_id(),
        "event_type": event_type,
        "data": event_data
    }
    
    st.session_state.user_analytics['user_actions'].append(event)
    
    # 更新统计
    if event_type == "new_user":
        st.session_state.user_analytics['total_users'] += 1
    elif event_type == "decision_made":
        st.session_state.user_analytics['total_decisions'] += 1
    elif event_type == "premium_upgrade":
        st.session_state.user_analytics['premium_conversions'] += 1
    elif event_type == "scenario_selected":
        st.session_state.user_analytics['scenario_usage'][event_data.get('scenario', 'unknown')] += 1


def get_analytics_dashboard():
    """获取数据统计仪表盘"""
    if 'user_analytics' not in st.session_state:
        init_user_data()
    
    analytics = st.session_state.user_analytics
    
    # 计算关键指标
    total_users = analytics['total_users']
    total_decisions = analytics['total_decisions']
    premium_conversions = analytics['premium_conversions']
    conversion_rate = (premium_conversions / total_users * 100) if total_users > 0 else 0
    avg_decisions_per_user = (total_decisions / total_users) if total_users > 0 else 0
    
    # 按场景统计
    scenario_df = pd.DataFrame(
        list(analytics['scenario_usage'].items()),
        columns=['场景', '使用次数']
    ).sort_values('使用次数', ascending=False)
    
    # 收入统计
    revenue = analytics['revenue']
    
    return {
        "total_users": total_users,
        "total_decisions": total_decisions,
        "premium_conversions": premium_conversions,
        "conversion_rate": f"{conversion_rate:.2f}%",
        "avg_decisions_per_user": f"{avg_decisions_per_user:.2f}",
        "scenario_df": scenario_df,
        "revenue": revenue
    }


def show_admin_dashboard():
    """显示管理员数据统计仪表盘"""
    st.title("📊 数据统计仪表盘")
    
    # 获取统计数据
    analytics = get_analytics_dashboard()
    
    # 关键指标卡片
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("总用户数", analytics['total_users'])
    
    with col2:
        st.metric("总决策次数", analytics['total_decisions'])
    
    with col3:
        st.metric("付费转化数", analytics['premium_conversions'])
    
    with col4:
        st.metric("付费转化率", analytics['conversion_rate'])
    
    st.markdown("---")
    
    # 详细统计
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📈 收入统计")
        st.metric("总收入", f"¥{analytics['revenue']['total']}")
        st.metric("本月收入", f"¥{analytics['revenue']['monthly']}")
        st.metric("本年收入", f"¥{analytics['revenue']['yearly']}")
    
    with col2:
        st.subheader("🎯 场景使用统计")
        st.dataframe(analytics['scenario_df'], use_container_width=True, hide_index=True)
    
    st.markdown("---")
    
    st.subheader("📝 用户行为日志")
    
    # 获取最近的用户行为
    if 'user_analytics' in st.session_state:
        recent_actions = st.session_state.user_analytics['user_actions'][-10:]  # 最近10条
        
        for action in reversed(recent_actions):
            event_type = action['event_type']
            timestamp = action['timestamp']
            data = action['data']
            
            if event_type == "new_user":
                st.info(f"🆕 {timestamp} - 新用户注册：{data.get('user_id', 'Unknown')}")
            elif event_type == "decision_made":
                st.success(f"✅ {timestamp} - 完成决策分析：{data.get('scenario', 'Unknown')}")
            elif event_type == "premium_upgrade":
                st.success(f"💎 {timestamp} - 用户升级为专业版：{data.get('plan_type', 'Unknown')}")
            elif event_type == "scenario_selected":
                st.info(f"🎯 {timestamp} - 选择场景：{data.get('scenario', 'Unknown')}")


def show_premium_upgrade_modal():
    """显示付费升级弹窗"""
    st.markdown("---")
    st.markdown("## 💎 专业版功能")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("""
        ### ✅ 专业版功能

        - 🧠 AI深度智能分析
        - 📋 个性化行动清单
        - 📄 决策报告导出（PDF/Markdown）
        - 🔒 数据加密安全存储
        - 🎯 场景化专家建议
        - 💬 1对1专家咨询（每月1次）
        """)

    with col2:
        st.markdown("""
        ### 💰 定价方案

        **月付：** ¥29/月
        - 自动续费
        - 随时取消

        **年付：** ¥299/年
        - 节省 ¥49
        - 相当于 ¥25/月
        """)

    with col3:
        st.markdown("""
        ### 🚀 立即升级

        [点击立即升级](https://checkout.paddle.com/v2/checkout/start?product=12345&quantity=1)

        或联系客服：
        - 微信：decision_helper
        - 邮箱：support@example.com
        """)

    # 模拟付费成功
    if st.button("🎁 体验专业版功能（仅限演示）"):
        st.session_state.user_premium = True
        track_user_event("premium_upgrade", {"plan_type": "demo"})
        st.success("🎉 恭喜！您已激活专业版功能")
        st.rerun()


def calculate_analysis(scores_dict):
    """计算分析结果"""
    analysis = {}

    for option, scores in scores_dict.items():
        total_score = sum(scores.values())
        avg_score = total_score / len(scores)

        # 计算关键指标
        weighted_score = 0
        weighted_count = 0

        # 为不同场景设置不同的权重
        # 职业选择：收入和发展前景更重要
        if st.session_state.scenario == "职业选择":
            weighted_score += scores.get("💰 收入高低", 0) * 1.5
            weighted_score += scores.get("📈 发展前景", 0) * 1.5
            weighted_score += scores.get("⚖️ 工作生活平衡", 0) * 1.2
            weighted_score += scores.get("😀 工作开心度", 0) * 1.2
            weighted_count += 1.5 + 1.5 + 1.2 + 1.2
            
            # 其他维度
            for key, value in scores.items():
                if key not in ["💰 收入高低", "📈 发展前景", "⚖️ 工作生活平衡", "😀 工作开心度"]:
                    weighted_score += value
                    weighted_count += 1
        
        # 感情选择：彼此喜欢和价值观一致更重要
        elif st.session_state.scenario == "感情选择":
            weighted_score += scores.get("❤️ 彼此喜欢", 0) * 2
            weighted_score += scores.get("🤝 价值观一致", 0) * 1.8
            weighted_score += scores.get("💬 沟通顺畅", 0) * 1.5
            weighted_score += scores.get("😊 相处开心", 0) * 1.5
            weighted_count += 2 + 1.8 + 1.5 + 1.5
            
            # 其他维度
            for key, value in scores.items():
                if key not in ["❤️ 彼此喜欢", "🤝 价值观一致", "💬 沟通顺畅", "😊 相处开心"]:
                    weighted_score += value
                    weighted_count += 1
        
        # 其他场景使用平均分
        else:
            weighted_score = total_score
            weighted_count = len(scores)

        weighted_avg = weighted_score / weighted_count if weighted_count > 0 else 0

        analysis[option] = {
            "total_score": total_score,
            "avg_score": round(avg_score, 2),
            "weighted_avg": round(weighted_avg, 2),
            "details": scores
        }

    return analysis


def generate_ai_analysis(analysis, scenario, options, is_premium):
    """生成AI智能分析"""
    best_option = max(analysis.items(), key=lambda x: x[1]["weighted_avg"])
    best_data = best_option[1]

    # 场景化分析
    if scenario == "职业选择":
        ai_insights = generate_career_insights(best_option, best_data, analysis, is_premium)
    elif scenario == "感情选择":
        ai_insights = generate_relationship_insights(best_option, best_data, analysis, is_premium)
    elif scenario == "生活选择":
        ai_insights = generate_life_insights(best_option, best_data, analysis, is_premium)
    elif scenario == "消费选择":
        ai_insights = generate_shopping_insights(best_option, best_data, analysis, is_premium)
    else:
        ai_insights = generate_general_insights(best_option, best_data, analysis, is_premium)

    return ai_insights


def generate_career_insights(best_option, best_data, analysis, is_premium):
    """职业选择场景的AI分析"""
    insights = []

    # 收入vs发展分析
    income_score = best_data["details"].get("💰 收入高低", 0)
    growth_score = best_data["details"].get("📈 发展前景", 0)
    balance_score = best_data["details"].get("⚖️ 工作生活平衡", 0)
    happy_score = best_data["details"].get("😀 工作开心度", 0)

    if income_score >= 4 and growth_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】在收入和发展方面都表现优秀，是一个高质量的职业选择。"
        })
    elif income_score >= 4 and growth_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】收入高但发展潜力不足，建议考虑3-5年后的职业规划。"
        })
    elif income_score <= 2 and growth_score >= 4:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】属于'先苦后甜'的选择，建议做好1-2年的心理准备，关注长期积累。"
        })

    # 工作生活平衡分析
    if balance_score >= 4 and happy_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】工作生活平衡好，工作开心度高，适合长期发展。"
        })
    elif balance_score <= 2 and happy_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】工作生活平衡差，工作开心度低，可能会影响身心健康。"
        })

    # 付费功能：更详细的分析
    if is_premium:
        insights.append({
            "type": "🎯 专家建议",
            "content": f"基于职业发展数据分析，【{best_option[0]}】的综合推荐指数为{best_data['weighted_avg']/5*100:.0f}%，建议重点关注行业3年内的变革趋势。"
        })

        # 平衡性分析
        for option, data in analysis.items():
            if option == best_option[0]:
                continue
            if data["weighted_avg"] >= 4:
                insights.append({
                    "type": "🔄 替代方案",
                    "content": f"【{option[0]}】综合表现优秀，可以作为备选方案，建议对比企业文化、团队氛围等软性因素。"
                })

    return insights


def generate_relationship_insights(best_option, best_data, analysis, is_premium):
    """感情选择场景的AI分析"""
    insights = []

    # 核心指标分析
    love_score = best_data["details"].get("❤️ 彼此喜欢", 0)
    value_score = best_data["details"].get("🤝 价值观一致", 0)
    communication_score = best_data["details"].get("💬 沟通顺畅", 0)
    happy_score = best_data["details"].get("😊 相处开心", 0)

    if love_score >= 4 and value_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】在彼此喜欢和价值观一致方面都表现优秀，是一个高质量的感情选择。"
        })
    elif love_score >= 4 and value_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】彼此喜欢但价值观可能存在冲突，建议深入沟通未来规划、生活理念等关键问题。"
        })
    elif love_score <= 2 and value_score >= 4:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】价值观一致但感情基础不足，建议多花时间培养感情，了解彼此。"
        })

    # 沟通和开心度分析
    if communication_score >= 4 and happy_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】沟通顺畅，相处开心，感情基础良好。"
        })
    elif communication_score <= 2 and happy_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】沟通不顺畅，相处不开心，建议考虑是否适合。"
        })

    # 付费功能：更详细的分析
    if is_premium:
        insights.append({
            "type": "🎯 专家建议",
            "content": f"基于感情心理学分析，【{best_option[0]}】的感情健康指数为{best_data['weighted_avg']/5*100:.0f}%，建议定期安排深度沟通时间。"
        })

    return insights


def generate_life_insights(best_option, best_data, analysis, is_premium):
    """生活选择场景的AI分析"""
    insights = []

    # 核心指标分析
    comfort_score = best_data["details"].get("🏠 居住舒适度", 0)
    pressure_score = best_data["details"].get("💰 经济压力", 0)
    happiness_score = best_data["details"].get("😌 生活幸福感", 0)

    if comfort_score >= 4 and pressure_score <= 2:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】居住舒适度高，经济压力小，是一个高质量的生活选择。"
        })
    elif comfort_score >= 4 and pressure_score >= 4:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】居住舒适度高但经济压力大，建议做好财务规划，预留应急资金。"
        })
    elif comfort_score <= 2 and pressure_score <= 2:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】居住舒适度一般但经济压力小，适合当前经济状况紧张的情况，建议作为过渡选择。"
        })

    # 生活幸福感分析
    if happiness_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】生活幸福感高，能带来更好的生活体验。"
        })
    elif happiness_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】生活幸福感低，可能会影响身心健康。"
        })

    # 付费功能：更详细的分析
    if is_premium:
        insights.append({
            "type": "🎯 专家建议",
            "content": f"基于生活经济学分析，【{best_option[0]}】的生活质量指数为{best_data['weighted_avg']/5*100:.0f}%，建议做好长期生活规划。"
        })

    return insights


def generate_shopping_insights(best_option, best_data, analysis, is_premium):
    """消费选择场景的AI分析"""
    insights = []

    # 核心指标分析
    price_score = best_data["details"].get("💰 价格高低", 0)
    value_score = best_data["details"].get("⚖️ 性价比", 0)
    need_score = best_data["details"].get("🎯 功能需求", 0)
    use_score = best_data["details"].get("⚡ 使用频率", 0)

    if value_score >= 4 and need_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】性价比高，满足功能需求，是一个理性的消费选择。"
        })
    elif value_score <= 2 and need_score >= 4:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】满足功能需求但性价比低，建议对比其他品牌或型号。"
        })
    elif value_score >= 4 and need_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】性价比高但不满足功能需求，建议重新考虑是否真的需要。"
        })

    # 使用频率分析
    if use_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】使用频率高，物有所值。"
        })
    elif use_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】使用频率低，可能会造成浪费。"
        })

    # 付费功能：更详细的分析
    if is_premium:
        insights.append({
            "type": "🎯 专家建议",
            "content": f"基于消费心理学分析，【{best_option[0]}】的消费理性指数为{best_data['weighted_avg']/5*100:.0f}%，建议根据实际需求做出选择。"
        })

    return insights


def generate_general_insights(best_option, best_data, analysis, is_premium):
    """通用场景的AI分析"""
    insights = []

    # 综合评分分析
    if best_data["weighted_avg"] >= 4.5:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】的综合评分很高（{best_data['weighted_avg']}/5），各方面表现均衡优秀，值得重点考虑。"
        })
    elif best_data["weighted_avg"] >= 3.5:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】的综合评分良好（{best_data['weighted_avg']}/5），是一个稳妥的选择。"
        })

    # 核心维度分析
    like_score = best_data["details"].get("👍 喜欢程度", 0)
    regret_score = best_data["details"].get("🤔 后悔概率", 0)
    feeling_score = best_data["details"].get("😌 内心感受", 0)

    if like_score >= 4 and feeling_score >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】喜欢程度高，内心感受好，符合自己的真实需求。"
        })
    elif like_score <= 2 and feeling_score <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】喜欢程度低，内心感受差，建议重新考虑。"
        })

    # 风险提示
    if regret_score >= 4:
        insights.append({
            "type": "🚨 风险提示",
            "content": f"【{best_option[0]}】后悔概率高（评分{regret_score}/5），建议充分评估风险来源，做好风险预案。"
        })

    return insights


def generate_action_plan(best_option, best_data, scenario, is_premium):
    """生成行动清单"""
    action_plan = []

    # 通用行动清单
    action_plan.extend([
        "用3天时间记录自己对每个选项的真实感受（用日记记录）",
        "与1-2个信任的朋友或导师讨论这个选择，获取外部视角",
        "列出最坏情况：如果选择【{}】失败了，你的底线是什么？".format(best_option[0])
    ])

    # 场景化行动清单
    if scenario == "职业选择":
        action_plan.extend([
            "与行业内人士深入沟通，了解真实工作情况",
            "评估自己的核心竞争力，确认是否匹配",
            "准备Plan B：如果这个选择不顺利，你的替代方案是什么？"
        ])
        # 付费功能：更详细的行动清单
        if is_premium:
            action_plan.extend([
                "制定3个月职业发展计划，明确阶段性目标",
                "建立职业导师网络，每月至少与1位导师深度交流",
                "参加行业会议或专业培训，拓展人脉和视野"
            ])

    elif scenario == "感情选择":
        action_plan.extend([
            "安排一次深度沟通，与对方坦诚讨论未来规划",
            "列出这段关系的核心冲突点，评估是否可解决",
            "给自己设定一个决定期限，避免无限期纠结"
        ])
        # 付费功能：更详细的行动清单
        if is_premium:
            action_plan.extend([
                "安排每周一次的'关系复盘'时间，评估关系进展",
                "寻求专业情感咨询，学习更好的沟通技巧",
                "与信任的朋友或家人讨论，获取外部视角"
            ])

    elif scenario == "生活选择":
        action_plan.extend([
            "做详细的成本收益分析表（包括隐性成本）",
            "实地体验或模拟体验（如：实地看房、试驾等）",
            "评估这个选择对其他生活目标的影响"
        ])
        # 付费功能：更详细的行动清单
        if is_premium:
            action_plan.extend([
                "制定6个月实施计划，明确关键节点和检查点",
                "预留20%的预算作为风险缓冲",
                "与家人或重要他人沟通，获得他们的理解和支持"
            ])

    elif scenario == "消费选择":
        action_plan.extend([
            "列出这个产品的核心需求，确认是否真的需要",
            "对比3个以上的同类产品，选择性价比最高的",
            "评估使用频率，计算使用成本"
        ])
        # 付费功能：更详细的行动清单
        if is_premium:
            action_plan.extend([
                "制定年度消费预算，避免冲动消费",
                "建立'冷静期'机制，重要消费先放3天",
                "学习理财知识，提高消费决策能力"
            ])

    return action_plan


def main():
    """主程序"""

    # 初始化用户数据
    init_user_data()

    # 追踪新用户（仅第一次）
    if 'is_new_user' not in st.session_state:
        st.session_state.is_new_user = True
        track_user_event("new_user", {"user_id": get_user_id()})

    # 侧边栏：用户状态和功能导航
    with st.sidebar:
        st.title("🤔 AI决策小助手")

        # 管理员入口
        st.markdown("---")
        if st.button("📊 管理员仪表盘", type="secondary", use_container_width=True):
            st.session_state.show_admin = True
            st.rerun()

        st.markdown("---")

        # 用户状态显示
        is_premium = check_user_premium()
        usage_count = get_user_usage_count()

        if is_premium:
            st.success("✅ 专业版用户")
            st.markdown(f"已使用：{usage_count} 次")
        else:
            st.info("🆓 免费版用户")
            st.markdown(f"已使用：{usage_count} / {FREE_USER_LIMIT} 次")

            if usage_count >= FREE_USER_LIMIT:
                st.error("⚠️ 本月免费额度已用完")
                st.markdown("升级专业版可无限制使用")

        st.markdown("---")

        # 决策场景选择
        st.markdown("## 🎯 选择决策场景")

        # 使用卡片式布局展示场景
        cols = st.columns(2)
        for i, (scenario_name, scenario_info) in enumerate(DECISION_SCENARIOS.items()):
            with cols[i % 2]:
                if st.button(
                    f"{scenario_info['emoji']} {scenario_name}",
                    key=f"scenario_{scenario_name}",
                    use_container_width=True,
                    help=scenario_info['description']
                ):
                    st.session_state.scenario = scenario_name
                    track_user_event("scenario_selected", {"scenario": scenario_name})
                    st.rerun()

        # 显示当前场景
        if 'scenario' in st.session_state:
            current_scenario = st.session_state.scenario
            scenario_info = DECISION_SCENARIOS[current_scenario]
            st.markdown(f"\n**当前场景：** {scenario_info['emoji']} {current_scenario}")
            st.markdown(f"**说明：** {scenario_info['description']}")

        st.markdown("---")

        # 付费入口
        if not is_premium:
            if st.button("💎 升级专业版", type="primary", use_container_width=True):
                show_premium_upgrade_modal()
                return

        st.markdown("---")
        st.info("⚠️ 本工具仅为决策辅助，不能替代专业心理咨询")

    # 显示管理员仪表盘
    if st.session_state.get('show_admin', False):
        show_admin_dashboard()
        return

    # 检查是否选择了场景
    if 'scenario' not in st.session_state:
        st.title("🤔 AI决策小助手")
        st.markdown("## 帮你轻松做决定")
        st.markdown("---")
        st.markdown("### 🎯 请先选择一个决策场景")
        st.markdown("在左侧边栏选择一个场景，开始你的决策之旅！")
        return

    # 主界面
    current_scenario = st.session_state.scenario
    scenario_info = DECISION_SCENARIOS[current_scenario]

    st.markdown(f"""
    <div style="background-color:{scenario_info['color']}; padding:20px; border-radius:10px; margin-bottom:20px;">
        <h1 style="color:white; margin:0;">{scenario_info['emoji']} {current_scenario} - 决策分析</h1>
        <p style="color:white; margin:5px 0 0 0;">{scenario_info['description']}</p>
    </div>
    """, unsafe_allow_html=True)

    # 检查免费版使用限制
    if not is_premium and usage_count >= FREE_USER_LIMIT:
        st.error(f"免费版每月限 {FREE_USER_LIMIT} 次决策分析，请升级专业版使用更多功能")
        show_premium_upgrade_modal()
        return

    # 第一步：输入选项
    st.header("第一步：输入你的选项")
    st.markdown("请输入2-4个你正在纠结的选项")

    # 动态添加选项
    num_options = st.slider("选项数量", min_value=2, max_value=4, value=2, key="num_options")

    options = []
    for i in range(num_options):
        option = st.text_input(
            f"选项 {i+1}",
            placeholder=f"例如：留在一线城市 / 回老家发展",
            key=f"option_{i}"
        )
        if option:
            options.append(option)

    if not all(options):
        st.info("请填写所有选项后再继续")
        return

    st.divider()

    # 第二步：打分
    st.header("第二步：对每个选项打分")

    st.markdown("""
    <div style="background-color:#f8f9fa; padding:15px; border-radius:8px;">
    <h4>🎯 评分标准：</h4>
    <p><strong>😀 5分 = 非常好，非常满意</strong></p>
    <p><strong>😊 4分 = 比较好，比较满意</strong></p>
    <p><strong>😐 3分 = 一般，马马虎虎</strong></p>
    <p><strong>😞 2分 = 比较差，不太满意</strong></p>
    <p><strong>😫 1分 = 非常差，非常不满意</strong></p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("💡 提示：尽量根据你的真实感受打分，不要过度理性化。")

    # 获取当前场景的维度
    dimensions = DECISION_SCENARIOS[current_scenario]["dimensions"]

    scores_dict = {}

    for option in options:
        st.subheader(f"📍 {option}")
        scores = {}

        # 使用两列布局
        cols = st.columns(2)
        for i, dimension in enumerate(dimensions):
            with cols[i % 2]:
                # 使用更直观的评分方式
                score = st.slider(
                    f"{dimension}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"{option}_{dimension}",
                    help=f"对【{option}】在 '{dimension}' 方面打分",
                    format="{value}分"
                )
                scores[dimension] = score

        scores_dict[option] = scores
        st.divider()

    # 第三步：生成分析
    if st.button("🔍 生成决策分析", type="primary", use_container_width=True):
        # 增加使用次数
        increment_usage_count()
        
        # 追踪决策事件
        track_user_event("decision_made", {
            "scenario": current_scenario,
            "options": options,
            "is_premium": is_premium
        })

        with st.spinner("AI正在深度分析中..."):
            # 计算分析结果
            analysis = calculate_analysis(scores_dict)

            # 生成AI分析
            ai_insights = generate_ai_analysis(analysis, current_scenario, options, is_premium)

            # 生成行动清单
            best_option = max(analysis.items(), key=lambda x: x[1]["weighted_avg"])
            action_plan = generate_action_plan(best_option, best_option[1], current_scenario, is_premium)

            # 显示结果
            st.success("🎉 AI分析完成！")

            # 使用两列布局展示结果
            col1, col2 = st.columns([2, 1])

            # 左列：详细分析
            with col1:
                st.header("📊 详细分析")

                # 找出最高分选项
                st.subheader(f"🏆 综合评分最高：【{best_option[0]}】")
                st.metric("综合得分", f"{best_option[1]['weighted_avg']:.2f}/5")

                # AI智能分析
                st.subheader("🧠 AI智能分析")

                for insight in ai_insights:
                    if insight["type"] == "✅ 优势":
                        st.success(f"{insight['content']}")
                    elif insight["type"] == "⚠️ 风险":
                        st.warning(f"{insight['content']}")
                    elif insight["type"] == "🚨 风险提示":
                        st.error(f"{insight['content']}")
                    elif insight["type"] == "💡 建议":
                        st.info(f"{insight['content']}")
                    elif insight["type"] == "🔄 替代方案":
                        st.info(f"{insight['content']}")
                    elif insight["type"] == "🎯 专家建议":
                        st.info(f"{insight['content']}")

                # 检查是否为专业版，显示完整分析
                if not is_premium:
                    st.info("💡 专业版提供更详细的AI分析和个性化建议，升级即可解锁")

            # 右列：对比表格和行动清单
            with col2:
                st.subheader("选项对比表")

                df_data = []
                for option, data in analysis.items():
                    df_data.append({
                        "选项": option[:8] + "...",
                        "综合得分": f"{data['weighted_avg']:.2f}",
                        "总分": data["total_score"],
                        "均分": f"{data['avg_score']:.2f}"
                    })

                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # 行动清单
                st.divider()
                st.subheader("📝 行动清单")

                if is_premium:
                    for i, action in enumerate(action_plan, 1):
                        st.markdown(f"{i}. {action}")
                else:
                    # 免费版只显示前3条
                    for i, action in enumerate(action_plan[:3], 1):
                        st.markdown(f"{i}. {action}")

                    st.info(f"💡 专业版提供 {len(action_plan)} 条详细行动建议，升级即可查看全部")

            # 深度反思
            st.divider()
            st.header("🤔 深度反思")

            reflection_questions = [
                f"选择【{best_option[0]}】时，你的第一感受是什么？（焦虑/释然/兴奋/犹豫）",
                f"如果6个月后回看这个选择，你希望如何评价它？",
                f"这个选择中有哪些部分是可以调整的？有没有中间方案？",
                f"最坏情况下，你能否接受【{best_option[0]}】的失败？"
            ]

            cols = st.columns(2)
            for i, question in enumerate(reflection_questions):
                with cols[i % 2]:
                    st.markdown(f"**{i+1}.** {question}")

            st.info("💭 建议：给自己1-3天时间思考这些问题，不需要马上做出最终决定。")

            # 导出功能（仅专业版）
            st.divider()
            st.header("📥 导出决策报告")

            report_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scenario": current_scenario,
                "options": options,
                "scores": scores_dict,
                "analysis": analysis,
                "ai_insights": ai_insights,
                "action_plan": action_plan,
                "best_option": best_option[0]
            }

            col1, col2, col3 = st.columns(3)

            # JSON导出（所有用户可用）
            with col1:
                st.download_button(
                    label="📄 下载JSON报告",
                    data=json.dumps(report_data, ensure_ascii=False, indent=2),
                    file_name=f"decision_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

            # Markdown导出（仅专业版）
            with col2:
                if is_premium:
                    # 生成Markdown报告
                    markdown_report = f"""# AI决策分析报告

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**决策场景：** {current_scenario}
**综合推荐：** {best_option[0]}

---

## 📊 综合评分

| 选项 | 综合得分 | 总分 | 均分 |
|------|----------|------|------|
"""

                    for option, data in analysis.items():
                        markdown_report += f"| {option} | {data['weighted_avg']:.2f} | {data['total_score']} | {data['avg_score']:.2f} |\n"

                    markdown_report += "\n---\n\n## 🧠 AI智能分析\n\n"

                    for insight in ai_insights:
                        markdown_report += f"**{insight['type']}** {insight['content']}\n\n"

                    markdown_report += "\n---\n\n## 📝 行动清单\n\n"

                    for i, action in enumerate(action_plan, 1):
                        markdown_report += f"{i}. {action}\n"

                    st.download_button(
                        label="📝 下载Markdown报告",
                        data=markdown_report,
                        file_name=f"decision_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
                        mime="text/markdown"
                    )
                else:
                    st.markdown("📝 Markdown报告")
                    st.info("专业版功能，升级即可导出")

            # PDF导出（仅专业版）
            with col3:
                if is_premium:
                    st.markdown("📄 PDF报告")
                    st.info("准备中...")
                else:
                    st.markdown("📄 PDF报告")
                    st.info("专业版功能，升级即可导出")

            st.divider()
            st.markdown("""
            **重要提醒：**

            这个工具只是帮你梳理思路，最终的选择权在你。

            相信自己的判断，你比任何工具都更了解自己。

            ——

            如果这个工具对你有帮助，欢迎分享给有需要的朋友。
            """)


if __name__ == "__main__":
    main()
