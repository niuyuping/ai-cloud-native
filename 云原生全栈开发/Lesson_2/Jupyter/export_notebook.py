#!/usr/bin/env python3
"""
导出 Jupyter Notebook 并修复路径
让导出的 HTML 文件中的资源路径正确
"""
import subprocess
import sys
import re
from pathlib import Path


def export_and_fix_paths(notebook_path, output_dir=None):
    """导出 notebook 并修复路径"""
    notebook = Path(notebook_path).resolve()
    if not notebook.exists():
        print(f"错误：找不到文件 {notebook_path}")
        return
    
    # 确定输出目录：默认导出到当前工作目录
    if output_dir:
        output_dir = Path(output_dir).resolve()
    else:
        output_dir = Path.cwd()
    
    output_dir.mkdir(parents=True, exist_ok=True)
    output_file = output_dir / f"{notebook.stem}.html"
    
    # 导出 HTML（不隐藏代码，保持原始路径）
    print(f"正在导出 {notebook.name}...")
    result = subprocess.run([
        sys.executable, "-m", "nbconvert",
        "--to", "html",
        "--no-input",  # 隐藏代码
        str(notebook),
        "--output-dir", str(output_dir),
        "--output", notebook.stem
    ], capture_output=True, text=True, check=False)
    
    if result.returncode != 0:
        print(f"导出失败：{result.stderr}")
        return
    
    # 读取导出的 HTML
    print("正在修复路径...")
    with open(output_file, 'r', encoding='utf-8') as f:
        html_content = f.read()
    
    # 修复路径：
    # ../Assets/ -> ./Assets/
    # ../../References/ -> ../References/
    html_content = re.sub(
        r'src="\.\./Assets/',
        r'src="./Assets/',
        html_content
    )
    html_content = re.sub(
        r'href="\.\./\.\./References/',
        r'href="../References/',
        html_content
    )
    
    # 写回文件
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    
    print(f"✓ 导出完成：{output_file}")
    print("✓ 路径已修复，可在浏览器中正常显示")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法: python export_notebook.py <notebook_path> [output_dir]")
        print("      如果不指定 output_dir，将导出到当前目录")
        sys.exit(1)
    
    input_notebook_path = sys.argv[1]
    input_output_dir = sys.argv[2] if len(sys.argv) > 2 else None
    
    if input_output_dir:
        print(f"输出目录：{Path(input_output_dir).resolve()}")
    else:
        print(f"输出目录（默认）：{Path.cwd()}")
    
    export_and_fix_paths(input_notebook_path, input_output_dir)

