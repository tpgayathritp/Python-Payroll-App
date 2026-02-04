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
      stage('Archive logs') {
           steps {
                archiveArtifacts artifacts: '**/logs/**', fingerprint: true
            }
        }
      stage('Archive payslips') {
           steps {
                archiveArtifacts artifacts: '**/payslips/**', fingerprint: true
            }
        }

     stage('Deploy to Local Folder') {
    steps {
        bat 'if not exist C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed mkdir C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed'
        bat 'xcopy /Y /E output C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed\\'
        bat 'xcopy /Y /E logs C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed\\'
        bat 'xcopy /Y /E payslips C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed\\'
        bat 'copy payroll_output.zip C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed\\'
         }
      }

     stage('Pipeline Summary') {
    steps {
        bat '''
        echo ============================================
        echo           PAYROLL PIPELINE SUMMARY
        echo ============================================
        echo.
        echo Payslips generated:
        dir /b payslips
        echo.
        echo Logs generated:
        dir /b logs
        echo.
        echo Payroll summary CSV files:
        dir /b output\\*.csv
        echo.
        echo Deployment folder:
        echo C:\\Users\\gayathri\\Desktop\\Python\\Payroll_app\\Deployed
        echo.
        echo Pipeline completed successfully.
        echo ============================================
        '''
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
