from setuptools import setup, find_packages

setup(
    name='xiyan_mcp_server',  # 包的名字
    version='0.1.5.dev0',  # 版本号
    packages=find_packages(),  # 自动找到项目中的包
    install_requires=[  # 必要的包依赖
        # 'numpy',  # 示例：若有依赖包，将其列在此
'mcp',
'mysql-connector-python>=9.1.0',
'sqlalchemy',
'llama_index',
'yaml',
'pandas',
'pymysql'
    ],
    author='Bruce Luo',  # 作者
    author_email='godot.lzl@alibaba-inc.com',  # 作者邮箱
    description='A MCP server of natural language interface to Database',  # 简短描述
    long_description=open('README.md').read(),  # 从 README 文件读取详细描述
    long_description_content_type='text/markdown',  # 描述内容类型
    url='https://github.com/XGenerationLab/xiyan_mcp_server',  # 项目主页
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.11',  # 支持的 Python 版本
)
