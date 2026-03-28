#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
小程序 .wxapkg 文件反编译工具
集成 wxappUnpacker 实现自动反编译
"""

import os
import subprocess
import tempfile
import shutil
import zipfile
import tarfile
from pathlib import Path
from typing import Optional


class Unpacker:
    """小程序反编译器"""

    def __init__(self, wxapkg_path: str):
        """
        初始化反编译器

        Args:
            wxapkg_path: .wxapkg 文件路径
        """
        self.wxapkg_path = Path(wxapkg_path)
        self.temp_dir = None
        self.unpacker_script = None

    def is_wxapkg(self) -> bool:
        """检查是否为 .wxapkg 文件"""
        return self.wxapkg_path.suffix == '.wxapkg'

    def is_project_dir(self) -> bool:
        """检查是否为小程序项目目录"""
        # 检查是否有 app.json
        if not (self.wxapkg_path / 'app.json').exists():
            return False

        # 检查是否有 pages 目录或 utils 目录
        has_pages = (self.wxapkg_path / 'pages').exists()
        has_utils = (self.wxapkg_path / 'utils').exists()
        has_js_files = any(f.suffix == '.js' for f in self.wxapkg_path.rglob('*.js'))

        return has_pages or has_utils or has_js_files

    def get_unpacker_path(self) -> Optional[str]:
        """获取反编译工具路径"""
        # 1. 检查系统 PATH 中是否有 wuWxapkg.js
        if shutil.which('node'):
            try:
                # 检查全局安装的 wxappUnpacker
                result = subprocess.run(
                    ['npm', 'list', '-g', '--depth=0'],
                    capture_output=True,
                    text=True
                )
                if 'wxappUnpacker' in result.stdout:
                    return 'npm'
            except Exception:
                pass

        # 2. 检查本地目录中是否有 wxappUnpacker
        script_dir = Path(__file__).parent.parent.parent / 'tools' / 'wxappUnpacker'
        if script_dir.exists():
            return str(script_dir / 'wuWxapkg.js')

        # 3. 检查常见的本地安装位置
        local_paths = [
            Path.home() / 'wxappUnpacker',
            Path(__file__).parent.parent.parent / 'wxappUnpacker',
        ]
        for path in local_paths:
            if (path / 'wuWxapkg.js').exists():
                return str(path / 'wuWxapkg.js')

        return None

    def install_unpacker(self) -> bool:
        """安装 wxappUnpacker"""
        print("[*] 检测到 .wxapkg 文件，需要安装反编译工具...")

        # 检查是否已安装
        unpacker_path = self.get_unpacker_path()
        if unpacker_path:
            print(f"[+] 检测到反编译工具: {unpacker_path}")
            self.unpacker_script = unpacker_path
            return True

        # 尝试安装
        print("[*] 正在安装 wxappUnpacker...")

        # 方式 1: npm 全局安装
        if shutil.which('npm'):
            try:
                print("[*] 尝试通过 npm 安装...")
                subprocess.run(
                    ['npm', 'install', '-g', 'wxappUnpacker'],
                    check=True,
                    capture_output=True
                )
                print("[+] wxappUnpacker 安装成功")
                self.unpacker_script = 'npm'
                return True
            except subprocess.CalledProcessError as e:
                print(f"[-] npm 安装失败: {e}")

        # 方式 2: 克隆仓库
        try:
            print("[*] 尝试克隆 wxappUnpacker 仓库...")
            tools_dir = Path(__file__).parent.parent.parent / 'tools'
            tools_dir.mkdir(parents=True, exist_ok=True)

            clone_dir = tools_dir / 'wxappUnpacker'
            if clone_dir.exists():
                shutil.rmtree(clone_dir)

            subprocess.run(
                ['git', 'clone', 'https://github.com/xuedipapa/wxappUnpacker.git', str(clone_dir)],
                check=True
            )

            # 安装依赖
            subprocess.run(
                ['npm', 'install'],
                cwd=str(clone_dir),
                check=True,
                capture_output=True
            )

            print("[+] wxappUnpacker 安装成功")
            self.unpacker_script = str(clone_dir / 'wuWxapkg.js')
            return True

        except subprocess.CalledProcessError as e:
            print(f"[-] 克隆仓库失败: {e}")
        except Exception as e:
            print(f"[-] 安装失败: {e}")

        print("[-] 无法自动安装 wxappUnpacker")
        print("[!] 请手动安装:")
        print("    npm install -g wxappUnpacker")
        print("    # 或")
        print("    git clone https://github.com/xuedipapa/wxappUnpacker.git")
        print("    cd wxappUnpacker")
        print("    npm install")

        return False

    def unpack(self) -> Optional[str]:
        """
        反编译 .wxapkg 文件

        Returns:
            反编译后的项目目录路径
        """
        if not self.is_wxapkg():
            return str(self.wxapkg_path)

        # 安装反编译工具
        if not self.install_unpacker():
            return None

        # 创建临时目录
        self.temp_dir = Path(tempfile.mkdtemp(prefix='miniprogram_unpacked_'))
        print(f"[+] 创建临时目录: {self.temp_dir}")

        # 执行反编译
        print(f"[*] 正在反编译 {self.wxapkg_path.name}...")

        try:
            if self.unpacker_script == 'npm':
                # 使用 npm 安装的版本
                subprocess.run(
                    ['wuWxapkg.js', str(self.wxapkg_path), str(self.temp_dir)],
                    check=True
                )
            else:
                # 使用本地脚本
                subprocess.run(
                    ['node', self.unpacker_script, str(self.wxapkg_path), str(self.temp_dir)],
                    check=True
                )

            print(f"[+] 反编译成功，输出目录: {self.temp_dir}")

            # 验证反编译结果
            if not (self.temp_dir / 'app.json').exists():
                print("[-] 反编译结果验证失败，未找到 app.json")
                return None

            return str(self.temp_dir)

        except subprocess.CalledProcessError as e:
            print(f"[-] 反编译失败: {e}")
            return None
        except Exception as e:
            print(f"[-] 反编译失败: {e}")
            return None

    def cleanup(self):
        """清理临时目录"""
        if self.temp_dir and self.temp_dir.exists():
            print(f"[*] 清理临时目录: {self.temp_dir}")
            shutil.rmtree(self.temp_dir)
            print("[+] 清理完成")


def main():
    import argparse

    parser = argparse.ArgumentParser(description='小程序反编译工具')
    parser.add_argument('input_path', help='.wxapkg 文件或项目目录路径')
    parser.add_argument('-o', '--output', help='输出目录（仅用于 .wxapkg 文件）')
    args = parser.parse_args()

    input_path = Path(args.input_path)

    # 检查输入类型
    unpacker = Unpacker(args.input_path)

    if unpacker.is_wxapkg():
        print("[*] 检测到 .wxapkg 文件，开始反编译...")
        output_dir = unpacker.unpack()

        if output_dir:
            print(f"[+] 反编译成功: {output_dir}")

            # 如果指定了输出目录，复制文件
            if args.output:
                output_path = Path(args.output)
                if output_path.exists():
                    shutil.rmtree(output_path)
                shutil.copytree(output_dir, output_path)
                print(f"[+] 已复制到: {args.output}")

        else:
            print("[-] 反编译失败")
            exit(1)

    elif unpacker.is_project_dir():
        print("[*] 检测到小程序项目目录，无需反编译")
        print(f"[+] 项目目录: {args.input_path}")

    else:
        print("[-] 未知的文件类型，请确保是 .wxapkg 文件或小程序项目目录")
        exit(1)


if __name__ == '__main__':
    main()
