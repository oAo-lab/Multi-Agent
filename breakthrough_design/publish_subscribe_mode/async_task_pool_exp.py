import asyncio
from abc import ABC, abstractmethod
from collections import defaultdict


# 定义任务类
class Task:
    def __init__(self, name, description, steps):
        self.name = name
        self.description = description
        self.steps = steps  # 任务步骤列表
        self.current_step = 0  # 当前步骤索引
        self.is_taken = False

    def __str__(self):
        return f"Task: {self.name}, Description: {self.description}, Steps: {len(self.steps)}, Current Step: {self.current_step}"

    def next_step(self):
        """进入下一个步骤"""
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            return True
        return False

    def is_completed(self):
        """检查任务是否完成"""
        return self.current_step == len(self.steps) - 1


# 定义任务步骤类
class TaskStep:
    def __init__(self, description, required_level):
        self.description = description
        self.required_level = required_level  # 完成该步骤所需的最低等级

    def __str__(self):
        return f"Step: {self.description}, Required Level: {self.required_level}"


# 定义发布者类
class Publisher:
    def __init__(self):
        self.tasks = []
        self.subscribers = []

    async def add_task(self, task):
        self.tasks.append(task)
        await self.notify_subscribers()

    async def remove_task(self, task):
        self.tasks.remove(task)
        await self.notify_subscribers()

    async def notify_subscribers(self):
        for subscriber in self.subscribers:
            await subscriber.update_tasks(self.tasks)

    async def subscribe(self, subscriber):
        if subscriber not in self.subscribers:
            self.subscribers.append(subscriber)
            await subscriber.update_tasks(self.tasks)

    async def unsubscribe(self, subscriber):
        if subscriber in self.subscribers:
            self.subscribers.remove(subscriber)


# 定义订阅者抽象类
class Subscriber(ABC):
    def __init__(self, name, level):
        self.name = name
        self.level = level  # 角色等级
        self.tasks = []

    @abstractmethod
    async def update_tasks(self, tasks):
        pass

    @abstractmethod
    async def take_task(self, task_name):
        pass


# 定义具体订阅者类
class Disciple(Subscriber):
    async def update_tasks(self, tasks):
        self.tasks = [task for task in tasks if not task.is_taken]
        print(f"{self.name} (Level {self.level}) received task update:")
        for task in self.tasks:
            print(task)
        print()

    async def take_task(self, task_name):
        for task in self.tasks:
            if task.name == task_name and not task.is_taken:
                task.is_taken = True
                print(f"{self.name} has taken task: {task.name}")
                await self.perform_task_step(task)
                return
        print(f"{self.name} could not take task: {task_name}")

    async def perform_task_step(self, task: Task):
        """执行任务的当前步骤"""
        if task.current_step < len(task.steps):
            step = task.steps[task.current_step]
            if self.level >= step.required_level:
                print(f"{self.name} is performing step: {step}")
                # 模拟步骤执行时间
                await asyncio.sleep(1)
                if task.next_step():
                    await self.notify_others(task)
                else:
                    print(
                        f"{self.name} has completed task: {task.name} {task.description}"
                    )
                    await self.notify_others(task)
            else:
                print(
                    f"{self.name} cannot perform step: {step} (required level: {step.required_level})"
                )
        else:
            print(f"{self.name} has completed all steps of task: {task.name}")

    async def notify_others(self, task):
        for subscriber in self.publisher.subscribers:
            if subscriber != self:
                await subscriber.update_tasks(self.publisher.tasks)


# 定义建造者抽象类
class Builder(ABC):
    @abstractmethod
    def create_disciple(self, name, level):
        pass


# 定义具体建造者类
class DiscipleBuilder(Builder):
    def create_disciple(self, name, level):
        return Disciple(name, level)


# 定义弟子池类
class DisciplePool:
    def __init__(self):
        self.pool = defaultdict(list)  # 使用字典存储不同等级的弟子

    def add_disciple(self, disciple):
        self.pool[disciple.level].append(disciple)

    def get_disciple(self, level):
        if self.pool[level]:
            return self.pool[level].pop()  # 返回并移除一个弟子
        return None

    def has_disciple(self, level):
        return bool(self.pool[level])

    def __str__(self):
        return "\n".join(
            [
                f"Level {level}: {len(disciples)} disciples"
                for level, disciples in self.pool.items()
            ]
        )


# 测试代码
async def main():
    # 创建发布者
    publisher = Publisher()

    # 创建任务步骤
    step1 = TaskStep("Defeat the boss", required_level=4)
    step2 = TaskStep("Collect the loot", required_level=3)
    step3 = TaskStep("Report the gains", required_level=2)

    # 创建任务
    task1 = Task(
        "Kill Boss and Report",
        "Defeat the boss, collect the loot, and report the gains.",
        [step1, step2, step3],
    )

    task2 = Task(
        "采集千年雪人参",
        "",
        [
            TaskStep("击败守护药材的魔兽", required_level=4),
            TaskStep("搜寻药材出现的领域", required_level=3),
            TaskStep("收集药材并分析收益", required_level=2),
        ],
    )

    # 添加任务
    await publisher.add_task(task1)
    await publisher.add_task(task2)

    # 创建建造者
    builder = DiscipleBuilder()

    # 创建弟子池
    disciple_pool = DisciplePool()

    # 动态创建弟子并加入弟子池
    for i in range(5):
        disciple_pool.add_disciple(
            builder.create_disciple(f"True Disciple {i + 1}", level=4)
        )
    for i in range(10):
        disciple_pool.add_disciple(
            builder.create_disciple(f"Inner Disciple {i + 1}", level=3)
        )
    for i in range(15):
        disciple_pool.add_disciple(
            builder.create_disciple(f"Outer Disciple {i + 1}", level=2)
        )

    print("Disciple Pool:")
    print(disciple_pool)

    # 从弟子池中分配弟子到任务
    for task in publisher.tasks:
        for step in task.steps:
            for level in range(step.required_level, 100):  # 从最低等级到最高等级
                if disciple_pool.has_disciple(level):
                    disciple = disciple_pool.get_disciple(level)
                    disciple.publisher = publisher
                    await publisher.subscribe(disciple)
                    await disciple.take_task(task.name)
                    break

    # 等待所有任务完成
    await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
