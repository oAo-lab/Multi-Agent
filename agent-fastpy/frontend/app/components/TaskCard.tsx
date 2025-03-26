import { toast } from 'react-toastify';
import type { Task } from '../services/api';

interface TaskCardProps {
  task: Task;
  onStart: (id: number) => void;
  onStop: (id: number) => void;
}

export default function TaskCard({ task, onStart, onStop }: TaskCardProps) {
  const statusColors = {
    pending: 'bg-gray-500',
    running: 'bg-primary',
    completed: 'bg-success',
    error: 'bg-error'
  };

  const handleAction = async (action: () => Promise<void>, successMsg: string) => {
    try {
      await action();
      toast.success(successMsg);
    } catch (error) {
      toast.error('操作失败，请重试');
    }
  };

  return (
    <div className="card bg-base-100 shadow-xl hover:shadow-2xl transition-shadow">
      <div className="card-body">
        <div className="flex justify-between items-start">
          <h3 className="card-title">{task.name}</h3>
          <div className={`badge ${statusColors[task.status]} text-white`}>
            {task.status}
          </div>
        </div>
        
        <div className="flex items-center gap-2">
          <progress 
            className="progress progress-primary w-full" 
            value={task.progress} 
            max="100"
          ></progress>
          <span className="text-sm">{task.progress}%</span>
        </div>
        
        <div className="flex justify-between text-sm">
          <div className="flex items-center gap-1">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 9a3 3 0 100-6 3 3 0 000 6zm-7 9a7 7 0 1114 0H3z" clipRule="evenodd" />
            </svg>
            {task.agents} Agents
          </div>
          <div className="text-gray-500">
            Created: {new Date(task.created_at).toLocaleDateString()}
          </div>
        </div>
        
        <div className="card-actions justify-end mt-2">
          {task.status === 'running' ? (
            <button 
              className="btn btn-sm btn-error"
              onClick={() => handleAction(async () => onStop(task.id), '任务已暂停')}
            >
              停止
            </button>
          ) : (
            <button 
              className="btn btn-sm btn-primary"
              onClick={() => handleAction(async () => onStart(task.id), '任务已启动')}
              disabled={task.status === 'completed'}
            >
              {task.status === 'pending' ? '启动' : '重试'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
