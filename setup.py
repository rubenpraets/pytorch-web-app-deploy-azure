from setuptools import setup

setup(
    name='flask_pytorch_web_app',
    packages=['flask_pytorch_web_app'],
    include_package_data=True,
    install_requires=[
        'click==7.1.1',
        'dominate==2.5.1',
        'Flask==1.1.2',
        'Flask-Bootstrap==3.3.7.1',
        'Flask-Uploads',
        'future==0.18.2',
        'itsdangerous==1.1.0',
        'Jinja2==2.11.2',
        'MarkupSafe==1.1.1',
        'numpy==1.18.3',
        'Pillow==7.1.1',
        'torch==1.5.0',
        'torchvision==0.6.0',
        'visitor==0.1.3',
        'Werkzeug==0.15.6',
        'python-dotenv',
        'gunicorn'
    ],
)
