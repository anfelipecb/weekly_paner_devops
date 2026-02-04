import http from 'k6/http';
import { check, sleep } from 'k6';
import { htmlReport } from 'https://raw.githubusercontent.com/benc-uk/k6-reporter/main/dist/bundle.js';

const BASE_URL = __ENV.BASE_URL || 'http://localhost:5001';

export const options = {
  vus: 10,              // 10 virtual users
  duration: '30s',      // run for 30 seconds
  thresholds: {
    'http_req_failed': ['rate<0.01'],     // error rate < 1%
    'http_req_duration': ['p(95)<500'],   // 95% of requests < 500ms
  },
};

export default function () {
  // Health check
  const healthRes = http.get(`${BASE_URL}/health`);
  check(healthRes, { 'health status 200': (r) => r.status === 200 });

  // GET tasks (main API)
  const tasksRes = http.get(`${BASE_URL}/api/tasks`);
  check(tasksRes, { 'tasks status 200': (r) => r.status === 200 });

  sleep(0.5);
}

export function handleSummary(data) {
    return {
      'report/load-report.html': htmlReport(data),
      stdout: textSummary(data, { indent: ' ', enableColors: true }),
    };
  }
  
import { textSummary } from 'https://jslib.k6.io/k6-summary/0.0.1/index.js';