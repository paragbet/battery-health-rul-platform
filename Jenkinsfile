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
                    python -m pip install pytest pandas
                    python -m pip list
                '''
            }
        }

        stage('Run Unit Tests') {
            steps {
                sh '''
                    . .jenkins-venv/bin/activate
                    python -m pytest tests/
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