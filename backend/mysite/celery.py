# [추가] Django 프로젝트에서 Celery 앱을 등록하는 파일

import os

from celery import Celery

# [추가] Django settings 모듈 지정
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# [추가] Celery 앱 생성
app = Celery("mysite")

# [추가] Django settings.py의 CELERY_ 접두사 설정값 자동 로드
app.config_from_object("django.conf:settings", namespace="CELERY")

# [추가] INSTALLED_APPS 안의 tasks.py 자동 탐색
app.autodiscover_tasks()
