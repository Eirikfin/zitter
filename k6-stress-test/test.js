import http from 'k6/http';
import { check, sleep } from 'k6';

export let options = {
  stages: [
    { duration: '30s', target: 200 },   // ramp up to 200 users (per server)
    { duration: '1m', target: 400 },    // ramp up to 400 users
    { duration: '1m', target: 600 },    // ramp up to 600 users (approx 200/server)
    { duration: '2m', target: 900 },    // ramp up to 900 users (approx 300/server)
    { duration: '2m', target: 1200 },   // ramp up to 1200 users (approx 400/server)
    { duration: '2m', target: 1500 },   // ramp up to 1500 users (approx 500/server)
    { duration: '1m', target: 0 },      // ramp down to 0
  ],
};

export default function () {
  let res = http.get('http://localhost:8080/tweets/all');
  check(res, { 'status is 200': (r) => r.status === 200 });
  sleep(0.1);
}