pipeline {
    agent any

    stages {

        stage('Checkout') {
            steps {
                git branch: 'main',
                    url: 'https://github.com/tpgayathritp/Python-Payroll-App.git'
            }
        }

        stage('Install Dependencies') {
            steps {
                bat "python -m pip install --upgrade pip"
                bat "python -m pip install -r requirements.txt"
            }
        }

        stage('Run Payroll Script') {
            steps {
                bat "python Payroll.py"
            }
        }

        stage('Package Output') {
            steps {
                bat "powershell Compress-Archive -Path output -DestinationPath payroll_output.zip -Force"
            }
        }

        stage('Archive Artifacts') {
            steps {
                archiveArtifacts artifacts: 'payroll_output.zip', fingerprint: true
            }
        }

        stage('Archive Output') {
           steps {
                archiveArtifacts artifacts: '**/output/**', fingerprint: true
            }
        }
      stage('Archive Output') {
           steps {
                archiveArtifacts artifacts: '**/logs/**', fingerprint: true
            }
        }
      stage('Archive Output') {
           steps {
                archiveArtifacts artifacts: '**/payslips/**', fingerprint: true
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
