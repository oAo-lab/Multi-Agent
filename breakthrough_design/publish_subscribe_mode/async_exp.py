import asyncio


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

    async def add_task(self, task):
        """异步添加任务"""
        self.tasks.append(task)
        await self.notify_subscribers()

    async def remove_task(self, task):
        """异步移除任务"""
        self.tasks.remove(task)
        await self.notify_subscribers()

    async def notify_subscribers(self):
        """异步通知所有订阅者"""
        for subscriber in self.subscribers:
            await subscriber.update_tasks(self.tasks)

    async def subscribe(self, subscriber):
        """异步添加订阅者"""
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            await subscriber.update_tasks(self.tasks)

    async def unsubscribe(self, subscriber):
        """异步移除订阅者"""
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)


class Subscriber:
    """订阅者类，表示宗门子弟"""

    def __init__(self, name):
        self.name = name
        self.tasks = []

    async def update_tasks(self, tasks):
        """异步更新任务列表"""
        self.tasks = tasks
        print(f"{self.name} received task update:")
        for task in self.tasks:
            print(task)
        print()

    async def take_task(self, task_name):
        """异步接受任务"""
        for task in self.tasks:
            if task.name == task_name and not task.is_taken:
                task.is_taken = True
                print(f"{self.name} has taken task: {task.name}")
                await self.notify_others(task_name)
                return
        print(f"{self.name} could not take task: {task_name}")

    async def notify_others(self, task_name):
        """异步通知其他订阅者任务已被接受"""
        for subscriber in self.publisher.subscribers:
            if subscriber != self:
                await subscriber.update_tasks(self.publisher.tasks)


# 测试代码
async def main():
    # 创建发布者
    publisher = Publisher()

    # 创建任务
    task1 = Task("Collect Herbs", "Collect 10 herbs from the forest.")
    task2 = Task("Hunt Monsters", "Defeat 5 monsters in the cave.")
    task3 = Task("Repair Bridge", "Repair the broken bridge in the village.")

    # 添加任务
    await publisher.add_task(task1)
    await publisher.add_task(task2)
    await publisher.add_task(task3)

    # 创建订阅者
    subscriber1 = Subscriber("Zhang San")
    subscriber2 = Subscriber("Li Si")
    subscriber3 = Subscriber("Wang Wu")

    # 设置发布者引用
    subscriber1.publisher = publisher
    subscriber2.publisher = publisher
    subscriber3.publisher = publisher

    # 订阅任务
    await publisher.subscribe(subscriber1)
    await publisher.subscribe(subscriber2)
    await publisher.subscribe(subscriber3)

    # 订阅者接受任务
    await subscriber1.take_task("Collect Herbs")
    await subscriber2.take_task("Hunt Monsters")
    await subscriber3.take_task("Repair Bridge")

    # 等待所有任务完成
    await asyncio.sleep(1)


if __name__ == "__main__":
    asyncio.run(main())
