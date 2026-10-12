pipeline {
    agent any

    stages {
        stage('Install Dependencies') {
            steps {
                sh '''
                    python3 -m venv venv
                    venv/bin/pip install -r requirements.txt
                '''
            }
        }

        stage('Run Automated Tests') {
            steps {
                sh '''
                    mkdir -p reports
                    venv/bin/pytest -v \
                      --cov=app \
                      --cov-report=term-missing \
                      --junitxml=reports/test-results.xml tests/
                '''
            }
        }
    }

    post {
        always {
            echo 'Library Management Platform pipeline completed.'
        }
    }
}
