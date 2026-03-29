/**
 * 飞书Python工具箱 - 主要JavaScript文件
 */

// 全局配置
const CONFIG = {
    apiBaseUrl: '/api',
    defaultAI: 'claude'
};

// AI模型配置
const AI_MODELS = {
    claude: {
        name: 'Claude 3.5 Sonnet',
        id: 'claude-3-5-sonnet-20241022',
        color: '#9B59B6'
    },
    gpt: {
        name: 'GPT-4 Omni',
        id: 'gpt-4o',
        color: '#10B981'
    },
    deepseek: {
        name: 'DeepSeek R1',
        id: 'deepseek-chat',
        color: '#FF9500'
    }
};

// 应用状态
let appState = {
    tables: [],
    documents: [],
    events: [],
    tasks: [],
    messages: []
};

// 工具函数
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `alert alert-${type} position-fixed`;
    toast.style.css = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        max-width: 400px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        animation: slideIn 0.3s ease-out;
    `;
    toast.innerHTML = message;
    document.body.appendChild(toast);
    
    setTimeout(() => {
        toast.style.opacity = '0';
        setTimeout(() => {
            document.body.removeChild(toast);
        }, 300);
    }, 3000);
}

// 模态框函数
function showModal(title, content, footer = null) {
    const modalHtml = `
        <div class="modal fade show" tabindex="-1" role="dialog">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h5 class="modal-title">${title}</h5>
                        <button type="button" class="btn-close" data-bs-dismiss="modal" aria-label="Close" onclick="closeModal()"></button>
                    </div>
                    <div class="modal-body">
                        ${content}
                    </div>
                    ${footer ? `<div class="modal-footer">${footer}</div>` : ''}
                </div>
            </div>
        </div>
    `;
    
    document.body.insertAdjacentHTML('beforeend', modalHtml);
    
    // 绑听关闭按钮
    const closeBtn = document.querySelector('.btn-close');
    if (closeBtn) {
        closeBtn.addEventListener('click', closeModal);
    }
}

function closeModal() {
    const modal = document.querySelector('.modal');
    if (modal) {
        modal.classList.remove('show');
        setTimeout(() => {
            if (modal.parentNode) {
                modal.parentNode.removeChild(modal);
            }
        }, 300);
    }
}

// API调用函数
async function callApi(endpoint, method = 'GET', data = null) {
    try {
        const options = {
            method: method,
            headers: {
                'Content-Type': 'application/json'
            }
        };
        
        if (data) {
            options.body = JSON.stringify(data);
        }
        
        const response = await fetch(`${CONFIG.apiBaseUrl}${endpoint}`, options);
        const result = await response.json();
        return result;
    } catch (error) {
        console.error('API调用失败:', error);
        showToast(`错误: ${error.message}`, 'danger');
        return { success: false, error: error.message };
    }
}

// 自然语言查询
async function executeNLQuery() {
    const query = document.getElementById('nlQueryInput').value;
    const resultDiv = document.getElementById('nlQueryResult');
    
    if (!query.trim()) {
        showToast('请输入查询内容', 'warning');
        return;
    }
    
    resultDiv.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border"></div> 正在分析查询...</div>';
    
    const result = await callApi('/ai/query', 'POST', { query, context: { data: "你的数据" } });
    
    if (result.success) {
        let resultHtml = '<div class="alert alert-success"><i class="bi bi-check-circle"></i> 查询成功！</div>';
        resultHtml += `<p><strong>意图：</strong>${result.intent}</p>`;
        
        if (result.result) {
            resultHtml += `<p><strong>结果：</strong></p>`;
            if (typeof result.result === 'string') {
                resultHtml += `<code>${result.result}</code>`;
            } else if (Array.isArray(result.result)) {
                resultHtml += `<ul class="list-group">`;
                result.result.forEach(item => {
                    resultHtml += `<li class="list-group-item">${JSON.stringify(item)}</li>`;
                });
                resultHtml += '</ul>';
            } else if (typeof result.result === 'number') {
                resultHtml += `<div class="alert alert-info"><strong>数值：</strong> ${result.result}</div>`;
            }
        }
        
        resultDiv.innerHTML = resultHtml;
    } else {
        resultDiv.innerHTML = `<div class="alert alert-danger"><i class="bi bi-exclamation-circle"></i> 查询失败：${result.error}</div>`;
    }
}

// 智能推荐
async function getRecommendations() {
    const input = document.getElementById('recommendInput').value;
    const resultDiv = document.getElementById('recommendationResult');
    
    if (!input.trim()) {
        showToast('请描述你的任务或需求', 'warning');
        return;
    }
    
    resultDiv.innerHTML = '<div class="d-flex justify-content-center"><div class="spinner-border"></div> 正在生成推荐...</div>';
    
    const result = await callApi('/ai/recommend', 'POST', { context: { task: input } });
    
    if (result.success) {
        let resultHtml = '<div class="alert alert-success"><i class="bi bi-lightbulb"></i> 推荐结果：</div>';
        
        result.recommendations.forEach(rec => {
            resultHtml += `<div class="card mt-2 p-3">`;
            resultHtml += `<h5>${rec.title}</h5>`;
            resultHtml += `<p class="text-muted">${rec.reason}</p>`;
            resultHtml += `<span class="badge bg-primary">${rec.priority || 'Medium'}</span>`;
            resultHtml += ` <span class="badge bg-secondary">${rec.type || '未知'}</span>`;
            resultHtml += `</div>`;
        });
        
        resultDiv.innerHTML = resultHtml;
    } else {
        resultDiv.innerHTML = `<div class="alert alert-danger"><i class="bi-exclamation-triangle"></i> 生成失败：${result.error}</div>`;
    }
}

// 工作流引擎
class WorkflowEngine {
    constructor() {
        this.workflows = [];
        this.triggers = [];
    }
    
    addWorkflow(workflow) {
        this.workflows.push(workflow);
        console.log(`添加工作流: ${workflow.name}`);
    }
    
    addTrigger(trigger) {
        this.triggers.push(trigger);
        console.log(`添加触发器: ${trigger.name}`);
    }
    
    async executeWorkflow(workflowId, context = {}) {
        const workflow = this.workflows.find(w => w.id === workflowId);
        if (!workflow) {
            console.error(`工作流不存在: ${workflowId}`);
            return;
        }
        
        console.log(`执行工作流: ${workflow.name}`);
        for (step of workflow.steps) {
            const result = await this.executeStep(step, context);
            context = { ...context, ...result };
        }
        
        return context;
    }
    
    async executeStep(step, context) {
        console.log(`执行步骤: ${step.name}`);
        // 这里实现具体的步骤执行逻辑
        switch (step.type) {
            case 'api_call':
                return await this.callAPI(step.api_endpoint, step.method, step.params, context);
            case 'condition':
                return this.evaluateCondition(step.condition, context);
            case 'data_processing':
                return this.processData(step.operation, step.params, context);
            case 'notification':
                return this.sendNotification(step.message, step.recipient, context);
            default:
                console.log(`未知步骤类型: ${step.type}`);
                return context;
        }
    }
    
    evaluateCondition(condition, context) {
        // 评估条件
        const left = this.getValue(condition.left, context);
        const right = this.getValue(condition.right, context);
        const operator = condition.operator;
        
        switch (operator) {
            case '==': return left === right;
            case '!=': return left != right;
            case '>': return left > right;
            case '<': return left < right;
            case '>=': return left >= right;
            case '<=': return left <= right;
            case 'in': return Array.isArray(right) && right.includes(left);
            'not in': return !Array.isArray(right) || !right.includes(left);
            default: return false;
        }
    }
    
    getValue(path, context) {
        const keys = path.split('.');
        let value = context;
        for (const key of keys) {
            if (value && key in value) {
                value = value[key];
            } else {
                return undefined;
            }
        }
        return value;
    }
    
    async callAPI(endpoint, method, params, context) {
        // API调用
        return await callApi(endpoint, method, {
            ...params,
            ...context
        });
    }
    
    processData(operation, params, context) {
        // 数据处理
        switch (operation) {
            'filter': return this.filterData(params.field, params.value, context);
            'aggregate': return this.aggregateData(params.field, params.function, context);
            'transform': return this.transformData(params.fields, context);
            default: return context;
        }
    }
    
    filterData(field, value, context) {
        return {
            ...context,
            filtered_data: context.data.filter(row => row[field] == value)
        };
    }
    
    aggregateData(field, func, context) {
        const data = context.data || [];
        const values = data.map(row => row[field]);
        
        let result;
        switch (func) {
            'sum': result = values.reduce((a, b) => a + b, 0);
            'avg': result = values.reduce((a, b) => (a + b) / values.length, 0);
            'max': result = Math.max(...values);
            'min': result = Math.min(...values);
            'count': values.length;
        }
        
        return {
            ...context,
            aggregated_data: result
        };
    }
    
    transformData(fields, context) {
        const data = context.data || [];
        const transformed = data.map(row => {
            const newRow = {};
            fields.forEach(field => {
                newRow[field] = row[field];
            });
            return newRow;
        });
        
        return {
            ...context,
            transformed_data: transformed
        };
    }
    
    sendNotification(message, recipient, context) {
        console.log(`发送通知给 ${recipient}: ${message}`);
        return {
            ...context,
            notification_sent: true
        };
    }
}

// 全局工作流引擎实例
const workflowEngine = new WorkflowEngine();

// 示例工作流
const exampleWorkflow = {
    id: "daily_report",
    name: "每日报告生成",
    steps: [
        {
            id: "step1",
            name: "获取今日数据",
            type: "api_call",
            api_endpoint: "/api/bitable/records",
            method: "GET",
            params: {
                app_token: "AXDyb30BNamJJ6sMYh2cda7Gnxg",
                table_id: "tblcpk0OtPpxNwrs"
            }
        },
        {
            id: "condition1",
            name: "检查库存低于最小值",
            type: "condition",
            condition: {
                left: "min_stock",
                operator: "<",
                right: "current_stock"
            }
        },
        {
            id: "step2",
            name: "发送库存警告",
            type: "notification",
            message: "库存不足警告",
            recipient: "ou_xxx"
        },
        {
            id: "step3",
            name: "生成报告",
            type: "data_processing",
            operation: "aggregate",
            field: "amount",
            function: "sum"
        }
    ]
};

workflowEngine.addWorkflow(exampleWorkflow);

// 初始化
document.addEventListener('DOMContentLoaded', function() => {
    // 页面加载完成后执行的代码
    console.log('飞书Python工具箱 v2.0.0 已加载');
    
    // 加载应用状态
    loadAppState();
    
    // 设置当前AI模型
    updateAIModel('claude');
    
    // 绑定事件
    bindEvents();
});

async function loadAppState() {
    // 获取仪表盘数据
    const tables = await callApi('/api/bitable/tables', 'GET');
    if (tables.success) {
        appState.tables = tables;
        updateDashboard();
    }
}

function updateDashboard() {
    // 更新仪表盘统计
    document.getElementById('tableCount').textContent = appState.tables.length || 0;
}

function updateAIModel(model) {
    // 更新当前AI模型
    CONFIG.defaultAI = model;
}

function bindEvents() {
    // 绑定所有按钮事件
    document.querySelectorAll('button').forEach(btn => {
        btn.addEventListener('click', handleButtonClick);
    });
}

function handleButtonClick(event) {
    const button = event.target.closest('button');
    const action = button.getAttribute('data-action');
    
    switch(action) {
        case 'showBitableModal':
            showBitableModal();
            break;
        case 'showDocModal':
            showDocModal();
            break;
        case 'showCalendarModal':
            showCalendarModal();
            break;
        case 'showTaskModal':
            showTaskModal();
            break;
        case 'showMessageModal':
            showMessageModal();
            break;
        case 'showAIModal':
            showAIModal();
            break;
        default:
            console.log('未知操作:', action);
    }
}

// 模态框函数
function showBitableModal() {
    showModal('管理多维表格', `
        <form id="bitableForm">
            <div class="mb-3">
                <label for="appToken">App Token</label>
                <input type="text" class="form-control" id="appToken" placeholder="输入飞书多维表格的app_token">
            </div>
            <div class="mb-3">
                <label for="tableId">表格ID</label>
                <input type="text" class="form-control" id="tableId" placeholder="输入数据表ID">
            </div>
            <div class="mb-3">
                <label>操作</label>
                <select class="form-select" id="bitableAction">
                    <option value="list">列出记录</option>
                    <option value="create">创建记录</option>
                    <option value="export">导出数据</option>
                </select>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeBitableAction()">执行</button>
            </div>
        </form>
    `);
}

function showDocModal() {
    showModal('管理文档', `
        <form id="docForm">
            <div class="mb-3">
                <label for="docTitle">文档标题</label>
                <input type="text" class="form-control" id="docTitle" placeholder="输入文档标题">
            </div>
            <div class="mb-3">
                <label for="docContent">文档内容（Markdown格式）</label>
                <textarea class="form-control" id="docContent" rows="10" placeholder="输入文档内容（支持Markdown）"></textarea>
            </div>
            <div class="mb-3">
                <label>权限</label>
                <select class="form-select" id="docPermission">
                    <option value="write">可写</option>
                    <option value="read">只读</option>
                </select>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeDocAction()">创建文档</button>
            </div>
        </form>
    `);
}

function showCalendarModal() {
    showModal('管理日历', `
        <form id="calendarForm">
            <div class="mb-3">
                <label for="calendarId">日历ID</label>
                <input type="text" class="form-control" id="calendarId" placeholder="输入日历ID">
            </div>
            <div class="mb-3">
                <label for="eventTitle">日程标题</label>
                <input type="text" class="form-control" id="eventTitle" placeholder="输入日程标题">
            </div>
            <div class="mb-3">
                <label>开始时间</label>
                <input type="datetime-local" class="form-control" id="startTime">
            </div>
            <div class="mb-3">
                <label>结束时间</label>
                <input type="datetime-local" class="form-control" id="endTime">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeCalendarAction()">创建日程</button>
            </div>
        </form>
    `);
}

function showTaskModal() {
    showModal('管理任务', `
        <form id="taskForm">
            <div class="mb-3">
                <label for="tasklistGuid">任务清单ID</label>
                <input type="text" class="form-control" id="tasklistGuid" placeholder="输入任务清单ID">
            </div>
            <div class="mb-3">
                <label for="taskSummary">任务标题</label>
                <input type="text" class="form-control" id="taskSummary" placeholder="输入任务标题">
            </div>
            <div class="mb-3">
                <label for="taskDescription">任务描述</label>
                <textarea class="form-control" id="taskDescription" rows="5" placeholder="输入任务描述"></textarea>
            </div>
            <div class="mb-3">
                <label>截止时间</label>
                <input type="datetime-local" class="form-control" id="taskDue">
            </div>
            <div class="mb-3">
                <label>负责人</label>
                <input type="text" class="form-control" id="taskAssignee" placeholder="输入负责人ID">
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeTaskAction()">创建任务</button>
            </div>
        </form>
    `);
}

function showMessageModal() {
    showModal('发送消息', `
        <form id="messageForm">
            <div class="mb-3">
                <label for="receiveId">接收者ID</label>
                <input type="text" class="form-control" id="receiveId" placeholder="输入接收者ID">
            </div>
            <div class="mb-3">
                <label for="messageContent">消息内容</label>
                <textarea class="form-control" id="messageContent" rows="5" placeholder="输入消息内容"></textarea>
            </div>
            <div class="mb-3">
                <label>接收者类型</label>
                <select class="form-select" id="receiveIdType">
                    <option value="open_id">用户ID</option>
                    <option value="chat_id">群聊ID</option>
                </select>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeMessageAction()">发送消息</button>
            </div>
        </form>
    `);
}

function showAIModal() {
    showModal('AI查询', `
        <form id="aiQueryForm">
            <div class="mb-3">
                <label>AI模型</label>
                <select class="form-select" id="aiModelSelect">
                    <option value="claude" selected>Claude 3.5</option>
                    <option value="gpt">GPT-4</option>
                    <option value="deepseek">DeepSeek</option>
                </select>
            </div>
            <div class="mb-3">
                <label>查询类型</label>
                <select class="form-select" id="aiQueryType">
                    <option value="nl_query">自然语言查询</option>
                    <option value="data_clean">数据清洗</option>
                    <option value="recommend">智能推荐</option>
                </select>
            </div>
            <div class="mb-3">
                <label>查询/提示词</label>
                <textarea class="form-control" id="aiQuery" rows="5" placeholder="输入查询或提示词"></textarea>
            </div>
            <div class="modal-footer">
                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">取消</button>
                <button type="button" class="btn btn-primary" onclick="executeAIAction()">执行</button>
            </div>
        </form>
    `);
}

// 执行操作
async function executeBitableAction() {
    const action = document.getElementById('bitableAction').value;
    const appToken = document.getElementById('appToken').value;
    const tableId = documentId('tableId').value;
    
    closeModal();
    
    switch (action) {
        case 'list':
            await callApi('/api/bitable/records', 'GET', { app_token: appToken, table_id: tableId });
            showToast('记录列表已更新', 'success');
            break;
        case 'create':
            // 实际应用中需要用户提供字段数据
            const fields = {
                "test_field": "test_value"
            };
            await callApi('/api/bitable/records', 'POST', {
                app_token: appToken,
                table_id: tableId,
                fields: fields
            });
            showToast('记录已创建', 'success');
            break;
        case 'export':
            // 导出数据
            showToast('数据导出中...', 'info');
            break;
    }
}

async function executeDocAction() {
    const title = document.getElementById('docTitle').value;
    const content = document.getElementById('docContent').value;
    const permission = document.getElementById('docPermission').value;
    
    closeModal();
    
    await callApi('/api/doc/documents', 'POST', {
        title,
        content: content,
        permission: permission
    });
    
    showToast('文档已创建', 'success');
}

async function executeCalendarAction() {
    const calendarId = document.getElementById('calendarId').value;
    const title = document.getElementById('eventTitle').value;
    const startTime = document.getElementById('startTime').value;
    const endTime = document.getElementById('endTime').value;
    
    closeModal();
    
    await callApi('/api/calendar/events', 'POST', {
        calendar_id: calendarId,
        title: title,
        start_time: startTime,
        end_time: endTime,
        description: "",
        attendees: []
    });
    
    showToast('日程已创建', 'success');
}

async function executeTaskAction() {
    const tasklistGuid = document.getElementById('tasklistGuid').value;
    const summary = document.getElementById('taskSummary').value;
    const description = document.getElementById('taskDescription').value;
    const dueTime = document.getElementById('taskDue').value;
    const assignee = document.getElementById('taskAssignee').value;
    
    closeModal();
    
    await callApi('/api/task/tasks', 'POST', {
        tasklist_guid: tasklistGuid,
        summary: summary,
        description: description,
        due_time: dueTime,
        assignee: assignee
    });
    
    showToast('任务已创建', 'success');
}

async function executeMessageAction() {
    const receiveId = document.getElementById('receiveId').value;
    const content = document.getElementById('messageContent').value;
    const receiveIdType = document.getElementById('receiveIdType').value;
    
    closeModal();
    
    await callApi('/api/message/send', 'POST', {
        receive_id: receiveId,
        content: content,
        receive_id_type: receiveIdType
    });
    
    showToast('消息已发送', 'success');
}

async function executeAIAction() {
    const model = document.getElementById('aiModelSelect').value;
    const type = document.getElementById('aiQueryType').value;
    const query = document.getElementById('aiQuery').value;
    
    closeModal();
    
    switch (type) {
        case 'nl_query':
            executeNLQuery();
            break;
        case 'data_clean':
            showToast('数据清洗功能需要上传数据文件', 'info');
            break;
        case 'recommend':
            getRecommendations();
            break;
    }
}

// 实用工具函数
function formatDate(date) {
    const d = new Date(date);
    return d.toLocaleString('zh-CN');
}

function formatNumber(num) {
    return num.toLocaleString('zh-CN');
}

// 导出功能
function exportData(data, filename) {
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename || 'data.json';
    a.click();
    URL.revokeObjectURL(url);
    showToast('文件已下载', 'success');
}

console.log('飞书Python工具箱 v2.0.0 前端已加载完成');
