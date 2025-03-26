from typing import Dict, List
from async_agent import PromptTemplate

def get_frontend_templates() -> List[PromptTemplate]:
    """获取前端开发相关的提示词模板"""
    return [
        PromptTemplate(
            name="component_development",
            description="用于指导React/Vue组件开发的提示词模板",
            template="""作为一个前端开发专家，请帮助开发一个{component_type}组件。要求：
1. 遵循{framework}最佳实践和设计模式
2. 实现{features}功能
3. 确保代码可复用性和可维护性
4. 添加必要的类型定义和注释
5. 考虑性能优化和边界情况""",
            parameters={
                "component_type": "组件类型，如：表单、列表、弹窗等",
                "framework": "使用的框架，如：React、Vue",
                "features": "需要实现的具体功能描述"
            }
        ),
        PromptTemplate(
            name="styling_guide",
            description="用于指导前端样式编写的提示词模板",
            template="""作为UI/UX专家，请帮助优化组件样式。要求：
1. 使用{style_approach}方案（如：CSS Modules、Styled Components等）
2. 实现{design_spec}设计规范
3. 确保响应式布局和跨浏览器兼容性
4. 优化动画和过渡效果
5. 考虑深色模式和主题定制""",
            parameters={
                "style_approach": "样式解决方案",
                "design_spec": "设计规范和要求"
            }
        ),
        PromptTemplate(
            name="state_management",
            description="用于指导前端状态管理的提示词模板",
            template="""作为状态管理专家，请帮助设计状态管理方案。要求：
1. 使用{state_solution}方案
2. 处理{state_type}类型的状态
3. 实现数据持久化和同步
4. 优化性能和内存使用
5. 处理异步操作和副作用""",
            parameters={
                "state_solution": "状态管理方案，如：Redux、Vuex、Pinia等",
                "state_type": "状态类型，如：用户数据、主题设置等"
            }
        ),
        PromptTemplate(
            name="api_integration",
            description="用于指导前端API集成的提示词模板",
            template="""作为前端集成专家，请帮助设计API集成方案。要求：
1. 使用{http_client}发起请求
2. 实现{api_features}功能
3. 处理错误和异常情况
4. 实现请求缓存和优化
5. 确保数据类型安全""",
            parameters={
                "http_client": "HTTP客户端，如：Axios、Fetch等",
                "api_features": "API功能描述，如：认证、数据获取等"
            }
        ),
        PromptTemplate(
            name="testing_guide",
            description="用于指导前端测试编写的提示词模板",
            template="""作为测试专家，请帮助编写前端测试用例。要求：
1. 使用{test_framework}框架
2. 测试{test_scope}范围的功能
3. 包含单元测试和集成测试
4. 模拟异步操作和副作用
5. 确保测试覆盖率""",
            parameters={
                "test_framework": "测试框架，如：Jest、Vitest等",
                "test_scope": "测试范围，如：组件渲染、状态更新等"
            }
        ),
        PromptTemplate(
            name="optimization_guide",
            description="用于指导前端性能优化的提示词模板",
            template="""作为性能优化专家，请帮助优化前端性能。要求：
1. 优化{optimization_target}方面的性能
2. 实现代码分割和懒加载
3. 优化资源加载和缓存
4. 减少不必要的渲染
5. 优化打包和构建过程""",
            parameters={
                "optimization_target": "优化目标，如：首屏加载、运行时性能等"
            }
        )
    ]