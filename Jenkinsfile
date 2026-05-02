pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Checking out source code...'
                checkout scm
            }
        }

        stage('Create Virtual Environment') {
            steps {
                echo 'Creating isolated Python virtual environment...'
                sh '''
                    rm -rf .jenkins-venv
                    python3 -m venv .jenkins-venv
                '''
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing dependencies inside virtual environment...'
                sh '''
                    . .jenkins-venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                echo 'Running unit tests...'
                sh '''
                    . .jenkins-venv/bin/activate
                    pytest tests/
                '''
            }
        }
    }

    post {
        success {
            echo 'Jenkins pipeline completed successfully.'
        }

        failure {
            echo 'Jenkins pipeline failed.'
        }
    }
}