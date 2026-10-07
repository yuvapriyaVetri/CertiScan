pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                echo 'Checking out CertiScan source code...'
                checkout scm
            }
        }

        stage('Install Dependencies') {
            steps {
                echo 'Installing Python dependencies...'
                sh '''
                    python3 -m venv venv
                    ./venv/bin/pip install --upgrade pip
                    ./venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Test') {
            steps {
                echo 'Testing CertiScan application...'
                sh '''
                    ./venv/bin/python -c "import app; print('CertiScan application import test PASSED')"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying CertiScan...'
                sh '''
                    sudo -n /usr/bin/systemctl restart certiscan
                    sleep 3
                    sudo -n /usr/bin/systemctl status certiscan
                '''
            }
        }
    }

    post {
        success {
            echo 'CertiScan CI/CD pipeline completed successfully!'
        }

        failure {
            echo 'CertiScan CI/CD pipeline failed.'
        }
    }
}
