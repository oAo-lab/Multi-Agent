import { EventEmitter } from 'events'
import * as fs from 'fs'
import * as path from 'path'

// 消息接口
interface Message {
  role: 'system' | 'user' | 'assistant'
  content: string
}

// 基础Agent接口
interface Agent {
  execute(task: Task): Promise<string>
  systemPrompt: string
}

// 任务接口
interface Task {
  id: string
  type: TaskType
  content: string
  status: TaskStatus
  messages: Message[]
  result?: any
}

// 任务类型枚举
enum TaskType {
  THINKING = 'THINKING',
  PLANNING = 'PLANNING',
  EXECUTING = 'EXECUTING',
  MONITORING = 'MONITORING',
  COLLABORATING = 'COLLABORATING',
}

// 任务状态枚举
enum TaskStatus {
  PENDING = 'PENDING',
  IN_PROGRESS = 'IN_PROGRESS',
  COMPLETED = 'COMPLETED',
  FAILED = 'FAILED',
}

// 观察者接口
interface Observer {
  update(task: Task): void
}

// 主题接口
interface Subject {
  attach(observer: Observer): void
  detach(observer: Observer): void
  notify(task: Task): void
}

// 结果保存类
class ResultSaver {
  private outputDir: string

  constructor(outputDir: string = 'output') {
    this.outputDir = outputDir
    this.ensureDirectoryExists(outputDir)
  }

  private ensureDirectoryExists(dir: string): void {
    if (!fs.existsSync(dir)) {
      fs.mkdirSync(dir, { recursive: true })
    }
  }

  saveTaskProcess(task: Task): void {
    const processPath = path.join(this.outputDir, `task_${task.id}_process.json`)
    fs.writeFileSync(
      processPath,
      JSON.stringify(
        {
          id: task.id,
          type: task.type,
          status: task.status,
          messages: task.messages,
        },
        null,
        2
      )
    )
    console.log(`任务过程已保存到: ${processPath}`)
  }

  saveTaskResult(task: Task): void {
    const resultPath = path.join(this.outputDir, `task_${task.id}_result.txt`)
    fs.writeFileSync(resultPath, task.result || '')
    console.log(`任务结果已保存到: ${resultPath}`)
  }

  extractAndSaveArtifacts(task: Task): void {
    if (!task.result) return

    const artifacts = this.extractCodeArtifacts(task.result)
    if (Object.keys(artifacts).length === 0) return

    const artifactDir = path.join(this.outputDir, `task_${task.id}_artifacts`)
    this.ensureDirectoryExists(artifactDir)

    Object.entries(artifacts).forEach(([filename, content]) => {
      const filePath = path.join(artifactDir, filename)
      fs.writeFileSync(filePath, content)
      console.log(`代码产物已保存到: ${filePath}`)
    })
  }

  // 提取代码产物
  extractCodeArtifacts(content: string): Record<string, string> {
    const artifacts: Record<string, string> = {}
    const codeBlockRegex = /```(?:html|css|javascript|js|typescript|ts)([\s\S]*?)```/g
    let match
    let index = 0

    while ((match = codeBlockRegex.exec(content)) !== null) {
      const codeContent = match[1].trim()
      let filename = ''

      // 尝试从代码块前的内容中提取文件名
      const prevContent = content.substring(0, match.index).trim()
      const filenameMatch = prevContent.match(/(?:文件名|filename)[：:]\s*([a-zA-Z0-9_\-.]+)/i)

      if (filenameMatch) {
        filename = filenameMatch[1] as unknown as string
      } else {
        // 根据代码类型生成默认文件名
        if (match[0].startsWith('```html')) {
          filename = `index_${index}.html`
        } else if (match[0].startsWith('```css')) {
          filename = `styles_${index}.css`
        } else if (match[0].startsWith('```js') || match[0].startsWith('```javascript')) {
          filename = `script_${index}.js`
        } else if (match[0].startsWith('```ts') || match[0].startsWith('```typescript')) {
          filename = `script_${index}.ts`
        } else {
          filename = `file_${index}.txt`
        }
      }

      artifacts[filename] = codeContent
      index++
    }

    return artifacts
  }
}

// Agent工厂类
class AgentFactory {
  static createAgent(type: string, useCloudLLM: boolean): Agent {
    switch (type) {
      case 'Thinker':
        return new ThinkerAgent(useCloudLLM)
      case 'Preacher':
        return new PreacherAgent(useCloudLLM)
      case 'Executor':
        return new ExecutorAgent(useCloudLLM)
      case 'Monitor':
        return new MonitorAgent(useCloudLLM)
      case 'Collaborator':
        return new CollaboratorAgent(useCloudLLM)
      default:
        throw new Error(`Unknown agent type: ${type}`)
    }
  }
}

// 基础Agent抽象类
abstract class BaseAgent implements Agent {
  systemPrompt: string = ''
  protected useCloudLLM: boolean

  constructor(useCloudLLM: boolean) {
    this.useCloudLLM = useCloudLLM
  }

  protected async callLLM(task: Task, userMessage: string): Promise<string> {
    try {
      if (task.messages.length === 0) {
        task.messages.push({
          role: 'system',
          content: this.systemPrompt,
        })
      }

      task.messages.push({
        role: 'user',
        content: userMessage,
      })

      const body = JSON.stringify({
        model: this.useCloudLLM ? 'qwen-long' : 'deepseek-r1:1.5b',
        messages: task.messages,
        stream: false,
      })

      const response = await fetch(
        this.useCloudLLM
          ? 'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions'
          : 'http://localhost:11434/api/chat',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            Authorization: 'Bearer sk-xxx', // TODO: 需要修正
          },
          body,
        }
      )

      let assistantMessage = ''
      const data = await response.json()

      if (this.useCloudLLM) {
        assistantMessage = data.choices[0].message.content
      } else {
        assistantMessage = data.message.content
      }
      
      task.messages.push({
        role: 'assistant',
        content: assistantMessage,
      })

      return assistantMessage
    } catch (error) {
      console.error('Error calling LLM:', error)
      throw error
    }
  }

  abstract execute(task: Task): Promise<string>
}

// 沉思者Agent
class ThinkerAgent extends BaseAgent {
  constructor(useCloudLLM: boolean) {
    super(useCloudLLM)
    this.systemPrompt = `你是一个专注于需求分析的AI助手。你的职责是：
1. 深入理解用户的初始需求
2. 通过提问引导用户明确需求细节
3. 总结并确认最终的需求规格
请以专业、耐心的态度与用户交互，直到需求完全明确。`
  }

  async execute(task: Task): Promise<string> {
    console.log('ThinkerAgent analyzing user requirements...')
    const response = await this.callLLM(task, `当前用户需求：${task.content}\n请分析需求并提出澄清问题。`)
    console.log('Analysis result:', response)
    return response
  }
}

// 布道者Agent
class PreacherAgent extends BaseAgent {
  constructor(useCloudLLM: boolean) {
    super(useCloudLLM)
    this.systemPrompt = `你是一个专注于任务分解的AI助手。你的职责是：
1. 将复杂需求分解为可执行的子任务
2. 为每个子任务定义清晰的目标和验收标准
3. 确定子任务之间的依赖关系
请以系统化、结构化的方式进行任务拆分。`
  }

  async execute(task: Task): Promise<string> {
    console.log('PreacherAgent breaking down tasks...')
    const response = await this.callLLM(task, `需要拆分的任务：${task.content}\n请进行任务分解。`)
    console.log('Task breakdown:', response)
    return response
  }
}

// 执行者Agent
class ExecutorAgent extends BaseAgent {
  constructor(useCloudLLM: boolean) {
    super(useCloudLLM)
    this.systemPrompt = `你是一个专注于任务执行的AI助手。你的职责是：
1. 按照任务规格执行具体实现
2. 确保代码质量和功能完整性
3. 生成必要的测试用例
请以专业、严谨的态度完成任务实现。`
  }

  async execute(task: Task): Promise<string> {
    console.log('ExecutorAgent executing task...')
    const response = await this.callLLM(task, `待执行的任务：${task.content}\n请开始实现。`)
    console.log('Execution result:', response)
    return response
  }
}

// 监督者Agent
class MonitorAgent extends BaseAgent implements Observer {
  constructor(useCloudLLM: boolean) {
    super(useCloudLLM)
    this.systemPrompt = `你是一个专注于任务监督的AI助手。你的职责是：
1. 监控任务执行的全过程
2. 评估执行结果是否符合需求
3. 提供优化建议和改进方向
请以客观、严谨的态度进行监督和反馈。`
  }

  async execute(task: Task): Promise<string> {
    console.log('MonitorAgent monitoring task...')
    const response = await this.callLLM(
      task,
      `待监控的任务：${task.content}\n当前执行状态：${task.status}\n请评估执行情况并提供反馈。`
    )
    console.log('Monitoring result:', response)
    return response
  }

  update(task: Task): void {
    console.log(`Task ${task.id} status updated to: ${task.status}`)
    this.execute(task).catch(console.error)
  }
}

// 协作者Agent
class CollaboratorAgent extends BaseAgent {
  constructor(useCloudLLM: boolean) {
    super(useCloudLLM)
    this.systemPrompt = `你是一个专注于任务协调的AI助手。你的职责是：
1. 制定任务执行计划
2. 协调各个执行者之间的配合
3. 确保任务按计划推进
请以高效、有序的方式进行任务调度。`
  }

  async execute(task: Task): Promise<string> {
    console.log('CollaboratorAgent providing task scheduling...')
    const response = await this.callLLM(task, `待调度的任务：${task.content}\n请制定执行计划。`)
    console.log('Scheduling result:', response)
    return response
  }
}

// 用户交互接口
interface UserInteraction {
  askQuestion(question: string): Promise<string>
  close(): void
}

// 控制台用户交互实现
class ConsoleUserInteraction implements UserInteraction {
  private readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  async askQuestion(question: string): Promise<string> {
    return new Promise((resolve) => {
      this.readline.question(question + '\n', (answer: string) => {
        resolve(answer)
      })
    })
  }

  close() {
    this.readline.close()
  }
}

// 任务管理器类
class TaskManager extends EventEmitter implements Subject {
  private observers: Observer[] = []
  private tasks: Map<string, Task> = new Map()
  private agents: Map<string, Agent> = new Map()
  private userInteraction: UserInteraction
  private resultSaver: ResultSaver
  private useCloudLLM: boolean

  constructor(userInteraction: UserInteraction, useCloudLLM: boolean) {
    super()
    this.userInteraction = userInteraction
    this.resultSaver = new ResultSaver()

    // 初始化所有Agent
    this.agents.set('Thinker', AgentFactory.createAgent('Thinker', useCloudLLM))
    this.agents.set('Preacher', AgentFactory.createAgent('Preacher', useCloudLLM))
    this.agents.set('Executor', AgentFactory.createAgent('Executor', useCloudLLM))
    this.agents.set('Monitor', AgentFactory.createAgent('Monitor', useCloudLLM))
    this.agents.set('Collaborator', AgentFactory.createAgent('Collaborator', useCloudLLM))

    // 添加监督者作为观察者
    const monitorAgent = this.agents.get('Monitor') as MonitorAgent
    this.attach(monitorAgent)

    this.useCloudLLM = useCloudLLM
  }

  attach(observer: Observer): void {
    const index = this.observers.indexOf(observer)
    if (index === -1) {
      this.observers.push(observer)
    }
  }

  detach(observer: Observer): void {
    const index = this.observers.indexOf(observer)
    if (index !== -1) {
      this.observers.splice(index, 1)
    }
  }

  notify(task: Task): void {
    for (const observer of this.observers) {
      observer.update(task)
    }
  }

  createTask(content: string, type: TaskType): Task {
    const task: Task = {
      id: Math.random().toString(36).substr(2, 9),
      type,
      content,
      status: TaskStatus.PENDING,
      messages: [],
    }
    this.tasks.set(task.id, task)
    return task
  }

  updateTaskStatus(taskId: string, status: TaskStatus): void {
    const task = this.tasks.get(taskId)
    if (task && task.status !== status) {
      task.status = status
      this.emit('statusChanged', task)
      this.notify(task)
      this.resultSaver.saveTaskProcess(task)
    }
  }

  async executeTask(task: Task): Promise<void> {
    this.updateTaskStatus(task.id, TaskStatus.IN_PROGRESS)

    try {
      // 1. 需求分析阶段 - 沉思者进行多轮对话
      const thinkerAgent = this.agents.get('Thinker')
      if (!thinkerAgent) throw new Error('Thinker agent not found')
      let requirementAnalysis = await thinkerAgent.execute(task)

      // 自动判断需求是否明确
      let isRequirementClear = await this.isRequirementClear(requirementAnalysis)
      while (!isRequirementClear) {
        const additionalInfo = await this.userInteraction.askQuestion('请提供补充说明：')
        task.content += '\n用户补充：' + additionalInfo
        requirementAnalysis = await thinkerAgent.execute(task)
        isRequirementClear = await this.isRequirementClear(requirementAnalysis)
      }
      task.content = requirementAnalysis

      // 2. 任务拆分阶段 - 布道者拆分任务
      const preacherAgent = this.agents.get('Preacher')
      if (!preacherAgent) throw new Error('Preacher agent not found')
      const taskBreakdown = await preacherAgent.execute(task)

      // 3. 任务调度阶段 - 协作者制定执行计划
      const collaboratorAgent = this.agents.get('Collaborator')
      if (!collaboratorAgent) throw new Error('Collaborator agent not found')
      const executionPlan = await collaboratorAgent.execute({ ...task, content: taskBreakdown })

      // 4. 任务执行阶段 - 执行者执行任务
      const executorAgent = this.agents.get('Executor')
      if (!executorAgent) throw new Error('Executor agent not found')
      const executionResult = await executorAgent.execute({ ...task, content: executionPlan })

      // 保存执行结果
      task.result = executionResult
      this.resultSaver.saveTaskResult(task)
      this.resultSaver.extractAndSaveArtifacts(task)

      // 5. 监督者评估结果
      const monitorAgent = this.agents.get('Monitor')
      if (!monitorAgent) throw new Error('Monitor agent not found')
      const evaluation = await monitorAgent.execute({ ...task, content: executionResult })

      task.result += '\n\n评估结果：\n' + evaluation
      this.resultSaver.saveTaskResult(task)

      this.updateTaskStatus(task.id, TaskStatus.COMPLETED)
    } catch (error) {
      console.error('Error executing task:', error)
      this.updateTaskStatus(task.id, TaskStatus.FAILED)
      throw error
    }
  }

  private async isRequirementClear(requirementAnalysis: string): Promise<boolean> {
    // 这里可以添加更复杂的逻辑来自动判断需求是否明确
    // 例如使用自然语言处理模型或关键词匹配等方法
    return requirementAnalysis.includes('明确') || requirementAnalysis.includes('确定')
  }
}

// 主程序入口
async function main() {
  const useCloudLLM = await askUseCloudLLM()
  const userInteraction = new ConsoleUserInteraction()
  const taskManager = new TaskManager(userInteraction, useCloudLLM)

  try {
    // 获取用户初始需求
    const initialRequirement = await userInteraction.askQuestion('请描述您的需求：')

    // 创建并执行任务
    const task = taskManager.createTask(initialRequirement, TaskType.THINKING)
    await taskManager.executeTask(task)

    console.log('\n任务执行完成！')
    console.log(`所有结果已保存到 output 目录中，任务ID: ${task.id}`)
  } catch (error) {
    console.error('程序执行出错：', error)
  } finally {
    userInteraction.close()
  }
}

async function askUseCloudLLM(): Promise<boolean> {
  const readline = require('readline').createInterface({
    input: process.stdin,
    output: process.stdout,
  })

  return new Promise((resolve) => {
    readline.question('您希望使用云端AI吗？(yes/no): ', (answer: any) => {
      readline.close()
      resolve(answer.toLowerCase() === 'yes')
    })
  })
}

// 运行主程序
main().catch(console.error)
