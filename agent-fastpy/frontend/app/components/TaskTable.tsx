import React from "react";
import { Table, Button } from "antd";
import type { Task } from "../types/task";

interface TaskTableProps {
  tasks: Task[];
  loading: boolean;
  handleStart: (id: string) => void;
  handleStop: (id: string) => void;
  handleEdit: (task: Task) => void;
  handleDelete: (id: string) => void;
  onViewLog: (id: string) => void;
}

const TaskTable: React.FC<TaskTableProps> = ({
  tasks,
  loading,
  handleStart,
  handleStop,
  handleEdit,
  handleDelete,
  onViewLog,
}) => {
  const columns = [
    { title: "Name", dataIndex: "name", key: "name" },
    { title: "Status", dataIndex: "status", key: "status" },
    { title: "Created At", dataIndex: "created_at", key: "created_at" },
    { title: "Progress", dataIndex: "progress", key: "progress" },
    { title: "Agents", dataIndex: "agents", key: "agents" },
    {
      title: "Actions",
      key: "actions",
      render: (_: any, record: Task) => (
        <div className="flex space-x-2">
          {['created', 'stopped'].includes(record.status) && (
            <Button onClick={() => handleStart(record.id)}>Start</Button>
          )}
          {['running', 'error'].includes(record.status) && (
            <Button onClick={() => handleStop(record.id)}>Stop</Button>
          )}
          <Button onClick={() => handleEdit(record)}>Edit</Button>
          <Button danger onClick={() => handleDelete(record.id)}>Delete</Button>
          <Button type="link" onClick={() => onViewLog(record.id)}>查看日志</Button>
        </div>
      ),
    },
  ];

  return (
    <Table
      className="mt-4"
      dataSource={tasks}
      columns={columns}
      rowKey="id"
      loading={loading}
    />
  );
};

export default TaskTable;
