class Task:
    """任务类，表示一个宗门任务"""

    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.is_taken = False

    def __str__(self):
        return f"Task: {self.name}, Description: {self.description}, Taken: {self.is_taken}"


class Publisher:
    """发布者类，负责发布任务和通知订阅者"""

    def __init__(self):
        self.tasks = []
        self.subscribers = []

    def add_task(self, task):
        """添加任务"""
        self.tasks.append(task)
        self.notify_subscribers()

    def remove_task(self, task):
        """移除任务"""
        self.tasks.remove(task)
        self.notify_subscribers()

    def notify_subscribers(self):
        """通知所有订阅者"""
        for subscriber in self.subscribers:
            subscriber.update_tasks(self.tasks)

    def subscribe(self, subscriber):
        """添加订阅者"""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            subscriber.update_tasks(self.tasks)

    def unsubscribe(self, subscriber):
        """移除订阅者"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)


class Subscriber:
    """订阅者类，表示宗门子弟"""

    def __init__(self, name):
        self.name = name
        self.tasks = []

    def update_tasks(self, tasks):
        """更新任务列表"""
        self.tasks = tasks
        print(f"{self.name} received task update:")
        for task in self.tasks:
            print(task)
        print()

    def take_task(self, task_name):
        """接受任务"""
        for task in self.tasks:
            if task.name == task_name and not task.is_taken:
                task.is_taken = True
                print(f"{self.name} has taken task: {task.name}")
                return
        print(f"{self.name} could not take task: {task_name}")


# 测试代码
if __name__ == "__main__":
    # 创建发布者
    publisher = Publisher()

    # 创建任务
    task1 = Task("Collect Herbs", "Collect 10 herbs from the forest.")
    task2 = Task("Hunt Monsters", "Defeat 5 monsters in the cave.")
    task3 = Task("Repair Bridge", "Repair the broken bridge in the village.")

    # 添加任务
    publisher.add_task(task1)
    publisher.add_task(task2)
    publisher.add_task(task3)

    # 创建订阅者
    subscriber1 = Subscriber("Zhang San")
    subscriber2 = Subscriber("Li Si")
    subscriber3 = Subscriber("Wang Wu")

    # 订阅任务
    publisher.subscribe(subscriber1)
    publisher.subscribe(subscriber2)
    publisher.subscribe(subscriber3)

    # 订阅者接受任务
    subscriber1.take_task("Collect Herbs")
    subscriber2.take_task("Hunt Monsters")
    subscriber3.take_task("Repair Bridge")

    # 更新任务状态
    publisher.notify_subscribers()
