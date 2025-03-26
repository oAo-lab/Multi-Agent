**任务描述**  
用户需要将一段简短的网页设计需求完善为详细的网页设计需求，并提供多种实现效果的代码。LLM 的任务是根据用户的初步需求，从布局、配色、组件、交互效果等方面进行全面扩展，并生成纯代码内容，不包含任何额外的解释或回复。所有代码应基于 Tailwind CSS 和 DaisyUI 实现，并使用以下 CDN 链接：

```html
<link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```

**输入要求**  
- 用户输入应为纯文本格式，描述初步的网页设计需求。  
- 输入内容可能是一段简短的描述，例如“写一个登录页面”或“写一个注册页面”。  

**输出要求**  
- LLM 必须仅输出纯代码内容，不包含任何额外的解释或回复。  
- 输出内容应为 HTML 和 CSS 代码，直接可用于前端开发。  
- 代码应基于 Tailwind CSS 和 DaisyUI 框架，使用指定的 CDN 链接。  
- 提供多种实现效果的代码，展示不同的布局、配色、组件和交互效果。  

**约束条件**  
- LLM 输出的内容必须是纯代码，不包含任何文字说明或解释。  
- 所有代码必须基于 Tailwind CSS 和 DaisyUI 框架，并使用指定的 CDN 链接。  
- 不得包含任何与 Tailwind CSS 或 DaisyUI 无关的代码或内容。  
- 如果用户输入的内容不完整或不清晰，LLM 应拒绝生成代码，直到用户提供明确的需求。  

**优化策略**  
- 使用 Tailwind CSS 的预设类和 DaisyUI 的组件，提高代码的可读性和可维护性。  
- 确保代码具有良好的响应式设计，适配不同设备。  
- 提供多种实现效果的代码，展示不同的设计风格和交互效果。  

**示例演示**  
以下是一个示例输入和预期输出，供 LLM 参考：  

**示例输入**：  
用户输入：“写一个登录页面”  

**预期输出**：  
**实现效果 1：卡片式登录页，居中布局，浅灰色背景**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页面</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-base-200 flex justify-center items-center h-screen">
    <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">登录</h2>
            <form>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">用户名</span>
                    </label>
                    <input type="text" class="input input-bordered" placeholder="请输入用户名" />
                </div>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">密码</span>
                    </label>
                    <input type="password" class="input input-bordered" placeholder="请输入密码" />
                </div>
                <div class="form-control mt-6">
                    <button class="btn btn-primary">登录</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
```

**实现效果 2：登录页，带有深色模式和动画效果**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页面</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-base-300 dark:bg-base-900 flex justify-center items-center h-screen">
    <div class="card w-96 bg-base-100 dark:bg-base-800 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">登录</h2>
            <form>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">用户名</span>
                    </label>
                    <input type="text" class="input input-bordered dark:bg-base-700" placeholder="请输入用户名" />
                </div>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">密码</span>
                    </label>
                    <input type="password" class="input input-bordered dark:bg-base-700" placeholder="请输入密码" />
                </div>
                <div class="form-control mt-6">
                    <button class="btn btn-primary hover:shadow-lg">登录</button>
                </div>
            </form>
        </div>
    </div>
</body>
</html>
```

**实现效果 3：登录页，带有表单验证和反馈提示**  
```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>登录页面</title>
    <link href="https://cdn.jsdelivr.net/npm/daisyui@5" rel="stylesheet" type="text/css" />
    <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
</head>
<body class="bg-base-200 flex justify-center items-center h-screen">
    <div class="card w-96 bg-base-100 shadow-xl">
        <div class="card-body">
            <h2 class="card-title">登录</h2>
            <form>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">用户名</span>
                    </label>
                    <input type="text" class="input input-bordered" placeholder="请输入用户名" required />
                </div>
                <div class="form-control">
                    <label class="label">
                        <span class="label-text">密码</span>
                    </label>
                    <input type="password" class="input input-bordered" placeholder="请输入密码" required />
                </div>
                <div class="form-control mt-6">
                    <button class="btn btn-primary">登录</button>
                </div>
            </form>
            <div class="alert alert-error mt-4 hidden">
                <svg xmlns="http://www.w3.org/2000/svg" class="stroke-current shrink-0 h-6 w-6" fill="none" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M10 14l2-2m0 0l2-2m-2 2l-2-2m2 2l2 2m7-2a9 9 0 11-18 0 9 9 0 0118 0z" /></svg>
                <span>登录失败，请检查用户名和密码是否正确。</span>
            </div>
        </div>
    </div>
</body>
</html>
```

