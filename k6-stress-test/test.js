import http from 'k6/http';

const url = 'http://localhost:8080/tweets/all';

export let options = {
  scenarios: {
    scenario_one: {
      executor: 'constant-vus',
      exec: 'worker1',
      vus: 1000,
      duration: '1m',
    },
    scenario_two: {
      executor: 'constant-vus',
      exec: 'worker2',
      vus: 1000,
      duration: '1m',
    },
    scenario_tree: {
      executor: 'constant-vus',
      exec: 'worker3',
      vus: 1000,
      duration: '1m',
    },
    scenario_four: {
      executor: 'constant-vus',
      exec: 'worker4',
      vus: 1000,
      duration: '1m',
    },
  },
};

export function worker1() {
  http.get(url);
}

export function worker2() {
  http.get(url);
}
export function worker3() {
  http.get(url);
}
export function worker4() {
  http.get(url);
}