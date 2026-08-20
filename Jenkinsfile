pipeline {
    agent {
        kubernetes {
            label 'python311'
            defaultContainer 'python'
        }
    }

    stages {

        stage('Environment') {
            steps {
                sh '''
                    echo "===== Environment ====="
                    whoami
                    pwd
                    python3 --version
                    pip3 --version
                '''
            }
        }

    }
}