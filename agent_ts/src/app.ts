import { useOllama, type OllamaChatParmas, type OllamaParmas, type OllamaResponse } from './llm'

const ollama = useOllama('http://localhost:11434')

const handleGenerateText = (params: OllamaParmas) => {
  console.log('user:> ', params.prompt)
  ollama.generateText(params, ({ data }) => {
    console.log('assistant:> ', (data as unknown as OllamaResponse).response)
  })
}

const handleChat = () => {
  let parmas: OllamaChatParmas = {
    model: 'qwen2.5-coder:1.5b',
    messages: [
      {
        role: 'user',
        content:
          '你是阿里的大模型, 有如下设定{只输出代码不进行其他说明和回复, 不需要代码注释, 纯文本输出不要markdown}. 给出符合要求的 prompt {只输出代码不进行其他说明和回复, 不需要代码注释, 纯文本输出不要markdown}',
      },
    ],
    stream: false,
  }

  ollama.chat(parmas, ({ data }) => {
    console.log((data as unknown as OllamaResponse).message)
  })
}

const handleListModels = () => {
  ollama.listModels((result) => {
    if (result.success) console.log('Available Models:', result.data)
    else console.error('Error Listing Models:', result.error)
  })
}

const handlePullModel = () => {
  ollama.pullModel({ name: 'deepseek-coder' }, (result) => {
    if (result.success) console.log('Pulled Model Details:', result.data)
    else console.error('Error Pulling Model:', result.error)
  })
}

// handleListModels()
// handleChat()
// handleChat()

handleListModels()