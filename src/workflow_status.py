"""
流程状态管理模块
管理 .workflow-status.json 文件
"""

import json
import os
from datetime import datetime
from typing import Optional, Literal
from dataclasses import dataclass, asdict

StatusType = Literal["planning", "developing", "testing", "reviewing", "done"]


@dataclass
class WorkflowStatus:
    """工作流状态"""
    current_feature: str
    status: StatusType
    prd_path: Optional[str] = None
    test_cases_path: Optional[str] = None
    test_report_path: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    STATUS_FILE = ".workflow-status.json"

    @classmethod
    def load(cls, project_root: str) -> Optional["WorkflowStatus"]:
        """从文件加载状态"""
        status_file = os.path.join(project_root, cls.STATUS_FILE)
        if not os.path.exists(status_file):
            return None

        with open(status_file, "r", encoding="utf-8") as f:
            data = json.load(f)

        return cls(
            current_feature=data.get("current_feature", ""),
            status=data.get("status", "planning"),
            prd_path=data.get("prd_path"),
            test_cases_path=data.get("test_cases_path"),
            test_report_path=data.get("test_report_path"),
            created_at=data.get("created_at"),
            updated_at=data.get("updated_at"),
        )

    def save(self, project_root: str) -> None:
        """保存状态到文件"""
        self.updated_at = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = self.updated_at

        status_file = os.path.join(project_root, self.STATUS_FILE)
        with open(status_file, "w", encoding="utf-8") as f:
            json.dump(asdict(self), f, indent=2, ensure_ascii=False)

    @classmethod
    def create(
        cls,
        project_root: str,
        feature_name: str,
        prd_path: str,
        test_cases_path: str,
    ) -> "WorkflowStatus":
        """创建新的工作流状态"""
        status = cls(
            current_feature=feature_name,
            status="planning",
            prd_path=prd_path,
            test_cases_path=test_cases_path,
        )
        status.save(project_root)
        return status

    def transition_to(self, new_status: StatusType, project_root: str) -> bool:
        """
        状态流转

        合法的流转路径:
        - planning -> developing
        - developing -> testing
        - testing -> reviewing (测试通过)
        - testing -> testing (Bug修复后重测)
        - reviewing -> done (验收通过)
        """
        valid_transitions = {
            "planning": ["developing"],
            "developing": ["testing"],
            "testing": ["reviewing", "testing"],  # testing->testing 用于Bug修复后重测
            "reviewing": ["done"],
            "done": ["planning"],  # 新需求
        }

        if new_status in valid_transitions.get(self.status, []):
            self.status = new_status
            self.save(project_root)
            return True
        return False

    def set_test_report(self, test_report_path: str, project_root: str) -> None:
        """设置测试报告路径"""
        self.test_report_path = test_report_path
        self.save(project_root)

    def is_empty_or_done(self) -> bool:
        """检查是否可以开始新需求"""
        return self.status == "done" or not self.current_feature

    def can_develop(self) -> bool:
        """检查是否可以开始开发"""
        return self.status == "developing"

    def can_fix_bugs(self) -> bool:
        """检查是否可以修复Bug"""
        return self.status == "testing" and self.test_report_path is not None

    def can_test(self) -> bool:
        """检查是否可以开始测试"""
        return self.status == "testing"

    def can_accept(self) -> bool:
        """检查是否可以验收"""
        return self.status == "reviewing"

    def get_status_display(self) -> str:
        """获取状态显示文本"""
        status_map = {
            "planning": "📋 需求规划中",
            "developing": "🔧 开发中",
            "testing": "🧪 测试中",
            "reviewing": "👀 待验收",
            "done": "✅ 已完成",
        }
        return status_map.get(self.status, self.status)
