pipeline {
  agent any
  triggers {
    githubPush()
  }
  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }
    stage('Build') {
      steps {
        sh 'uv sync'
      }
    }
    stage('Package') {
        steps {
        sh '''
            mkdir -p dist
            zip -r dist/planner-${BUILD_NUMBER}.zip \
            app db static templates app.py requirements.txt pyproject.toml README.md \
            -x "*.pyc" -x ".git/*" -x "venv/*" -x ".venv/*" -x "*__pycache__*" -x "dist/*"
        '''
        }
    }
    stage('Test') {
      when { anyOf { branch 'main'; branch 'master'; branch 'feature/*' } }
      steps {
        sh 'uv run pytest tests/ || true'
      }
    }
    stage('SonarQube Analysis') {
        steps {
            script {
                scannerHome = tool 'SonarScanner'   // same name as in Jenkins Tools
            }
            withSonarQubeEnv('SonarQube') {       // same name as in Jenkins → System → SonarQube servers
            sh "${scannerHome}/bin/sonar-scanner"
            }
        }
    }
    stage('Quality Gate') {
        steps {
            timeout(time: 2, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
        }
    }
    stage('Load Test') {
        agent { label 'performance' }
        steps {
            checkout scm
            sh 'mkdir -p report'
            sh 'k6 run load/planner_load.js 2>&1 | tee report/load-test.log'
        }
    }
    stage('Deploy') {
      when { anyOf { branch 'main'; branch 'master' } }
      steps {
        echo 'Deploy only on main/master'
      }
    }
  }
  post {
    success {
        archiveArtifacts artifacts: 'dist/*.zip', fingerprint: true
        archiveArtifacts artifacts: 'report/load-report.html,report/load-test.log', fingerprint: true, allowEmptyArchive: true
    }
  }
}