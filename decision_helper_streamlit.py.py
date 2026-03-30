#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
决策辅助工具 - 轻量级版本
用途：帮助用户梳理决策选项，通过结构化分析获得更清晰的视角
注意：本工具仅为决策辅助，不能替代专业心理咨询
"""

import json
from typing import List, Dict


class DecisionHelper:
    """决策辅助类"""

    def __init__(self):
        # 预设的评估维度
        self.default_dimensions = [
            "短期收益（立刻能获得的好处）",
            "长期价值（1-3年后的影响）",
            "情绪负担（选择过程中的压力程度）",
            "资源消耗（时间、金钱、精力投入）",
            "后悔风险（选择后后悔的可能性）",
            "自我一致性（是否符合个人价值观）"
        ]

    def welcome(self):
        """欢迎界面"""
        print("=" * 60)
        print("决策辅助工具 - 帮你梳理混乱的选择")
        print("=" * 60)
        print("\n这个工具不会替你做决定，但会帮你：")
        print("1. 拆解选项的利弊")
        print("2. 从多个维度对比")
        print("3. 找到更清晰的思考方向")
        print("\n重要提示：如果你感到情绪极度低落或无法处理，请寻求专业帮助。")
        print("-" * 60)
        print()

    def get_options(self) -> List[str]:
        """获取用户输入的选项"""
        options = []
        print("请输入你正在纠结的选项（2-4个）：")

        while True:
            option = input(f"选项 {len(options) + 1}（输入 'done' 完成输入）: ").strip()
            if option.lower() == 'done':
                if len(options) < 2:
                    print("至少需要2个选项才能进行对比，请继续输入。")
                    continue
                break
            if not option:
                print("选项不能为空，请重新输入。")
                continue
            if len(options) >= 4:
                print("最多支持4个选项对比，已达到上限。")
                break
            options.append(option)

        return options

    def get_scores(self, options: List[str]) -> Dict[str, Dict[str, int]]:
        """获取用户对各选项在各维度的打分"""
        scores = {}

        print("\n现在请对每个选项在以下维度进行打分（1-5分）：")
        print("1分 = 非常差/非常不符合")
        print("5分 = 非常好/非常符合")
        print("-" * 60)

        for option in options:
            print(f"\n【{option}】")
            option_scores = {}

            for dimension in self.default_dimensions:
                while True:
                    try:
                        score = input(f"  {dimension} (1-5): ").strip()
                        score = int(score)
                        if 1 <= score <= 5:
                            option_scores[dimension] = score
                            break
                        else:
                            print("  请输入1-5之间的整数。")
                    except ValueError:
                        print("  请输入有效的数字（1-5）。")

            scores[option] = option_scores

        return scores

    def calculate_total(self, scores: Dict[str, Dict[str, int]]) -> Dict[str, Dict]:
        """计算各选项的总分和加权分析"""
        analysis = {}

        for option, option_scores in scores.items():
            total_score = sum(option_scores.values())
            avg_score = total_score / len(option_scores)

            # 关注关键维度
            emotional_burden = option_scores.get("情绪负担（选择过程中的压力程度）", 0)
            regret_risk = option_scores.get("后悔风险（选择后后悔的可能性）", 0)
            self_consistency = option_scores.get("自我一致性（是否符合个人价值观）", 0)

            analysis[option] = {
                "total_score": total_score,
                "avg_score": round(avg_score, 2),
                "emotional_burden": emotional_burden,
                "regret_risk": regret_risk,
                "self_consistency": self_consistency,
                "details": option_scores
            }

        return analysis

    def display_comparison(self, options: List[str], analysis: Dict[str, Dict]):
        """展示对比结果"""
        print("\n" + "=" * 60)
        print("决策对比分析")
        print("=" * 60)

        # 打印表格
        print("\n{:<20} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
            "选项", "总分", "均分", "情绪负担", "后悔风险", "自我一致性"
        ))
        print("-" * 60)

        for option in options:
            data = analysis[option]
            print("{:<20} {:<8} {:<8} {:<8} {:<8} {:<8}".format(
                option,
                data["total_score"],
                data["avg_score"],
                data["emotional_burden"],
                data["regret_risk"],
                data["self_consistency"]
            ))

        # 找出最高分选项
        best_option = max(analysis.items(), key=lambda x: x[1]["total_score"])
        print(f"\n📊 综合评分最高: {best_option[0]}")
        print(f"   总分: {best_option[1]['total_score']}, 均分: {best_option[1]['avg_score']}")

    def provide_reflection(self, best_option: str, analysis: Dict[str, Dict]):
        """提供反思问题"""
        print("\n" + "=" * 60)
        print("深度反思")
        print("=" * 60)

        data = analysis[best_option]
        reflection_questions = [
            f"选择【{best_option}】时，你的第一感受是什么？（焦虑/释然/兴奋/犹豫）",
            f"如果6个月后回看这个选择，你希望如何评价它？",
            f"这个选择中有哪些部分是可以调整的？有没有中间方案？"
        ]

        print("\n请思考以下问题（不需要马上回答，给自己一点时间）：\n")
        for i, question in enumerate(reflection_questions, 1):
            print(f"{i}. {question}")

    def check_emotional_alert(self, analysis: Dict[str, Dict]):
        """检查是否需要情绪安全提示"""
        print("\n" + "=" * 60)

        # 检查是否有高情绪负担的选项
        high_burden_options = [
            opt for opt, data in analysis.items()
            if data["emotional_burden"] >= 4
        ]

        if high_burden_options:
            print("⚠️  温馨提示")
            print("-" * 60)
            print("你的一些选项表现出较高的情绪负担。这说明这个选择对你来说很重要，")
            print("也可能让你感到压力。")
            print("\n请记住：")
            print("• 没有完美的选择，每个选择都有不确定性")
            print("• 你可以随时调整方向，不必一次决定终身")
            print("• 如果情绪让你无法思考，请给自己一点时间")

    def generate_report(self, options: List[str], scores: Dict[str, Dict[str, int]], analysis: Dict[str, Dict]):
        """生成决策报告"""
        report = {
            "timestamp": "2026-03-23",
            "options": options,
            "scores": scores,
            "analysis": analysis
        }

        filename = f"decision_report_{len(options)}options.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f"\n✓ 决策报告已保存到: {filename}")

    def run(self):
        """运行主程序"""
        self.welcome()

        # 获取选项
        options = self.get_options()

        # 获取打分
        scores = self.get_scores(options)

        # 计算分析
        analysis = self.calculate_total(scores)

        # 展示对比
        self.display_comparison(options, analysis)

        # 情绪提示
        self.check_emotional_alert(analysis)

        # 反思引导
        best_option = max(analysis.items(), key=lambda x: x[1]["total_score"])[0]
        self.provide_reflection(best_option, analysis)

        # 生成报告
        self.generate_report(options, scores, analysis)

        print("\n" + "=" * 60)
        print("分析完成！")
        print("=" * 60)
        print("\n记住：这个工具只是帮你梳理思路，最终的选择权在你。")
        print("相信自己的判断，你比任何工具都更了解自己。")
        print()


if __name__ == "__main__":
    helper = DecisionHelper()
    helper.run()
