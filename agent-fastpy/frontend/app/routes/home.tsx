import {
  createTask,
  deleteTask,
  editTask,
  fetchTaskHistory,
  fetchTasks,
  startTask,
  stopTask
} from "../services/api";

import {
  Button,
  ConfigProvider,
  Form,
  Input,
  Layout,
  message,
  theme
} from "antd";
import React, { useEffect, useState } from "react";
import Header from "../components/Header";
import TaskLogDrawer from "../components/TaskLogDrawer";
import TaskModal from "../components/TaskModal";
import TaskTable from "../components/TaskTable";
import type { Task } from "../types/task";

const TaskManagement: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState(false);
  const [modalVisible, setModalVisible] = useState(false);
  const [form] = Form.useForm();
  const [editingTask, setEditingTask] = useState<Task | null>(null);

  useEffect(() => {
    const interval = setInterval(loadTasks, 5000); // Poll every 5 seconds
    loadTasks(); // Initial load

    return () => clearInterval(interval); // Cleanup on unmount
  }, []);

  const [query, setQuery] = useState("");
  const [isDarkMode, setIsDarkMode] = useState(false);

  const toggleTheme = () => {
    setIsDarkMode((prev) => !prev);
  };

  const loadTasks = async () => {
    setLoading(true);
    try {
      const data: Task[] = await fetchTasks();
      setTasks(data.filter(task =>
        task.name.includes(query) || (task.description && task.description.includes(query))
      ));
    } catch (error) {
      message.error("Failed to fetch tasks");
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = (values: { name: string; description?: string; template?: string }) => {
    const payload = {
      name: values.name,
      template: values.template || "",
      description: values.description || "",
    };

    if (editingTask) {
      editTask(editingTask.id, payload)
        .then(() => {
          message.success("Task updated successfully");
        })
        .catch((error) => {
          console.error("Error during task edit:", error);
          message.error("Failed to update task");
        })
        .finally(() => {
          setModalVisible(false);
          loadTasks();
        });
    } else {
      createTask(payload)
        .then(() => {
          message.success("Task created successfully");
        })
        .catch((error) => {
          console.error("Error during task creation:", error);
          message.error("Failed to create task");
        })
        .finally(() => {
          setModalVisible(false);
          loadTasks();
        });
    }
  };

  const handleDelete = async (id: string) => {
    try {
      await deleteTask(id);
      message.success("Task deleted successfully");
      loadTasks();
    } catch (error) {
      message.error("Failed to delete task");
    }
  };

  const handleStart = async (id: string) => {
    try {
      await startTask(id);
      message.success("Task started");
      loadTasks();
    } catch (error) {
      message.error("Failed to start task");
    }
  };

  const handleStop = async (id: string) => {
    try {
      await stopTask(id);
      message.success("Task stopped");
      loadTasks();
    } catch (error) {
      message.error("Failed to stop task");
    }
  };

  const handleViewLog = (id: string) => {
    setLogDrawerVisible(true);
    setSelectedTaskId(id);
  };

  const [logDrawerVisible, setLogDrawerVisible] = useState(false);
  const [selectedTaskId, setSelectedTaskId] = useState<string | null>(null);
  const [logs, setLogs] = useState<string[]>([]);

  useEffect(() => {
    if (logDrawerVisible && selectedTaskId) {
      fetchTaskHistory(selectedTaskId).then(setLogs);
    }
  }, [logDrawerVisible, selectedTaskId]);

  return (
    <ConfigProvider
      theme={{
        algorithm: isDarkMode ? theme.darkAlgorithm : theme.defaultAlgorithm,
      }}
    >
      <Layout style={{ minHeight: "100vh" }}>
        <Header isDarkMode={isDarkMode} toggleTheme={toggleTheme} />
        <Layout.Content
          style={{
            padding: "24px",
            maxWidth: "1200px",
            margin: "0 auto",
            background: isDarkMode ? "#1f1f1f" : "#f9f9f9",
            color: isDarkMode ? "#e0e0e0" : "#333",
          }}
        >
          <div className="flex flex-col items-center justify-center space-y-4">
            <div className="flex space-x-4">
              <Input
                placeholder="Search tasks by name or description"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                style={{ width: 200 }}
              />
              <Button type="primary" onClick={loadTasks}>
                Search
              </Button>
            </div>
            <Button
              type="primary"
              onClick={() => {
                setEditingTask(null);
                form.resetFields();
                setModalVisible(true);
              }}
            >
              New Task
            </Button>
          </div>
          <TaskTable
            tasks={tasks}
            loading={loading}
            handleStart={handleStart}
            handleStop={handleStop}
            handleEdit={(task) => {
              setEditingTask(task);
              form.setFieldsValue(task);
              setModalVisible(true);
            }}
            handleDelete={handleDelete}
            onViewLog={handleViewLog}
          />
          <TaskLogDrawer
            visible={logDrawerVisible}
            onClose={() => setLogDrawerVisible(false)}
            logs={logs}
          />
          <TaskModal
            visible={modalVisible}
            onCancel={() => setModalVisible(false)}
            onOk={(v) => handleCreate(v)}
            form={form}
          />
        </Layout.Content>
        <Layout.Footer
          style={{
            textAlign: "center",
            background: isDarkMode ? "#1f1f1f" : "#f0f2f5",
            color: isDarkMode ? "#e0e0e0" : "#333",
          }}
        >
          Task Management System ©2025 Created by Your Company
        </Layout.Footer>
      </Layout>
    </ConfigProvider>
  );
};

export default TaskManagement;
