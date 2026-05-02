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
                    python3 -m venv .jenkins-venv
                '''
            }
        }

        stage('Install CI Dependencies') {
            steps {
                sh '''
                    . .jenkins-venv/bin/activate
                    python -m pip install --upgrade pip
                    pip install -r requirements-ci.txt
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

    post {
        success {
            echo 'Jenkins CI pipeline completed successfully.'
        }

        failure {
            echo 'Jenkins CI pipeline failed.'
        }
    }
}