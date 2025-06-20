import subprocess
import pkg_resources
import logicNLP_words_only


# def install_requirements():
#     requirements_file = 'requirements.txt'  # Path to your requirements file
#
#     # Execute the pip command to install requirements
#     subprocess.check_call(['pip', 'install', '-r', requirements_file])
#
#
# def check_requirement_installed(package):
#     print('check_requirement_installed')
#     try:
#         pkg_resources.get_distribution(package)
#         return True
#     except pkg_resources.DistributionNotFound:
#         return False
#
#
# if not check_requirement_installed('nltk'):
#     install_requirements()
#

from ReworkedUI import window


if __name__ == "__main__":
    try:
        window.mainloop()
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running the Python file: {e}")