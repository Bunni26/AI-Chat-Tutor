from setuptools import setup, find_packages

setup(
    name="ai-chat-tutor",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "Flask-SQLAlchemy==3.1.1",
        "SQLAlchemy==2.0.20",
        "PyMySQL==1.1.0",
        "python-dotenv==1.0.0",
        "requests==2.31.0",
        "Werkzeug==2.3.7",
        "PyJWT==2.8.0",
        "Flask-JWT-Extended==4.5.2",
        "pydantic==1.10.13"
    ],
)
