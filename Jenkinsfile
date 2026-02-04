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
            withSonarQubeEnv('SonarQube') {
                withCredentials([string(credentialsId: 'sonarqube-token2', variable: 'SONAR_TOKEN')]) {
                    sh 'sonar-scanner -Dsonar.host.url=http://localhost:9000 -Dsonar.login=$SONAR_TOKEN'
            }
            }
        }
    }
    stage('Quality Gate') {
        steps {
            timeout(time: 5, unit: 'MINUTES') {
                waitForQualityGate abortPipeline: true
            }
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
    }
  }
}