/**
 * 微信公众号文章排版发布工具 - 前端脚本
 */

// ==================== 初始化 ====================

document.addEventListener('DOMContentLoaded', function() {
    initUploadArea();
    initTheme();
    loadConfig();
});

// ==================== 主题切换 ====================

function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const themeIcon = document.getElementById('theme-icon');
    
    if (savedTheme === 'dark') {
        document.body.classList.add('dark-theme');
        if (themeIcon) themeIcon.textContent = '☀️';
    }
}

function toggleTheme() {
    const body = document.body;
    const themeIcon = document.getElementById('theme-icon');
    
    if (body.classList.contains('dark-theme')) {
        body.classList.remove('dark-theme');
        if (themeIcon) themeIcon.textContent = '🌙';
        localStorage.setItem('theme', 'light');
    } else {
        body.classList.add('dark-theme');
        if (themeIcon) themeIcon.textContent = '☀️';
        localStorage.setItem('theme', 'dark');
    }
}

// ==================== 文件上传 ====================

function initUploadArea() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('file-input');
    
    if (!uploadArea || !fileInput) return;
    
    // 点击上传
    uploadArea.addEventListener('click', () => fileInput.click());
    
    // 文件选择
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length > 0) {
            handleFileUpload(e.target.files[0]);
        }
    });
    
    // 拖拽上传
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('dragover');
    });
    
    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('dragover');
    });
    
    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('dragover');
        
        if (e.dataTransfer.files.length > 0) {
            handleFileUpload(e.dataTransfer.files[0]);
        }
    });
}

async function handleFileUpload(file) {
    const allowedTypes = ['docx', 'md', 'txt'];
    const ext = file.name.split('.').pop().toLowerCase();
    
    if (!allowedTypes.includes(ext)) {
        showToast('❌ 不支持的文件格式');
        return;
    }
    
    const formData = new FormData();
    formData.append('file', file);
    
    // 显示进度
    const progressDiv = document.getElementById('upload-progress');
    const progressFill = document.getElementById('progress-fill');
    const progressText = document.getElementById('progress-text');
    
    progressDiv.style.display = 'block';
    progressFill.style.width = '0%';
    progressText.textContent = '上传中...';
    
    addLog('info', `正在上传文件: ${file.name}`);
    
    try {
        // 模拟进度
        let progress = 0;
        const progressInterval = setInterval(() => {
            progress += 10;
            if (progress <= 90) {
                progressFill.style.width = progress + '%';
            }
        }, 100);
        
        const response = await fetch('/api/upload', {
            method: 'POST',
            body: formData
        });
        
        clearInterval(progressInterval);
        progressFill.style.width = '100%';
        
        const result = await response.json();
        
        if (result.success) {
            progressText.textContent = '上传成功！';
            addLog('success', `文件解析成功: ${result.data.title}`);
            
            // 填充编辑器
            document.getElementById('article-title').value = result.data.title;
            document.getElementById('article-content').value = result.data.content;
            
            showToast('✅ 文件上传成功');
        } else {
            progressText.textContent = '上传失败';
            addLog('error', result.message);
            showToast('❌ ' + result.message);
        }
        
        // 3秒后隐藏进度条
        setTimeout(() => {
            progressDiv.style.display = 'none';
        }, 3000);
        
    } catch (error) {
        progressDiv.style.display = 'none';
        addLog('error', '上传失败: ' + error.message);
        showToast('❌ 上传失败');
    }
}

// ==================== 文章排版 ====================

async function formatArticle() {
    const title = document.getElementById('article-title').value.trim();
    const content = document.getElementById('article-content').value.trim();
    const style = document.querySelector('input[name="style"]:checked')?.value || 'simple';
    
    if (!content) {
        showToast('❌ 请输入文章内容');
        return;
    }
    
    addLog('info', '正在排版文章...');
    
    try {
        const response = await fetch('/api/format', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                title: title || '未命名文章',
                content: content,
                style: style
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            addLog('success', '排版完成，正在打开预览...');
            
            // 打开预览页面
            const previewUrl = `/preview?title=${encodeURIComponent(result.data.title)}&html=${encodeURIComponent(result.data.html)}`;
            window.open(previewUrl, '_blank');
            
            showToast('✅ 排版成功，已打开预览');
        } else {
            addLog('error', result.message);
            showToast('❌ ' + result.message);
        }
        
    } catch (error) {
        addLog('error', '排版失败: ' + error.message);
        showToast('❌ 排版失败');
    }
}

// ==================== 配置管理 ====================

async function loadConfig() {
    try {
        const response = await fetch('/api/config');
        const result = await response.json();
        
        if (result.success && result.data) {
            if (result.data.appid) {
                document.getElementById('config-appid').value = result.data.appid;
            }
            if (result.data.appsecret) {
                document.getElementById('config-appsecret').value = result.data.appsecret;
            }
            if (result.data.default_style) {
                const radio = document.querySelector(`input[name="style"][value="${result.data.default_style}"]`);
                if (radio) radio.checked = true;
            }
        }
    } catch (error) {
        console.error('加载配置失败:', error);
    }
}

function showConfigModal() {
    document.getElementById('config-modal').classList.add('show');
    loadConfig();
}

function closeConfigModal() {
    document.getElementById('config-modal').classList.remove('show');
}

async function saveConfig() {
    const appid = document.getElementById('config-appid').value.trim();
    const appsecret = document.getElementById('config-appsecret').value.trim();
    const style = document.querySelector('input[name="style"]:checked')?.value || 'simple';
    
    if (!appid || !appsecret) {
        showToast('❌ 请填写完整的凭证信息');
        return;
    }
    
    addLog('info', '正在保存配置...');
    
    try {
        const response = await fetch('/api/config', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                appid: appid,
                appsecret: appsecret,
                default_style: style
            })
        });
        
        const result = await response.json();
        
        if (result.success) {
            addLog('success', '配置已保存');
            showToast('✅ 配置保存成功');
            closeConfigModal();
        } else {
            addLog('error', result.message);
            showToast('❌ ' + result.message);
        }
        
    } catch (error) {
        addLog('error', '保存配置失败: ' + error.message);
        showToast('❌ 保存配置失败');
    }
}

// ==================== 日志管理 ====================

function addLog(type, message) {
    const logContainer = document.getElementById('log-container');
    if (!logContainer) return;
    
    const time = new Date().toLocaleTimeString('zh-CN', { hour12: false });
    
    const logEntry = document.createElement('div');
    logEntry.className = `log-entry log-${type}`;
    logEntry.innerHTML = `
        <span class="log-time">${time}</span>
        <span class="log-message">${message}</span>
    `;
    
    logContainer.appendChild(logEntry);
    logContainer.scrollTop = logContainer.scrollHeight;
}

function clearLogs() {
    const logContainer = document.getElementById('log-container');
    if (!logContainer) return;
    
    logContainer.innerHTML = `
        <div class="log-entry log-info">
            <span class="log-time">--:--:--</span>
            <span class="log-message">日志已清空</span>
        </div>
    `;
}

// ==================== Toast 提示 ====================

function showToast(message) {
    const toast = document.getElementById('toast');
    if (!toast) return;
    
    toast.textContent = message;
    toast.className = 'toast show';
    
    setTimeout(() => {
        toast.className = 'toast';
    }, 3000);
}

// ==================== 点击模态框外部关闭 ====================

document.addEventListener('click', function(e) {
    const modal = document.getElementById('config-modal');
    if (e.target === modal) {
        closeConfigModal();
    }
});

// ESC 键关闭模态框
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeConfigModal();
    }
});
