HTML_TEMPLATE = """
<!DOCTYPE html> 
<html lang="zh-CN"> 
<head> 
    <meta charset="UTF-8"> 
    <style> 
        * { box-sizing: border-box; margin: 0; padding: 0; font-family: 'Microsoft YaHei', sans-serif; } 
        body { display: flex; flex-direction: column; height: 100vh; background: #f0f2f5; } 
        .toolbar { display: flex; align-items: center; padding: 8px 15px; background: #fff; border-bottom: 1px solid #ddd; box-shadow: 0 2px 4px rgba(0,0,0,0.05); z-index: 10; } 
        .menu-container { position: relative; margin-right: 20px; } 
        .menu-btn { padding: 6px 12px; background: #4CAF50; color: white; border: none; border-radius: 4px; cursor: pointer; font-size: 14px; } 
        .menu-btn:hover { background: #45a049; } 
        .dropdown { display: none; position: absolute; top: 100%; left: 0; background: white; border: 1px solid #ccc; border-radius: 4px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); min-width: 150px; z-index: 100; } 
        .dropdown.show { display: block; } 
        .dropdown-item { padding: 10px 15px; cursor: pointer; font-size: 14px; color: #333; } 
        .dropdown-item:hover { background: #f5f5f5; } 
        .group-selector { margin-right: 20px; } 
        .group-selector select { padding: 6px 10px; border-radius: 4px; border: 1px solid #ccc; font-size: 14px; outline: none;} 
        .search-box { flex: 1; display: flex; align-items: center; background: #f5f5f5; border-radius: 20px; padding: 0 15px; max-width: 500px; } 
        .search-box input { flex: 1; border: none; background: transparent; padding: 8px 5px; font-size: 14px; outline: none; } 
        .variant-check { display: flex; align-items: center; margin-right: 15px; font-size: 13px; color: #555; cursor: pointer; white-space: nowrap; } 
        .variant-check input { margin-right: 5px; } 
        .main-container { display: flex; flex: 1; overflow: hidden; } 
        .sidebar { width: 280px; background: #fff; border-right: 1px solid #ddd; overflow-y: auto; padding: 10px; } 
        .content-area { flex: 1; background: #fff; display: flex; flex-direction: column; } 
        .result-item { padding: 8px 10px; border-bottom: 1px solid #f0f0f0; cursor: pointer; font-size: 14px; display: flex; justify-content: space-between; align-items: center; } 
        .result-item:hover { background: #f9f9f9; } 
        .result-item.active { background: #e8f0fe; color: #1a73e8; } 
        .result-meta { font-size: 11px; color: #888; white-space: nowrap; margin-left: 10px;} 
        iframe { flex: 1; border: none; width: 100%; } 
        .modal { display: none; position: fixed; top:0; left:0; right:0; bottom:0; background: rgba(0,0,0,0.5); z-index: 1000; justify-content: center; align-items: center; } 
        .modal-content { background: white; padding: 20px; border-radius: 8px; min-width: 300px; } 
        .modal input { width: 100%; padding: 8px; margin: 10px 0; border: 1px solid #ccc; border-radius: 4px; } 
        .modal button { margin-right: 10px; padding: 6px 15px; border: none; border-radius: 4px; cursor: pointer; } 
        .btn-primary { background: #4CAF50; color: white; } 
        .btn-danger { background: #f44336; color: white; } 
        .group-view { position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: #fff; z-index: 1000; display: none; flex-direction: column; } 
        .group-header { display: flex; align-items: center; padding: 15px 20px; background: #f8f9fa; border-bottom: 1px solid #dee2e6; } 
        .group-header h3 { margin-left: 20px; font-size: 16px; color: #333; } 
        .btn-back { background: #6c757d; color: white; border: none; border-radius: 4px; padding: 8px 15px; cursor: pointer; } 
        .btn-back:hover { background: #5a6268; } 
        .group-container { display: flex; flex: 1; overflow: hidden; } 
        .group-panel { width: 50%; display: flex; flex-direction: column; border-right: 1px solid #dee2e6; } 
        .group-panel:last-child { border-right: none; } 
        .group-panel-title { padding: 12px 15px; font-weight: bold; background: #f1f3f5; border-bottom: 1px solid #dee2e6; font-size: 14px; color: #495057; } 
        .group-controls { padding: 15px; display: flex; gap: 10px; border-bottom: 1px solid #dee2e6; background: #fafafa; align-items: center; } 
        .form-control { flex: 1; padding: 8px 12px; border: 1px solid #ced4da; border-radius: 4px; outline: none; font-size: 14px; } 
        .btn-sm { padding: 6px 12px; border: 1px solid #ced4da; border-radius: 4px; background: #fff; cursor: pointer; font-size: 14px; } 
        .btn-danger { background: #f44336; color: white; } 
        #allDictsList, #groupDictsList { list-style: none; padding: 0; margin: 0; overflow-y: auto; flex: 1; } 
        #allDictsList li, #groupDictsList li { padding: 10px 15px; border-bottom: 1px solid #f1f1f1; cursor: default; display: flex; justify-content: space-between; align-items: center; font-size: 14px; } 
        #allDictsList li:hover, #groupDictsList li:hover { background: #e9ecef; } 
        .btn-group { display: flex; gap: 4px; align-items: center; } 
        .action-btn { cursor: pointer; padding: 2px 6px; border-radius: 3px; font-size: 14px; user-select: none; font-family: sans-serif; } 
        .add-btn { color: #28a745; font-weight: bold; font-size: 20px; line-height: 1; } 
        .add-btn:hover { background: #e6f4ea; } 
        .sort-btn { color: #5f6368; background: #f1f3f4; border-radius: 4px; } 
        .sort-btn:hover { background: #e8eaed; } 
        .remove-btn { color: #dc3545; font-weight: bold; cursor: pointer; padding: 0 5px; font-size: 16px; } 
        .remove-btn:hover { color: #a71d2a; } 
        .dict-excluded span:first-child { color: #999; font-style: italic; } 
    </style> 
</head> 
<body> 
    <div class="toolbar"> 
        <div class="menu-container"> 
            <button class="menu-btn" onclick="toggleMenu('fileMenu')">打开词典 ▼</button> 
            <div id="fileMenu" class="dropdown"> 
                <div class="dropdown-item" onclick="pywebview.api.open_file()">打开文件</div> 
                <div class="dropdown-item" onclick="pywebview.api.open_folder()">打开文件夹</div> 
            </div> 
        </div> 
        <button class="menu-btn" style="background: #2196F3;" onclick="showGroupView()">词典分组</button> 
        <select class="group-selector" id="groupSelect" onchange="pywebview.api.switch_group(this.value)"></select> 
        <label class="variant-check"> 
            <input type="checkbox" id="variantCheck" checked> 异体字搜索 
        </label> 
        <div class="search-box"> 
            <input type="text" id="searchInput" placeholder="请先在上方选择分组，再输入关键词搜索..." onkeyup="handleSearch(event)"> 
        </div> 
    </div> 
    <div class="main-container"> 
        <div class="sidebar"> 
            <div id="resultList"></div> 
        </div> 
        <div class="content-area"> 
            <div id="contentArea" style="flex:1; overflow-y: auto; background: #fff; padding: 10px; scrollbar-gutter: stable;"></div> 
        </div> 
    </div> 
    <div id="groupView" class="group-view"> 
        <div class="group-header"> 
            <button class="btn-back" onclick="showMainView()">← 返回主界面</button> 
            <h3>词典分组管理</h3> 
        </div> 
        <div class="group-container"> 
            <div class="group-panel"> 
                <div class="group-panel-title">全部词典 (双击查看详情)</div> 
                <ul id="allDictsList"></ul> 
            </div> 
            <div class="group-panel"> 
                <div class="group-controls"> 
                    <select id="groupSelectGroupView" class="form-control" onchange="pywebview.api.switch_group(this.value)"></select> 
                    <button class="btn-sm" onclick="showAddGroupModal()">新建分组</button> 
                    <button class="btn-sm btn-danger" onclick="deleteCurrentGroup()">删除分组</button> 
                </div> 
                <div class="group-panel-title">当前分组词典 (点击 ✕ 移除)</div> 
                <ul id="groupDictsList"></ul> 
            </div> 
        </div> 
    </div> 
    <div id="dictInfoModal" class="modal" style="z-index: 1001;"> 
        <div class="modal-content" style="min-width: 400px;"> 
            <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:15px;"> 
                <h3 id="dictInfoTitle" style="margin:0;">词典信息</h3> 
                <span style="cursor:pointer;font-size:24px;color:#aaa;" onclick="closeDictInfo()">&times;</span> 
            </div> 
            <div id="dictInfoBody" style="line-height:1.6; font-size:14px;"></div> 
        </div> 
    </div> 
    <div class="modal" id="addGroupModal"> 
        <div class="modal-content"> 
            <h3>添加新分组</h3> 
            <input type="text" id="newGroupName" placeholder="请输入分组名称"> 
            <button class="btn-primary" onclick="confirmAddGroup()">确定</button> 
            <button onclick="closeModals()">取消</button> 
        </div> 
    </div> 
    <script> 
        let currentDictId = null; 
        function toggleMenu(id) { 
            document.querySelectorAll('.dropdown').forEach(el => { 
                if(el.id !== id) el.classList.remove('show'); 
            }); 
            document.getElementById(id).classList.toggle('show'); 
        } 
        document.addEventListener('click', (e) => { 
            if (!e.target.closest('.menu-container')) document.querySelectorAll('.dropdown').forEach(el => el.classList.remove('show')); 
        }); 
        function handleSearch(e) { 
            if (e.key === 'Enter') { 
                const keyword = document.getElementById('searchInput').value.trim(); 
                const use_variants = document.getElementById('variantCheck').checked; 
                if(keyword) pywebview.api.search(keyword, use_variants); 
            } 
        } 
        function updateUI(data) { 
            const optHtml = data.groups.map(g => `<option value="${g.name}"${g.name === data.current ? 'selected' : ''}>${g.name}</option>`).join(''); 
            document.getElementById('groupSelect').innerHTML = optHtml; 
            document.getElementById('groupSelectGroupView').innerHTML = optHtml; 
        } 
        function updateResults(results) { 
            document.getElementById('resultList').innerHTML = results.map((r, i) => { 
                const count = r.sources.length; 
                return `<div class="result-item" onclick="showEntry(${i})"> 
                    <span style="overflow:hidden;text-overflow:ellipsis;white-space:nowrap;">${r.key}</span> 
                    <span class="result-meta">${count}</span> 
                </div>`; 
            }).join(''); 
        } 
        function setContent(dictDataArray) { 
            const container = document.getElementById('contentArea'); 
            container.innerHTML = ''; 
            window.removeEventListener('message', this._iframeMessageHandler); 
            this._iframeMessageHandler = function(event) { 
                if (event.data && event.data.type === 'resize') { 
                    const iframe = document.getElementById(event.data.id); 
                    if (iframe) iframe.style.height = (event.data.height + 30) + 'px'; 
                } 
            }; 
            window.addEventListener('message', this._iframeMessageHandler); 
            dictDataArray.forEach((item, index) => { 
                const details = document.createElement('details'); 
                details.className = 'dict-block'; 
                if (index === 0) details.open = true; 
                const summary = document.createElement('summary'); 
                summary.className = 'dict-summary'; 
                summary.innerText = `📖 ${item.dict_name}`; 
                details.appendChild(summary); 
                const iframeWrapper = document.createElement('div'); 
                iframeWrapper.style.cssText = 'padding: 0; margin: 0;'; 
                const iframe = document.createElement('iframe'); 
                const iframeId = `dict-iframe-${index}`; 
                iframe.id = iframeId; 
                iframe.style.cssText = 'width: 100%; border: none; height: 0px; overflow: hidden !important;'; 
                iframe.setAttribute('frameborder', '0'); 
                iframe.setAttribute('scrolling', 'no'); 
                iframe.srcdoc = item.html; 
                iframeWrapper.appendChild(iframe); 
                details.appendChild(iframeWrapper); 
                details.addEventListener('toggle', function() { 
                    if (details.open) setTimeout(function() { 
                        iframe.contentWindow.postMessage('calcHeight', '*'); 
                    }, 100); 
                }); 
                container.appendChild(details); 
            }); 
        } 
        function showEntry(index) { 
            document.querySelectorAll('.result-item').forEach(el => el.classList.remove('active')); 
            document.querySelectorAll('.result-item')[index].classList.add('active'); 
            pywebview.api.show_entry(index); 
        } 
        function showGroupView() { 
            document.getElementById('groupView').style.display = 'flex'; 
            pywebview.api.init_group_view(); 
        } 
        function showMainView() { 
            document.getElementById('groupView').style.display = 'none'; 
        } 
        function renderGroupView(allDicts, groups, currentGroup) { 
            // === 修复：确保分组下拉框正确渲染 === 
            const optHtml = groups.map(g => `<option value="${g.name}"${g.name === currentGroup ? 'selected' : ''}>${g.name}</option>`).join(''); 
            document.getElementById('groupSelect').innerHTML = optHtml; 
            document.getElementById('groupSelectGroupView').innerHTML = optHtml; 
            const currentGroupData = groups.find(g => g.name === currentGroup); 
            
            // ===== 渲染左侧：全部词典 ===== 
            const allList = document.getElementById('allDictsList'); 
            allList.innerHTML = ''; 
            allDicts.forEach(d => { 
                if (d.status === 'active') return; 
                const li = document.createElement('li'); 
                if (d.status === 'excluded') li.className = 'dict-excluded'; 
                
                const span = document.createElement('span'); 
                span.innerText = d.name; 
                span.style.flex = '1'; 
                span.ondblclick = () => pywebview.api.get_dict_info(d.id); 
                
                const btnGroup = document.createElement('div'); 
                btnGroup.className = 'btn-group'; 
                
                if (d.status === 'excluded') { 
                    const btn = document.createElement('span'); 
                    btn.innerText = '↻'; 
                    btn.className = 'action-btn sort-btn'; 
                    btn.title = '恢复并重新加载'; 
                    btn.onclick = (e) => { e.stopPropagation(); pywebview.api.reload_excluded_dict(d.id); }; 
                    btnGroup.appendChild(btn); 
                } else { 
                    const btn1 = document.createElement('span'); 
                    btn1.innerText = '✕'; 
                    btn1.className = 'action-btn remove-btn'; 
                    btn1.title = '排除并卸载'; 
                    btn1.style.marginRight = '6px'; 
                    btn1.onclick = (e) => { e.stopPropagation(); pywebview.api.exclude_dict(d.id); }; 
                    btnGroup.appendChild(btn1); 
                    
                    const btn2 = document.createElement('span'); 
                    btn2.innerText = '+'; 
                    btn2.className = 'action-btn add-btn'; 
                    btn2.title = '添加至分组'; 
                    btn2.onclick = (e) => { e.stopPropagation(); pywebview.api.add_dict_to_group(d.id); }; 
                    btnGroup.appendChild(btn2); 
                } 
                
                li.appendChild(span); 
                li.appendChild(btnGroup); 
                allList.appendChild(li); 
            }); 
            
            // ===== 渲染右侧：当前分组词典 ===== 
            const groupList = document.getElementById('groupDictsList'); 
            groupList.innerHTML = ''; 
            if (currentGroupData) { 
                currentGroupData.dicts.forEach(d => { 
                    const li = document.createElement('li'); 
                    const span = document.createElement('span'); 
                    span.innerText = d.name; 
                    span.style.flex = '1'; 
                    span.ondblclick = () => pywebview.api.get_dict_info(d.id); 
                    
                    const btnGroup = document.createElement('div'); 
                    btnGroup.className = 'btn-group'; 
                    [{text:'⤒',action:'top',title:'置顶'},{text:'↑',action:'up',title:'上移'},{text:'↓',action:'down',title:'下移'},{text:'⤓',action:'bottom',title:'置底'}].forEach(a => { 
                        const btn = document.createElement('span'); 
                        btn.innerText = a.text; 
                        btn.title = a.title; 
                        btn.className = 'action-btn sort-btn'; 
                        btn.onclick = (e) => { e.stopPropagation(); pywebview.api.move_dict(d.id, a.action); }; 
                        btnGroup.appendChild(btn); 
                    }); 
                    
                    const removeBtn = document.createElement('span'); 
                    removeBtn.innerText = '✕'; 
                    removeBtn.className = 'remove-btn'; 
                    removeBtn.title = '从分组移除'; 
                    removeBtn.onclick = (e) => { e.stopPropagation(); pywebview.api.remove_dict_from_group(d.id); }; 
                    btnGroup.appendChild(removeBtn); 
                    
                    li.appendChild(span); 
                    li.appendChild(btnGroup); 
                    groupList.appendChild(li); 
                }); 
            } 
        } 
        function showDictInfoModal(title, body) { 
            document.getElementById('dictInfoTitle').innerText = title; 
            document.getElementById('dictInfoBody').innerHTML = body; 
            document.getElementById('dictInfoModal').style.display = 'flex'; 
        } 
        function closeDictInfo() { 
            document.getElementById('dictInfoModal').style.display = 'none'; 
        } 
        function showAddGroupModal() { 
            document.getElementById('addGroupModal').style.display = 'flex'; 
            document.getElementById('newGroupName').focus(); 
        } 
        function closeModals() { 
            document.querySelectorAll('.modal').forEach(el => el.style.display = 'none'); 
        } 
        function confirmAddGroup() { 
            const name = document.getElementById('newGroupName').value.trim(); 
            if(name) { 
                pywebview.api.add_group(name); 
                closeModals(); 
                document.getElementById('newGroupName').value=''; 
            } 
        } 
        function deleteCurrentGroup() { 
            if(confirm('确定删除当前分组？')) pywebview.api.delete_group(); 
        } 
    </script> 
</body> 
</html>
"""