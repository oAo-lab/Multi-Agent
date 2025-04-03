// 定义 Handler 接口
interface Handler {
    handle(request: string): boolean
  }
  
  // 实现具体的处理逻辑
  class ConcreteHandlerA implements Handler {
    public successor: Handler | null = null
  
    public setNext(handler: Handler): void {
      this.successor = handler
    }
  
    public handle(request: string): boolean {
      if (this.canHandle(request)) {
        console.log(`ConcreteHandlerA handles the request ${request}`)
        return true
      } else if (this.successor !== null) {
        return this.successor.handle(request)
      }
      return false
    }
  
    private canHandle(request: string): boolean {
      return request === 'A'
    }
  }
  
  class ConcreteHandlerB implements Handler {
    public successor: Handler | null = null
  
    public setNext(handler: Handler): void {
      this.successor = handler
    }
  
    public handle(request: string): boolean {
      if (this.canHandle(request)) {
        console.log(`ConcreteHandlerB handles the request ${request}`)
        return true
      } else if (this.successor !== null) {
        return this.successor.handle(request)
      }
      return false
    }
  
    private canHandle(request: string): boolean {
      return request === 'B'
    }
  }
  
  class ConcreteHandlerC implements Handler {
    public successor: Handler | null = null
  
    public setNext(handler: Handler): void {
      this.successor = handler
    }
  
    public handle(request: string): boolean {
      if (this.canHandle(request)) {
        console.log(`Error Handle ConcreteHandlerC handles the request ${request}`)
        return true
      } else if (this.successor !== null) {
        return this.successor.handle(request)
      }
      return false
    }
  
    private canHandle(request: string): boolean {
      return request === 'C'
    }
  }
  
  // 创建责任链
  const handlerA = new ConcreteHandlerA()
  const handlerB = new ConcreteHandlerB()
  const handlerC = new ConcreteHandlerC()
  
  handlerA.setNext(handlerB)
  handlerB.setNext(handlerC)