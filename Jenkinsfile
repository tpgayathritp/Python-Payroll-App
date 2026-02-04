pipeline {
    agent any

    environment {
        PYTHON = "python"
    }

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tpgayathritp/Python-Payroll-App.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                sh "${PYTHON} -m pip install --upgrade pip"
                sh "${PYTHON} -m pip install -r requirements.txt"
            }
        }

        stage('Run Payroll Script') {
            steps {
                sh "${PYTHON} payroll/main.py"
            }
        }

        stage('Package Output') {
            steps {
                sh "zip -r payroll_output.zip output/"
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'payroll_output.zip', fingerprint: true
            }
        }
    }

    post {
        success {
            echo 'Payroll CI pipeline completed successfully'
        }
        failure {
            echo 'Payroll CI pipeline failed'
        }
    }
}
