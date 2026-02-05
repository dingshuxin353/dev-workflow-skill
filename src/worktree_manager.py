"""
Git Worktree 管理模块
"""

import os
import subprocess
from typing import List, Optional, Dict
from dataclasses import dataclass


@dataclass
class WorktreeInfo:
    """Worktree信息"""
    path: str
    branch: str
    commit: str


class WorktreeManager:
    """Git Worktree 管理器"""

    # 默认的worktree配置
    DEFAULT_WORKTREES = {
        "develop": "-develop",
        "test": "-test",
    }

    def __init__(self, main_repo_path: str):
        """
        初始化Worktree管理器

        Args:
            main_repo_path: 主仓库路径（main分支所在目录）
        """
        self.main_repo_path = os.path.abspath(main_repo_path)
        self.project_name = os.path.basename(self.main_repo_path)
        self.parent_dir = os.path.dirname(self.main_repo_path)

    def _run_git(self, args: List[str], cwd: Optional[str] = None) -> tuple:
        """执行git命令"""
        cmd = ["git"] + args
        result = subprocess.run(
            cmd,
            cwd=cwd or self.main_repo_path,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def get_worktree_path(self, branch: str) -> str:
        """获取指定分支的worktree路径"""
        if branch == "main" or branch == "master":
            return self.main_repo_path

        suffix = self.DEFAULT_WORKTREES.get(branch, f"-{branch}")
        return os.path.join(self.parent_dir, f"{self.project_name}{suffix}")

    def list_worktrees(self) -> List[WorktreeInfo]:
        """列出所有worktree"""
        code, stdout, _ = self._run_git(["worktree", "list", "--porcelain"])
        if code != 0:
            return []

        worktrees = []
        current = {}

        for line in stdout.split("\n"):
            if line.startswith("worktree "):
                current["path"] = line[9:]
            elif line.startswith("HEAD "):
                current["commit"] = line[5:]
            elif line.startswith("branch "):
                current["branch"] = line[7:].replace("refs/heads/", "")
            elif line == "" and current:
                if "path" in current:
                    worktrees.append(WorktreeInfo(
                        path=current.get("path", ""),
                        branch=current.get("branch", ""),
                        commit=current.get("commit", ""),
                    ))
                current = {}

        # 处理最后一个
        if current and "path" in current:
            worktrees.append(WorktreeInfo(
                path=current.get("path", ""),
                branch=current.get("branch", ""),
                commit=current.get("commit", ""),
            ))

        return worktrees

    def worktree_exists(self, branch: str) -> bool:
        """检查指定分支的worktree是否存在"""
        worktrees = self.list_worktrees()
        target_path = self.get_worktree_path(branch)
        return any(wt.path == target_path for wt in worktrees)

    def create_worktree(self, branch: str) -> bool:
        """
        创建worktree

        Args:
            branch: 分支名称

        Returns:
            是否成功
        """
        if self.worktree_exists(branch):
            return True

        worktree_path = self.get_worktree_path(branch)

        # 确保分支存在
        code, _, _ = self._run_git(["rev-parse", "--verify", branch])
        if code != 0:
            # 分支不存在，从main创建
            self._run_git(["branch", branch, "main"])

        # 创建worktree
        code, _, stderr = self._run_git(["worktree", "add", worktree_path, branch])
        if code != 0:
            print(f"创建worktree失败: {stderr}")
            return False

        return True

    def remove_worktree(self, branch: str) -> bool:
        """删除worktree"""
        worktree_path = self.get_worktree_path(branch)
        code, _, _ = self._run_git(["worktree", "remove", worktree_path])
        return code == 0

    def setup_all_worktrees(self) -> Dict[str, bool]:
        """
        设置所有默认的worktree

        Returns:
            各分支的创建结果
        """
        results = {}
        for branch in self.DEFAULT_WORKTREES.keys():
            results[branch] = self.create_worktree(branch)
        return results

    def get_current_worktree(self) -> Optional[str]:
        """获取当前所在的worktree分支"""
        cwd = os.getcwd()
        worktrees = self.list_worktrees()

        for wt in worktrees:
            if os.path.abspath(cwd).startswith(os.path.abspath(wt.path)):
                return wt.branch

        return None

    def sync_branch(self, source: str, target: str) -> bool:
        """
        同步分支（将source合并到target）

        Args:
            source: 源分支
            target: 目标分支

        Returns:
            是否成功
        """
        target_path = self.get_worktree_path(target)

        # 在目标worktree中执行合并
        code, _, stderr = self._run_git(
            ["merge", source, "--no-ff", "-m", f"Merge {source} into {target}"],
            cwd=target_path
        )

        if code != 0:
            print(f"合并失败: {stderr}")
            return False

        return True

    def get_status_summary(self) -> str:
        """获取所有worktree的状态摘要"""
        worktrees = self.list_worktrees()
        lines = ["Git Worktree 状态:", ""]

        for wt in worktrees:
            branch_name = wt.branch or "(detached)"
            lines.append(f"  {branch_name}: {wt.path}")
            lines.append(f"    commit: {wt.commit[:8]}")

        return "\n".join(lines)
