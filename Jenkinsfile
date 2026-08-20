pipeline {
    agent {
        kubernetes {
            label 'python311'
            defaultContainer 'python'
        }
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Install') {
            steps {
                sh '''
                    pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                sh '''
                    pytest
                '''
            }
        }

    }
}