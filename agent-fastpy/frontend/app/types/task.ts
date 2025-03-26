export interface Task {
  id: string;
  name: string;
  status: 'created' | 'pending' | 'running' | 'completed' | 'error' | 'stopped';
  description?: string;
  created_at?: string;
  progress?: string;
  agents?: string;
}
