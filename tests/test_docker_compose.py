import os
import re

from django.conf import settings


class TestDockerfileCompose:

    def test_dockerfile_compose(self):
        try:
            with open(f'{os.path.join(settings.BASE_DIR, "docker-compose.txt")}', 'r') as f:
                docker_compose = f.read()
        except FileNotFoundError:
            assert False, 'Проверьте, что добавили файл docker-compose.txt'

        assert re.search(r'image:\s+postgres:latest', docker_compose), \
            'Проверьте, что добавили образ postgres:latest в файл docker_compose'
        assert re.search(r'build:\s+\.', docker_compose), \
            'Проверьте, что добавили сборку контейнера из Dockerfile.txt в файл docker_compose'
