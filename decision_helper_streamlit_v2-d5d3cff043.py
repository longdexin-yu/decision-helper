#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策辅助工具 - Streamlit Web版本
用途：将命令行程序改造为Web应用，方便部署和分享
"""

import streamlit as st
import json
from datetime import datetime


# 页面配置
st.set_page_config(
    page_title="决策辅助工具",
    page_icon="🧭",
    layout="centered"
)

# 评估维度
DIMENSIONS = [
    "短期收益（立刻能获得的好处）",
    "长期价值（1-3年后的影响）",
    "情绪负担（选择过程中的压力程度）",
    "资源消耗（时间、金钱、精力投入）",
    "后悔风险（选择后后悔的可能性）",
    "自我一致性（是否符合个人价值观）"
]


def calculate_analysis(scores_dict):
    """计算分析结果"""
    analysis = {}

    for option, scores in scores_dict.items():
        total_score = sum(scores.values())
        avg_score = total_score / len(scores)

        emotional_burden = scores.get("情绪负担（选择过程中的压力程度）", 0)
        regret_risk = scores.get("后悔风险（选择后后悔的可能性）", 0)
        self_consistency = scores.get("自我一致性（是否符合个人价值观）", 0)

        analysis[option] = {
            "total_score": total_score,
            "avg_score": round(avg_score, 2),
            "emotional_burden": emotional_burden,
            "regret_risk": regret_risk,
            "self_consistency": self_consistency
        }

    return analysis


def main():
    """主程序"""

    # 标题和说明
    st.title("🧭 决策辅助工具")
    st.markdown("""
    这个工具不会替你做决定，但会帮你：
    - 拆解选项的利弊
    - 从多个维度对比
    - 找到更清晰的思考方向
    """)

    st.warning("⚠️ 重要提示：本工具仅为决策辅助，不能替代专业心理咨询或医疗诊断")

    st.divider()

    # 第一步：输入选项
    st.header("第一步：输入你的选项")

    # 动态添加选项
    num_options = st.slider("选项数量", min_value=2, max_value=4, value=2)

    options = []
    for i in range(num_options):
        option = st.text_input(f"选项 {i+1}", placeholder=f"例如：留在一线城市 / 回老家发展", key=f"option_{i}")
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
    - 3分 = 一般
    - 4分 = 比较好/比较符合
    - 5分 = 非常好/非常符合
    """)

    scores_dict = {}

    for option in options:
        st.subheader(f"📍 {option}")
        scores = {}

        cols = st.columns(2)
        for i, dimension in enumerate(DIMENSIONS):
            with cols[i % 2]:
                score = st.slider(
                    f"{dimension}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"{option}_{dimension}"
                )
                scores[dimension] = score

        scores_dict[option] = scores
        st.divider()

    # 第三步：生成分析
    if st.button("🔍 生成决策分析", type="primary"):
        with st.spinner("正在分析中..."):
            analysis = calculate_analysis(scores_dict)

            # 显示结果
            st.success("分析完成！")

            # 找出最高分选项
            best_option = max(analysis.items(), key=lambda x: x[1]["total_score"])
            st.header(f"🏆 综合评分最高：{best_option[0]}")
            st.metric("总分", best_option[1]["total_score"])
            st.metric("均分", best_option[1]["avg_score"])

            # 对比表格
            st.subheader("📊 选项对比表")

            import pandas as pd
            df_data = []
            for option, data in analysis.items():
                df_data.append({
                    "选项": option,
                    "总分": data["total_score"],
                    "均分": data["avg_score"],
                    "情绪负担": data["emotional_burden"],
                    "后悔风险": data["regret_risk"],
                    "自我一致性": data["self_consistency"]
                })

            df = pd.DataFrame(df_data)
            st.dataframe(df, use_container_width=True)

            # 情绪提示
            high_burden_options = [
                opt for opt, data in analysis.items()
                if data["emotional_burden"] >= 4
            ]

            if high_burden_options:
                st.warning(f"""
                💭 **温馨提示**
                你的一些选项（{', '.join(high_burden_options)}）表现出较高的情绪负担。
                这说明这个选择对你来说很重要，也可能让你感到压力。

                请记住：
                • 没有完美的选择，每个选择都有不确定性
                • 你可以随时调整方向，不必一次决定终身
                • 如果情绪让你无法思考，请给自己一点时间
                """)

            # 深度反思
            st.divider()
            st.subheader("🤔 深度反思")

            reflection_questions = [
                f"选择【{best_option[0]}】时，你的第一感受是什么？（焦虑/释然/兴奋/犹豫）",
                f"如果6个月后回看这个选择，你希望如何评价它？",
                f"这个选择中有哪些部分是可以调整的？有没有中间方案？"
            ]

            for i, question in enumerate(reflection_questions, 1):
                st.markdown(f"**{i}.** {question}")

            st.info("请思考以上问题（不需要马上回答，给自己一点时间）")

            # 下载报告
            st.divider()
            report_data = {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "options": options,
                "scores": scores_dict,
                "analysis": analysis,
                "best_option": best_option[0]
            }

            st.download_button(
                label="📥 下载决策报告",
                data=json.dumps(report_data, ensure_ascii=False, indent=2),
                file_name=f"decision_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )

            st.divider()
            st.markdown("""
            **重要提醒：**
            这个工具只是帮你梳理思路，最终的选择权在你。
            相信自己的判断，你比任何工具都更了解自己。
            """)


if __name__ == "__main__":
    main()
