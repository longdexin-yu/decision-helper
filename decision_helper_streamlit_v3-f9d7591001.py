#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策辅助工具 - AI智能版本
用途：集成AI分析功能，提供个性化决策建议
"""

import streamlit as st
import json
from datetime import datetime
import pandas as pd


# 页面配置
st.set_page_config(
    page_title="AI决策辅助工具",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)


# 预设决策场景
DECISION_SCENARIOS = {
    "职业发展": {
        "dimensions": [
            "短期薪资涨幅（1年内收入增长）",
            "长期职业发展空间（3-5年晋升可能）",
            "工作生活平衡（加班频率、工作强度）",
            "技能提升价值（能学到什么）",
            "行业前景稳定性（行业风险指数）",
            "地理位置便利性（通勤、城市资源）",
            "团队氛围（同事关系、领导风格）",
            "成就感满足感（工作意义感）"
        ],
        "description": "适用于职业选择、换工作、创业等职业决策"
    },
    "感情关系": {
        "dimensions": [
            "当前幸福指数（相处时的快乐程度）",
            "未来规划一致性（生活目标是否一致）",
            "沟通质量（能否有效沟通解决问题）",
            "信任安全感（对彼此的信任度）",
            "家庭支持度（父母朋友的接受度）",
            "个人成长空间（在一起是否能变得更好）",
            "经济适配性（消费观、收入匹配度）",
            "妥协成本（需要放弃的东西）"
        ],
        "description": "适用于恋爱关系、婚姻选择、分手等感情决策"
    },
    "生活选择": {
        "dimensions": [
            "短期便利性（立刻能获得的好处）",
            "长期生活质量（3-5年的生活品质）",
            "经济负担（一次性成本+持续性成本）",
            "时间成本（需要投入的时间）",
            "心理舒适度（心理压力、焦虑程度）",
            "后悔风险（选择后后悔的可能性）",
            "灵活性调整度（改变选择的难易程度）",
            "自我一致性（是否符合个人价值观）"
        ],
        "description": "适用于买房、买车、搬家、留学等生活决策"
    },
    "自定义场景": {
        "dimensions": [
            "短期收益（立刻能获得的好处）",
            "长期价值（1-3年后的影响）",
            "执行难度（实现的难易程度）",
            "资源消耗（时间、金钱、精力投入）",
            "风险概率（失败的可能性）",
            "后悔成本（选择后后悔的程度）",
            "收益稳定性（收益的确定性）",
            "自我一致性（是否符合个人价值观）"
        ],
        "description": "适用于其他类型的决策，可自定义维度"
    }
}


def calculate_analysis(scores_dict):
    """计算分析结果"""
    analysis = {}

    for option, scores in scores_dict.items():
        total_score = sum(scores.values())
        avg_score = total_score / len(scores)

        # 计算关键指标
        short_term = scores.get("短期收益（立刻能获得的好处）", 0)
        if short_term == 0:
            short_term = scores.get("短期薪资涨幅（1年内收入增长）", 0)
        if short_term == 0:
            short_term = scores.get("当前幸福指数（相处时的快乐程度）", 0)

        long_term = scores.get("长期价值（1-3年后的影响）", 0)
        if long_term == 0:
            long_term = scores.get("长期职业发展空间（3-5年晋升可能）", 0)
        if long_term == 0:
            long_term = scores.get("长期生活质量（3-5年的生活品质）", 0)

        risk = scores.get("风险概率（失败的可能性）", 0)
        if risk == 0:
            risk = scores.get("后悔风险（选择后后悔的可能性）", 0)

        self_consistency = scores.get("自我一致性（是否符合个人价值观）", 0)
        if self_consistency == 0:
            self_consistency = scores.get("自我一致性（是否符合个人价值观）", 0)

        analysis[option] = {
            "total_score": total_score,
            "avg_score": round(avg_score, 2),
            "short_term": short_term,
            "long_term": long_term,
            "risk": risk,
            "self_consistency": self_consistency,
            "details": scores
        }

    return analysis


def generate_ai_analysis(analysis, scenario, options):
    """生成AI智能分析"""
    best_option = max(analysis.items(), key=lambda x: x[1]["total_score"])
    best_data = best_option[1]

    # 场景化分析
    if scenario == "职业发展":
        ai_insights = generate_career_insights(best_option, best_data, analysis)
    elif scenario == "感情关系":
        ai_insights = generate_relationship_insights(best_option, best_data, analysis)
    elif scenario == "生活选择":
        ai_insights = generate_life_insights(best_option, best_data, analysis)
    else:
        ai_insights = generate_general_insights(best_option, best_data, analysis)

    return ai_insights


def generate_career_insights(best_option, best_data, analysis):
    """职业发展场景的AI分析"""
    insights = []

    # 薪资vs成长分析
    if best_data["short_term"] >= 4 and best_data["long_term"] >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】在短期收益和长期发展方面都表现优秀，是一个高质量的职业选择。"
        })
    elif best_data["short_term"] >= 4 and best_data["long_term"] <= 2:
        insights.append({
            "type": "⚠️ 风险",
            "content": f"【{best_option[0]}】短期收益高但长期发展潜力不足，建议考虑3-5年后的职业规划。"
        })
    elif best_data["short_term"] <= 2 and best_data["long_term"] >= 4:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】属于'先苦后甜'的选择，建议做好1-2年的心理准备，关注长期积累。"
        })

    # 风险评估
    if best_data["risk"] >= 4:
        insights.append({
            "type": "🚨 风险提示",
            "content": f"这个选择存在较高风险（评分{best_data['risk']}/5），建议：1. 做好风险预案；2. 设置止损点；3. 寻求导师或行业前辈建议。"
        })

    # 平衡性分析
    for option, data in analysis.items():
        if option == best_option[0]:
            continue
        if data["short_term"] >= 4 and data["long_term"] >= 3:
            insights.append({
                "type": "🔄 替代方案",
                "content": f"【{option[0]}】在收益和成长方面表现均衡，可以作为备选方案，建议对比企业文化、团队氛围等软性因素。"
            })

    return insights


def generate_relationship_insights(best_option, best_data, analysis):
    """感情关系场景的AI分析"""
    insights = []

    # 幸福指数分析
    if best_data["short_term"] >= 4 and best_data["self_consistency"] >= 4:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】在当前幸福感和价值观一致性方面表现优秀，这段关系有坚实的基础。"
        })
    elif best_data["short_term"] >= 4 and best_data["self_consistency"] <= 2:
        insights.append({
            "type": "⚠️ 潜在问题",
            "content": f"【{best_option[0]}】当前相处快乐但价值观可能存在冲突，建议深入沟通未来规划、生活理念等关键问题。"
        })

    # 风险评估
    if best_data["risk"] >= 4:
        insights.append({
            "type": "🚨 风险提示",
            "content": f"这段关系存在较高风险（评分{best_data['risk']}/5），建议：1. 冷静分析风险来源；2. 寻求情感咨询师建议；3. 不要在情绪冲动时做决定。"
        })

    # 妥协成本分析
    for option, data in analysis.items():
        if option == best_option[0]:
            continue
        if data["details"].get("妥协成本（需要放弃的东西）", 0) <= 2:
            insights.append({
                "type": "🔄 替代方案",
                "content": f"【{option[0]}】的妥协成本较低，如果【{best_option[0]}】让你感到压力过大，可以考虑这个选项。"
            })

    return insights


def generate_life_insights(best_option, best_data, analysis):
    """生活选择场景的AI分析"""
    insights = []

    # 收益成本分析
    if best_data["short_term"] >= 4 and best_data["risk"] <= 2:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】短期收益高且风险可控，是一个稳妥的生活选择。"
        })
    elif best_data["long_term"] >= 4 and best_data["risk"] >= 4:
        insights.append({
            "type": "💡 建议",
            "content": f"【{best_option[0]}】属于高风险高收益的选择，建议：1. 评估自己的风险承受能力；2. 做好充分准备；3. 设置应急预案。"
        })

    # 经济负担分析
    economic_burden = best_data["details"].get("经济负担（一次性成本+持续性成本）", 0)
    if economic_burden >= 4:
        insights.append({
            "type": "💰 经济提醒",
            "content": f"这个选择的经济负担较重（评分{economic_burden}/5），建议：1. 做详细的财务规划；2. 考虑是否有更经济的替代方案；3. 预留6个月的应急资金。"
        })

    return insights


def generate_general_insights(best_option, best_data, analysis):
    """通用场景的AI分析"""
    insights = []

    # 综合评分分析
    if best_data["avg_score"] >= 4.5:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】的综合评分很高（{best_data['avg_score']}/5），各方面表现均衡优秀，值得重点考虑。"
        })
    elif best_data["avg_score"] >= 3.5 and best_data["risk"] <= 2:
        insights.append({
            "type": "✅ 优势",
            "content": f"【{best_option[0]}】的综合评分良好（{best_data['avg_score']}/5）且风险可控，是一个稳妥的选择。"
        })

    # 风险提示
    if best_data["risk"] >= 4:
        insights.append({
            "type": "🚨 风险提示",
            "content": f"这个选择存在较高风险（评分{best_data['risk']}/5），建议充分评估风险来源，做好风险预案。"
        })

    # 自我一致性分析
    if best_data["self_consistency"] <= 2:
        insights.append({
            "type": "⚠️ 潜在问题",
            "content": f"这个选择与你的价值观一致性较低，即使客观评分高，也可能让你在执行时感到不适，建议深入思考内心真实需求。"
        })

    return insights


def generate_action_plan(best_option, best_data, scenario):
    """生成行动清单"""
    action_plan = []

    # 通用行动清单
    action_plan.extend([
        "用3天时间记录自己对每个选项的真实感受（用日记记录）",
        "与1-2个信任的朋友或导师讨论这个选择，获取外部视角",
        "列出最坏情况：如果选择【{}】失败了，你的底线是什么？".format(best_option[0])
    ])

    # 场景化行动清单
    if scenario == "职业发展":
        action_plan.extend([
            "与行业内人士深入沟通，了解真实工作情况",
            "评估自己的核心竞争力，确认是否匹配",
            "准备Plan B：如果这个选择不顺利，你的替代方案是什么？"
        ])
    elif scenario == "感情关系":
        action_plan.extend([
            "安排一次深度沟通，与对方坦诚讨论未来规划",
            "列出这段关系的核心冲突点，评估是否可解决",
            "给自己设定一个决定期限，避免无限期纠结"
        ])
    elif scenario == "生活选择":
        action_plan.extend([
            "做详细的成本收益分析表（包括隐性成本）",
            "实地体验或模拟体验（如：实地看房、试驾等）",
            "评估这个选择对其他生活目标的影响"
        ])

    return action_plan


def main():
    """主程序"""

    # 侧边栏：决策场景选择
    with st.sidebar:
        st.title("🧠 AI决策辅助工具")
        st.markdown("---")

        # 决策场景选择
        scenario = st.selectbox(
            "选择决策场景",
            list(DECISION_SCENARIOS.keys()),
            help="不同的场景会使用不同的评估维度"
        )

        st.markdown(f"**说明：**{DECISION_SCENARIOS[scenario]['description']}")

        st.markdown("---")
        st.markdown("### 📊 决策分析框架")
        st.markdown("""
        1. **多维度评分** - 从不同角度评估选项
        2. **AI智能分析** - 基于数据生成个性化建议
        3. **风险评估** - 识别潜在风险和机会成本
        4. **行动清单** - 给出具体的后续步骤
        """)

        st.markdown("---")
        st.info("⚠️ 本工具仅为决策辅助，不能替代专业心理咨询")

    # 主界面
    st.title(f"🧠 {scenario} - 决策分析")

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
    st.header("第二步：对每个选项打分（1-5分）")

    st.markdown("""
    **评分标准：**
    - 1分 = 非常差/非常不符合
    - 2分 = 比较差/不太符合
    - 3分 = 一般/中等
    - 4分 = 比较好/比较符合
    - 5分 = 非常好/非常符合

    **提示：** 尽量根据你的真实感受打分，不要过度理性化。
    """)

    # 获取当前场景的维度
    dimensions = DECISION_SCENARIOS[scenario]["dimensions"]

    scores_dict = {}

    for option in options:
        st.subheader(f"📍 {option}")
        scores = {}

        # 使用两列布局
        cols = st.columns(2)
        for i, dimension in enumerate(dimensions):
            with cols[i % 2]:
                score = st.slider(
                    f"{dimension}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"{option}_{dimension}",
                    help=f"对【{option}】在 '{dimension}' 方面打分"
                )
                scores[dimension] = score

        scores_dict[option] = scores
        st.divider()

    # 第三步：生成分析
    if st.button("🔍 生成AI决策分析", type="primary", use_container_width=True):
        with st.spinner("AI正在深度分析中..."):
            # 计算分析结果
            analysis = calculate_analysis(scores_dict)

            # 生成AI分析
            ai_insights = generate_ai_analysis(analysis, scenario, options)

            # 生成行动清单
            best_option = max(analysis.items(), key=lambda x: x[1]["total_score"])
            action_plan = generate_action_plan(best_option, best_option[1], scenario)

            # 显示结果
            st.success("AI分析完成！")

            # 使用两列布局展示结果
            col1, col2 = st.columns([2, 1])

            # 左列：详细分析
            with col1:
                st.header("📊 详细分析")

                # 找出最高分选项
                st.subheader(f"🏆 综合评分最高：【{best_option[0]}】")
                st.metric("总分", best_option[1]["total_score"])
                st.metric("均分", best_option[1]["avg_score"])

                # AI智能分析
                st.subheader("🧠 AI智能分析")
                for insight in ai_insights:
                    if insight["type"] == "✅ 优势":
                        st.success(insight["content"])
                    elif insight["type"] == "⚠️ 潜在问题":
                        st.warning(insight["content"])
                    elif insight["type"] == "🚨 风险提示":
                        st.error(insight["content"])
                    elif insight["type"] == "💡 建议":
                        st.info(insight["content"])
                    elif insight["type"] == "🔄 替代方案":
                        st.info(insight["content"])
                    elif insight["type"] == "💰 经济提醒":
                        st.info(insight["content"])

            # 右列：对比表格和行动清单
            with col2:
                st.subheader("选项对比表")

                df_data = []
                for option, data in analysis.items():
                    df_data.append({
                        "选项": option[:8] + "...",
                        "总分": data["total_score"],
                        "均分": data["avg_score"],
                        "短期": data["short_term"],
                        "长期": data["long_term"],
                        "风险": data["risk"],
                        "自洽": data["self_consistency"]
                    })

                df = pd.DataFrame(df_data)
                st.dataframe(df, use_container_width=True, hide_index=True)

                # 行动清单
                st.divider()
                st.subheader("📝 行动清单")
                for i, action in enumerate(action_plan, 1):
                    st.markdown(f"{i}. {action}")

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

            # 下载报告
            st.divider()
            st.subheader("📥 导出决策报告")

            report_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "scenario": scenario,
                "options": options,
                "scores": scores_dict,
                "analysis": analysis,
                "ai_insights": ai_insights,
                "action_plan": action_plan,
                "best_option": best_option[0]
            }

            col1, col2, col3 = st.columns(3)

            with col1:
                st.download_button(
                    label="📄 下载JSON报告",
                    data=json.dumps(report_data, ensure_ascii=False, indent=2),
                    file_name=f"decision_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                    mime="application/json"
                )

            with col2:
                # 生成Markdown报告
                markdown_report = f"""# AI决策分析报告

**生成时间：** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**决策场景：** {scenario}
**综合推荐：** {best_option[0]}

---

## 📊 综合评分

| 选项 | 总分 | 均分 | 短期收益 | 长期价值 | 风险 | 自我一致性 |
|------|------|------|----------|----------|------|------------|
"""

                for option, data in analysis.items():
                    markdown_report += f"| {option} | {data['total_score']} | {data['avg_score']} | {data['short_term']} | {data['long_term']} | {data['risk']} | {data['self_consistency']} |\n"

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
