import { Form, Input, Modal } from "antd";
import React from "react";

interface TaskModalProps {
  visible: boolean;
  onCancel: () => void;
  onOk: (arg0: any) => void;
  form: any;
}

const TaskModal: React.FC<TaskModalProps> = ({ visible, onCancel, onOk, form }) => {
  return (
      <Modal
        title="New Task"
        open={visible}
        onCancel={onCancel}
        onOk={() => form.submit()}
    >
      <Form form={form} layout="vertical" onFinish={(values) => onOk(values)}>
        <Form.Item
          name="name"
          label="Task Name"
          rules={[{ required: true, message: "Please enter task name" }]}
        >
          <Input />
        </Form.Item>
        <Form.Item name="description" label="Description">
          <Input.TextArea />
        </Form.Item>
      </Form>
    </Modal>
  );
};

export default TaskModal;
