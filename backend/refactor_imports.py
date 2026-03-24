import os
import re

def refactor_imports(directory):
    replacements = {
        r'from app\.models import': r'from app.domain.entities import',
        r'from app\.models\.': r'from app.domain.entities.',
        r'from app\.schemas import': r'from app.api.schemas import',
        r'from app\.schemas\.': r'from app.api.schemas.',
        r'from app\.services import': r'from app.application.services import',
        r'from app\.services\.': r'from app.application.services.',
        r'from app\.db\.database import': r'from app.infrastructure.database.database import',
        r'from app\.db\.seeds import': r'from app.infrastructure.database.seeds import',
        r'from app\.routes import': r'from app.api.v1.endpoints import',
        r'from app\.routes\.': r'from app.api.v1.endpoints.',
        r'from app\.repositories import': r'from app.infrastructure.repositories import',
        r'from app\.repositories\.': r'from app.infrastructure.repositories.',
        r'from app\.controllers\.auth_controller import AuthController': r'from app.application.services.auth_service import AuthService',
        r'from app\.api\.v1\.endpoints\.chatbot\.schemas import': r'from app.api.schemas.chatbot import',
        r'from app\.presentation\.chatbot\.schemas import': r'from app.api.schemas.chatbot import',
        r'backend\.app': r'app',
        r'AuthController': r'AuthService',
    }

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()

                new_content = content
                for pattern, replacement in replacements.items():
                    new_content = re.sub(pattern, replacement, new_content)

                if new_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"Refactorizado: {file_path}")

if __name__ == "__main__":
    refactor_imports('app')
