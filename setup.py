from cx_Freeze import setup, Executable

includefiles = ['requirements.txt']

setup(name="NLP",
      version="0.1",
      description="",
      executables=[Executable("main.py")])
