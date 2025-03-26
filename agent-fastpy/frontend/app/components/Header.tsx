import React from "react";
import { Layout, Avatar, Switch } from "antd";
import { UserOutlined } from "@ant-design/icons";

interface HeaderProps {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

const Header: React.FC<HeaderProps> = ({ isDarkMode, toggleTheme }) => {
  return (
    <Layout.Header
      style={{
        background: isDarkMode ? "#141414" : "#1890ff",
        color: "#fff",
        display: "flex",
        alignItems: "center",
        justifyContent: "space-between",
        padding: "0 32px",
      }}
    >
      <span style={{ fontSize: "1.25rem", fontWeight: "bold", color: "#fff" }}>
        Task Management System
      </span>
      <div style={{ display: "flex", alignItems: "center", gap: "16px" }}>
        <Switch
          checkedChildren="Dark"
          unCheckedChildren="Light"
          checked={isDarkMode}
          onChange={toggleTheme}
        />
        <Avatar icon={<UserOutlined />} />
      </div>
    </Layout.Header>
  );
};

export default Header;
