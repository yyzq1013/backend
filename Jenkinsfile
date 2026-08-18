pipeline {
    agent any

    stages {

        stage('Environment') {
            steps {
                sh '''
                    echo "===== Environment ====="
                    whoami
                    pwd
                    python3 --version || true
                    pip3 --version || true
                    git --version || true
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    echo "===== Test ====="
                    pytest
                '''
            }
        }

        stage('Build') {
            steps {
                echo 'Building backend...'
            }
        }

    }
}