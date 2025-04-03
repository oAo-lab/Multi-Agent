import { fetch } from 'bun'

interface ApiResponse<T> {
  success: boolean
  data?: T
  error?: string
}

type ApiCallback<T> = (result: ApiResponse<T>) => void

interface RequestOptions {
  stream?: boolean
  signal?: AbortSignal
}

interface ModelDetails {
  parent_model: string
  format: string
  family: string
  families: string[]
  parameter_size: string
  quantization_level: string
}

interface TagInfo {
  name: string
  model: string
  modified_at: string
  size: number
  digest: string
  details: ModelDetails
}

interface ListModelsResponse {
  models: TagInfo[]
}

interface OllamaChatParmas {
  model: string
  messages: Array<{ role: string; content: string }>
  stream: boolean
}

interface OllamaParmas {
  model: string
  prompt: string
  stream: boolean
}

interface OllamaResponse {
  model: string
  created_at: string
  response?: string
  message?: {
    role: string
    content: string
  }
  done: boolean
  done_reason: string
  context: Array<string>
}

class OllamaClient {
  private baseUrl: string

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl
  }

  private async callApi<T>(
    endpoint: string,
    method: string = 'POST',
    body?: Record<string, any>,
    options?: RequestOptions
  ): Promise<T | undefined> {
    return fetch(`${this.baseUrl}${endpoint}`, {
      method: method,
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(body),
      signal: options?.signal,
    })
      .then(async (response) => {
        if (!response.ok) throw new Error(`HTTP ${response.status}: ${response.statusText}`)
        const text = await response.text()
        try {
          return options?.stream ? text : JSON.parse(text)
        } catch (parseError) {
          throw new Error('Failed to parse JSON')
        }
      })
      .catch((error) => {
        console.error(error)
        throw error
      })
  }

  private handleRequestWithCallback<T>(
    endpoint: string,
    method: string = 'POST',
    params?: Record<string, any>,
    callback?: ApiCallback<T>,
    options?: RequestOptions
  ) {
    this.callApi<T>(endpoint, method, params, options)
      .then((data) => callback && callback({ success: true, data }))
      .catch((err) => callback && callback({ success: false, error: err.message }))
  }

  public generateText(params: OllamaParmas, callback: ApiCallback<string>, options?: RequestOptions) {
    this.handleRequestWithCallback<string>('/api/generate', 'POST', params, callback, options)
  }

  public chat(
    params: { model: string; messages: Array<{ role: string; content: string }>; stream: boolean },
    callback: ApiCallback<string>,
    options?: RequestOptions
  ) {
    this.handleRequestWithCallback<string>('/api/chat', 'POST', params, callback, options)
  }

  public listModels(callback: ApiCallback<Array<{ name: string }>>) {
    this.handleRequestWithCallback<ListModelsResponse>('/api/tags', 'GET', undefined, (result: any) => {
      if (result.success) {
        const modelsOnly = result.data.models.map(({ name }: { name: string }) => name)
        callback({ success: true, data: modelsOnly })
      } else {
        callback({ success: false, error: result.error })
      }
    })
  }

  public pullModel(params: { name: string }, callback: ApiCallback<{ status: string; digest: string }>) {
    this.handleRequestWithCallback<{ status: string; digest: string }>('/api/pull', 'POST', params, callback)
  }
}

const useOllama = (baseUrl: string): OllamaClient => {
  return new OllamaClient(baseUrl)
}

export { useOllama, type ApiResponse, type OllamaChatParmas, type OllamaParmas, type OllamaResponse }
