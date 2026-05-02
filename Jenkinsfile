pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                sh '''
                    rm -rf .jenkins-venv
                    python3.11 -m venv .jenkins-venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                sh '''
                    . .jenkins-venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . .jenkins-venv/bin/activate
                    pytest tests/
                '''
            }
        }
    }
}