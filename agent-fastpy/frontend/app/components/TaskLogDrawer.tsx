import React from 'react';
import { Drawer, List, Typography } from 'antd';

interface TaskLogDrawerProps {
  visible: boolean;
  onClose: () => void;
  logs: string[];
}

const TaskLogDrawer: React.FC<TaskLogDrawerProps> = ({ visible, onClose, logs }) => {
  return (
    <Drawer
      title="任务日志"
      placement="right"
      onClose={onClose}
      visible={visible}
      width={500}
    >
      <List
        size="large"
        bordered
        dataSource={logs}
        renderItem={(log) => (
          <List.Item>
            <Typography.Text>{typeof log === 'string' ? log : JSON.stringify(log)}</Typography.Text>
          </List.Item>
        )}
      />
    </Drawer>
  );
};

export default TaskLogDrawer;
