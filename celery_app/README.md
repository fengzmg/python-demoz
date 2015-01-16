    cd ..
    celery -A celery_app worker -l info

This will start the celery task queue workers