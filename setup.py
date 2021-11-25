from setuptools import find_packages, setup

__version__ = "0.0"
exec(open("./bot_scraper/version.py").read())

with open("README") as f:
    _LONG_DESCRIPTION = f.read()

setup(
    name="bot-scraper",
    packages=find_packages(),
    version=__version__,
    license="gpl-3.0",
    description="A telegram bot to stay tunded on real estate ads",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Roberto Bochet",
    author_email="robertobochet@gmail.com",
    url="https://github.com/RobertoBochet/bot-scraper",
    license_files=("LICENSE",),
    keywords=["bot", "telegrambot", "scraper", "telegram"],
    install_requires=[
        "python-telegram-bot ~= 13.8.1",
        "beautifulsoup4 ~= 4.10.0",
        "redis ~= 4.0.2",
        "requests ~= 2.26.0",
    ],
    extras_require={"dev": ["pre-commit ~= 2.15.0"]},
    classifiers=[
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.10",
)
