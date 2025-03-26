export interface Task {
  id: string;
  name: string;
  status: 'PENDING' | 'RUNNING' | 'SUCCESS' | 'FAILED';
  startTime: string;
  logs: string;
}
