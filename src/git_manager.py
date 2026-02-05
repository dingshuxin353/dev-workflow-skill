"""
Git操作封装模块
"""

import subprocess
from typing import List, Optional, Tuple


class GitManager:
    """Git操作管理器"""

    def __init__(self, repo_path: str):
        self.repo_path = repo_path

    def _run_git(self, args: List[str], cwd: Optional[str] = None) -> Tuple[int, str, str]:
        """执行git命令"""
        cmd = ["git"] + args
        result = subprocess.run(
            cmd,
            cwd=cwd or self.repo_path,
            capture_output=True,
            text=True,
        )
        return result.returncode, result.stdout.strip(), result.stderr.strip()

    def get_current_branch(self) -> str:
        """获取当前分支名"""
        code, stdout, _ = self._run_git(["branch", "--show-current"])
        return stdout if code == 0 else ""

    def branch_exists(self, branch_name: str) -> bool:
        """检查分支是否存在"""
        code, _, _ = self._run_git(["rev-parse", "--verify", branch_name])
        return code == 0

    def create_branch(self, branch_name: str, from_branch: str = "main") -> bool:
        """创建新分支"""
        if self.branch_exists(branch_name):
            return True
        code, _, _ = self._run_git(["branch", branch_name, from_branch])
        return code == 0

    def checkout(self, branch_name: str) -> bool:
        """切换分支"""
        code, _, _ = self._run_git(["checkout", branch_name])
        return code == 0

    def add(self, files: List[str]) -> bool:
        """添加文件到暂存区"""
        code, _, _ = self._run_git(["add"] + files)
        return code == 0

    def commit(self, message: str) -> bool:
        """提交更改"""
        # 使用heredoc格式确保消息格式正确
        full_message = f"{message}\n\nCo-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>"
        code, _, _ = self._run_git(["commit", "-m", full_message])
        return code == 0

    def merge(self, source_branch: str, target_branch: str, message: Optional[str] = None) -> bool:
        """合并分支"""
        # 先切换到目标分支
        if not self.checkout(target_branch):
            return False

        # 执行合并
        args = ["merge", source_branch, "--no-ff"]
        if message:
            args.extend(["-m", message])

        code, _, _ = self._run_git(args)
        return code == 0

    def pull(self, branch: Optional[str] = None) -> bool:
        """拉取最新代码"""
        args = ["pull"]
        if branch:
            args.extend(["origin", branch])
        code, _, _ = self._run_git(args)
        return code == 0

    def push(self, branch: Optional[str] = None) -> bool:
        """推送代码"""
        args = ["push"]
        if branch:
            args.extend(["origin", branch])
        code, _, _ = self._run_git(args)
        return code == 0

    def stash(self) -> bool:
        """暂存当前更改"""
        code, _, _ = self._run_git(["stash"])
        return code == 0

    def stash_pop(self) -> bool:
        """恢复暂存的更改"""
        code, _, _ = self._run_git(["stash", "pop"])
        return code == 0

    def get_status(self) -> str:
        """获取git状态"""
        code, stdout, _ = self._run_git(["status", "--short"])
        return stdout if code == 0 else ""

    def has_uncommitted_changes(self) -> bool:
        """检查是否有未提交的更改"""
        return bool(self.get_status())

    def tag(self, tag_name: str, message: str) -> bool:
        """创建标签"""
        code, _, _ = self._run_git(["tag", "-a", tag_name, "-m", message])
        return code == 0

    def get_latest_tag(self) -> Optional[str]:
        """获取最新标签"""
        code, stdout, _ = self._run_git(["describe", "--tags", "--abbrev=0"])
        return stdout if code == 0 else None

    def get_commit_log(self, count: int = 10) -> List[str]:
        """获取提交日志"""
        code, stdout, _ = self._run_git([
            "log",
            f"-{count}",
            "--oneline",
            "--no-decorate"
        ])
        return stdout.split("\n") if code == 0 and stdout else []
