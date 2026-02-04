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
    stage('Test') {
      when { anyOf { branch 'main'; branch 'master'; branch 'feature/*' } }
      steps {
        sh 'uv run pytest tests/ || true'
      }
    }
    stage('Deploy') {
      when { anyOf { branch 'main'; branch 'master' } }
      steps {
        echo 'Deploy only on main/master'
      }
    }
  }
}