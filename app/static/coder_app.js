document.addEventListener('DOMContentLoaded', () => {
    // Current application state (1 = buggy, 2 = fixed)
    let currentVersion = 1;

    // Thread Memory State & Elements
    let threadId = localStorage.getItem('shopbot_thread_id');
    const threadIdDisplay = document.getElementById('thread-id-val');
    const copyThreadBtn = document.getElementById('copy-thread-btn');
    const resetSessionBtn = document.getElementById('reset-session-btn');

    // Initialize Thread ID
    if (!threadId) {
        generateNewThread();
    } else {
        updateThreadDisplay();
    }

    function generateNewThread() {
        threadId = 'session-' + Math.random().toString(36).substring(2, 10) + Math.random().toString(36).substring(2, 6);
        localStorage.setItem('shopbot_thread_id', threadId);
        updateThreadDisplay();
    }

    function updateThreadDisplay() {
        if (threadIdDisplay) {
            threadIdDisplay.textContent = threadId;
        }
    }

    // Copy Thread ID
    if (copyThreadBtn) {
        copyThreadBtn.addEventListener('click', () => {
            navigator.clipboard.writeText(threadId).then(() => {
                const originalHTML = copyThreadBtn.innerHTML;
                copyThreadBtn.innerHTML = '<i data-lucide="check" style="color: var(--accent-order)"></i>';
                lucide.createIcons();
                setTimeout(() => {
                    copyThreadBtn.innerHTML = originalHTML;
                    lucide.createIcons();
                }, 2000);
            });
        });
    }

    // Elements
    const toggleRightPanelBtn = document.getElementById('toggle-right-panel');
    const rightPanel = document.getElementById('right-panel');
    const mainWorkspace = document.querySelector('.main-workspace');
    
    const chatContainer = document.getElementById('chat-container');
    const dynamicFlowContainer = document.getElementById('dynamic-simulation-flow');
    const promptForm = document.getElementById('prompt-form');
    const promptInput = document.getElementById('prompt-input');
    
    // Side Drawer Elements
    const manualTestBtn = document.getElementById('btn-manual-test');
    const drawerOverlay = document.getElementById('manual-test-drawer-overlay');
    const sideDrawer = document.getElementById('manual-test-drawer');
    const closeDrawerBtn = document.getElementById('close-drawer-btn');
    const runManualTestBtn = document.getElementById('run-manual-test-btn');
    const clearManualTestBtn = document.getElementById('clear-manual-test-btn');
    const manualInput = document.getElementById('manual-input');
    const manualExpected = document.getElementById('manual-expected');
    const manualResultCard = document.getElementById('manual-result-card');
    const manualOutputVal = document.getElementById('manual-output-val');
    const manualStatusBadge = document.getElementById('manual-status-badge');
    const manualFailDetails = document.getElementById('manual-fail-details');
    const manualFailExpected = document.getElementById('manual-fail-expected');
    const manualFailActual = document.getElementById('manual-fail-actual');
    const manualFailReason = document.getElementById('manual-fail-reason');
    const manualDrawerFixBtn = document.getElementById('manual-drawer-fix-btn');

    // Right Sidebar / Timeline Elements
    const terminalDisplay = document.getElementById('terminal-display');
    const versionNode1 = document.getElementById('version-node-1');
    const versionNode2 = document.getElementById('version-node-2');

    // Initialize Icons
    lucide.createIcons();

    // 1. Right Sidebar Collapse Toggle
    toggleRightPanelBtn.addEventListener('click', () => {
        rightPanel.classList.toggle('collapsed');
        lucide.createIcons();
    });

    // 1.2 Left Sidebar Collapse Toggle
    const toggleLeftPanelBtn = document.getElementById('toggle-left-panel');
    const leftPanel = document.querySelector('.sidebar-left');
    toggleLeftPanelBtn.addEventListener('click', () => {
        leftPanel.classList.toggle('collapsed');
        const iconName = leftPanel.classList.contains('collapsed') ? 'layout-sidebar' : 'layout-sidebar-open';
        toggleLeftPanelBtn.innerHTML = `<i data-lucide="${iconName}"></i>`;
        lucide.createIcons();
    });

    // 2. Expand/Collapse Code Block
    const collapseCodeBtn = document.getElementById('collapse-code-btn');
    const codeBody1 = document.getElementById('code-body-1');
    collapseCodeBtn.addEventListener('click', () => {
        codeBody1.classList.toggle('collapsed');
        if (codeBody1.classList.contains('collapsed')) {
            collapseCodeBtn.innerHTML = '<i data-lucide="chevrons-up-down"></i> Expand';
        } else {
            collapseCodeBtn.innerHTML = '<i data-lucide="chevrons-down-up"></i> Collapse';
        }
        lucide.createIcons();
    });

    // 3. Side Drawer Actions (Manual Test Drawer)
    function openDrawer() {
        sideDrawer.classList.add('open');
        drawerOverlay.classList.add('open');
    }

    function closeDrawer() {
        sideDrawer.classList.remove('open');
        drawerOverlay.classList.remove('open');
    }

    manualTestBtn.addEventListener('click', openDrawer);
    closeDrawerBtn.addEventListener('click', closeDrawer);
    drawerOverlay.addEventListener('click', closeDrawer);

    // Clear Manual Test
    clearManualTestBtn.addEventListener('click', () => {
        manualInput.value = '';
        manualExpected.value = '';
        manualResultCard.style.display = 'none';
        manualFailDetails.style.display = 'none';
    });

    // Run Manual Test Simulation
    runManualTestBtn.addEventListener('click', () => {
        const inputVal = manualInput.value.trim();
        if (!inputVal) {
            alert('Please enter a string to test.');
            return;
        }

        const expectedVal = manualExpected.value.trim().toLowerCase();
        
        // Simulating the Java palindrome check based on current active version
        let actualResult = false;
        
        if (currentVersion === 1) {
            // Version 1 bug: always returns true!
            actualResult = true;
        } else {
            // Version 2: correctly checks if palindrome
            const cleanStr = inputVal.toLowerCase().replace(/[^a-z0-9]/g, '');
            const reversedStr = cleanStr.split('').reverse().join('');
            actualResult = (cleanStr === reversedStr);
        }

        // Display Output
        manualOutputVal.textContent = actualResult.toString().toUpperCase();
        manualResultCard.style.display = 'block';

        // Check against Expected Output if provided
        if (expectedVal) {
            const expectedBool = (expectedVal === 'true' || expectedVal === 'yes' || expectedVal === 'pass');
            const pass = (actualResult === expectedBool);

            if (pass) {
                manualStatusBadge.textContent = 'PASS';
                manualStatusBadge.className = 'status-badge-coder pass';
                manualFailDetails.style.display = 'none';
            } else {
                manualStatusBadge.textContent = 'FAIL';
                manualStatusBadge.className = 'status-badge-coder fail';
                
                manualFailExpected.textContent = expectedBool.toString();
                manualFailActual.textContent = actualResult.toString();
                
                if (currentVersion === 1) {
                    manualFailReason.textContent = "Reason: Version 1 of Palindrome.java contains a bug and returns 'true' for non-palindrome strings.";
                    manualFailDetails.style.display = 'block';
                } else {
                    manualFailReason.textContent = "Reason: Output mismatch.";
                    manualFailDetails.style.display = 'block';
                }
            }
        } else {
            // No expected input, just show output status as INFO
            manualStatusBadge.textContent = 'EXECUTED';
            manualStatusBadge.className = 'status-badge-coder pass';
            manualFailDetails.style.display = 'none';
        }
    });

    // Fix Program button inside drawer
    manualDrawerFixBtn.addEventListener('click', () => {
        closeDrawer();
        // Trigger auto test flow first as it is required to reach auto fix
        triggerAutoTestFlow();
    });


    // 4. AUTO TEST SIMULATION PIPELINE
    const runAutoTestsBtn = document.getElementById('btn-run-auto-tests');
    runAutoTestsBtn.addEventListener('click', triggerAutoTestFlow);

    function appendTerminalLine(text, type = '') {
        const line = document.createElement('div');
        line.className = 'terminal-line';
        if (type) line.innerHTML = `<span class="${type}">${text}</span>`;
        else line.textContent = text;
        terminalDisplay.appendChild(line);
        terminalDisplay.scrollTop = terminalDisplay.scrollHeight;
    }

    function triggerAutoTestFlow() {
        // Disable Run Tests button to prevent multiple triggers
        runAutoTestsBtn.disabled = true;

        // Clear dynamic workspace content
        dynamicFlowContainer.innerHTML = '';

        // 1. Appending auto-test progress skeleton card
        const progressCard = document.createElement('div');
        progressCard.className = 'progress-card';
        progressCard.innerHTML = `
            <div class="loader-list">
                <div class="loader-item active" id="load-step-1">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Thinking...</span>
                </div>
                <div class="loader-item" id="load-step-2">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Generating intelligent test cases...</span>
                </div>
                <div class="loader-item" id="load-step-3">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Compiling program...</span>
                </div>
                <div class="loader-item" id="load-step-4">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Executing tests...</span>
                </div>
            </div>
        `;
        dynamicFlowContainer.appendChild(progressCard);
        lucide.createIcons();
        scrollToBottom();

        // Terminal Update
        appendTerminalLine('Analyzing codebase structure...', 't-muted');

        // Progress Timer Sequence
        setTimeout(() => {
            completeProgressStep(1);
            startProgressStep(2);
            appendTerminalLine('Generated test suit config. Test cases defined.', 't-muted');
        }, 800);

        setTimeout(() => {
            completeProgressStep(2);
            startProgressStep(3);
            appendTerminalLine('Compiling Palindrome.java and PalindromeTest.java...', 't-muted');
        }, 1600);

        setTimeout(() => {
            completeProgressStep(3);
            startProgressStep(4);
            appendTerminalLine('Compilation Successful. Class paths generated.', 't-success');
        }, 2400);

        setTimeout(() => {
            completeProgressStep(4);
            // Delete progress card and show Test Cases screen
            progressCard.remove();
            showTestCasesCard();
        }, 3200);
    }

    function startProgressStep(stepNum) {
        const item = document.getElementById(`load-step-${stepNum}`);
        if (item) {
            item.classList.add('active');
        }
    }

    function completeProgressStep(stepNum) {
        const item = document.getElementById(`load-step-${stepNum}`);
        if (item) {
            item.classList.remove('active');
            item.classList.add('done');
            lucide.createIcons();
        }
    }

    // Step 2: Show Test Cases Card
    function showTestCasesCard() {
        const tcCard = document.createElement('div');
        tcCard.className = 'test-cases-card';
        tcCard.innerHTML = `
            <h3>Generated Test Cases</h3>
            <div class="test-grid">
                <div class="test-card">
                    <div class="test-card-info">
                        <span class="tc-input">Input: "madam"</span>
                        <span class="tc-expected">Expected: true</span>
                    </div>
                    <span class="test-status-ico font-mono">?</span>
                </div>
                <div class="test-card">
                    <div class="test-card-info">
                        <span class="tc-input">Input: "racecar"</span>
                        <span class="tc-expected">Expected: true</span>
                    </div>
                    <span class="test-status-ico font-mono">?</span>
                </div>
                <div class="test-card">
                    <div class="test-card-info">
                        <span class="tc-input">Input: "hello"</span>
                        <span class="tc-expected">Expected: false</span>
                    </div>
                    <span class="test-status-ico font-mono">?</span>
                </div>
                <div class="test-card">
                    <div class="test-card-info">
                        <span class="tc-input">Input: "noon"</span>
                        <span class="tc-expected">Expected: true</span>
                    </div>
                    <span class="test-status-ico font-mono">?</span>
                </div>
            </div>
            <button class="btn-execute-tests" id="execute-tests-btn">Execute Tests</button>
        `;
        dynamicFlowContainer.appendChild(tcCard);
        scrollToBottom();

        document.getElementById('execute-tests-btn').addEventListener('click', () => {
            tcCard.remove();
            runTestExecutionFlow();
        });
    }

    // Step 3: Run Test Execution Flow (Buggy V1 fails)
    function runTestExecutionFlow() {
        appendTerminalLine('Starting test suite executor...', 't-muted');
        appendTerminalLine('Running Tests...\n');

        // Append Execution Results Card with loading bars
        const resultsCard = document.createElement('div');
        resultsCard.className = 'execution-results-card';
        resultsCard.innerHTML = `
            <div class="progress-bar-container">
                <div class="progress-header">
                    <span>Executing Test Cases</span>
                    <span id="exec-progress-num">0 / 4 Passed</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" id="exec-bar-fill" style="width: 0%; background-color: var(--primary-color);"></div>
                </div>
            </div>
            <div class="test-grid" id="exec-test-grid">
                <!-- Executed cards go here dynamically -->
            </div>
        `;
        dynamicFlowContainer.appendChild(resultsCard);
        scrollToBottom();

        const grid = document.getElementById('exec-test-grid');
        const fill = document.getElementById('exec-bar-fill');
        const progressNum = document.getElementById('exec-progress-num');

        // Sequentially execute test cases
        setTimeout(() => {
            appendTerminalLine('PASS | Input: "madam" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "madam"', 'Expected: true', 'PASS', true));
            fill.style.width = '25%';
            progressNum.textContent = '1 / 4 Passed';
            scrollToBottom();
        }, 600);

        setTimeout(() => {
            appendTerminalLine('PASS | Input: "racecar" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "racecar"', 'Expected: true', 'PASS', true));
            fill.style.width = '50%';
            progressNum.textContent = '2 / 4 Passed';
            scrollToBottom();
        }, 1200);

        setTimeout(() => {
            appendTerminalLine('FAIL | Input: "hello" (Expected: false, Got: true)', 't-error');
            grid.appendChild(createTestExecCard('Input: "hello"', 'Expected: false (Got: true)', 'FAIL', false));
            fill.style.width = '75%';
            fill.style.backgroundColor = 'var(--error-color)';
            progressNum.textContent = '2 / 4 Passed';
            scrollToBottom();
        }, 1800);

        setTimeout(() => {
            appendTerminalLine('PASS | Input: "noon" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "noon"', 'Expected: true', 'PASS', true));
            progressNum.textContent = '3 / 4 Passed';
            scrollToBottom();

            // After execution finishes, show Failure Warning Panel
            showFailureWarningPanel();
        }, 2400);
    }

    function createTestExecCard(input, expected, status, isPass) {
        const card = document.createElement('div');
        card.className = `test-card ${isPass ? 'pass' : 'fail'}`;
        card.innerHTML = `
            <div class="test-card-info">
                <span class="tc-input">${input}</span>
                <span class="tc-expected">${expected}</span>
            </div>
            <span class="test-status-ico font-mono">${status === 'PASS' ? '✓' : '✗'}</span>
        `;
        return card;
    }

    // Step 4: Show Failure Warning Card
    function showFailureWarningPanel() {
        const failCard = document.createElement('div');
        failCard.className = 'warning-card';
        failCard.innerHTML = `
            <div class="warn-icon-wrapper">
                <i data-lucide="alert-triangle"></i>
            </div>
            <div class="warn-content">
                <h3>Test Failure Detected</h3>
                <p>Incorrect palindrome logic in <span class="bold-val">Palindrome.java</span>. The function returns <span class="bold-val">true</span> for non-palindrome strings because of a structural flaw.</p>
                <div class="warn-actions">
                    <button class="btn-warn btn-warn-primary" id="btn-auto-fix">
                        <i data-lucide="sparkles"></i> ✨ Auto Fix Code
                    </button>
                    <button class="btn-warn btn-warn-secondary">View Details</button>
                </div>
            </div>
        `;
        dynamicFlowContainer.appendChild(failCard);
        lucide.createIcons();
        scrollToBottom();

        document.getElementById('btn-auto-fix').addEventListener('click', () => {
            failCard.remove();
            runAutoFixFlow();
        });
    }

    // Step 5: Run Auto Fix (AI indicators, Version 2 code diff)
    function runAutoFixFlow() {
        const progressCard = document.createElement('div');
        progressCard.className = 'progress-card';
        progressCard.innerHTML = `
            <div class="loader-list">
                <div class="loader-item active" id="fix-step-1">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Analyzing failures...</span>
                </div>
                <div class="loader-item" id="fix-step-2">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Updating logic...</span>
                </div>
                <div class="loader-item" id="fix-step-3">
                    <div class="spinner"></div>
                    <i data-lucide="check-circle-2" class="loader-icon-done"></i>
                    <span>Optimizing implementation...</span>
                </div>
            </div>
        `;
        dynamicFlowContainer.appendChild(progressCard);
        lucide.createIcons();
        scrollToBottom();

        appendTerminalLine('Analyzing test logs for logic adjustments...', 't-warning');

        setTimeout(() => {
            completeFixStep(1);
            startFixStep(2);
            appendTerminalLine('Identified return bug on line 9 of Palindrome.java.', 't-warning');
        }, 1000);

        setTimeout(() => {
            completeFixStep(2);
            startFixStep(3);
            appendTerminalLine('Modifying palindrome mismatch exit condition. Writing Version 2...', 't-muted');
        }, 2000);

        setTimeout(() => {
            completeFixStep(3);
            progressCard.remove();
            showDiffComparisonCard();
        }, 3000);
    }

    function startFixStep(stepNum) {
        const item = document.getElementById(`fix-step-${stepNum}`);
        if (item) {
            item.classList.add('active');
        }
    }

    function completeFixStep(stepNum) {
        const item = document.getElementById(`fix-step-${stepNum}`);
        if (item) {
            item.classList.remove('active');
            item.classList.add('done');
            lucide.createIcons();
        }
    }

    // Step 6: Show Version 1 vs Version 2 Comparison Diff Card
    function showDiffComparisonCard() {
        // Update version history sidebar node
        versionNode2.classList.add('active');
        versionNode1.classList.remove('active');
        currentVersion = 2; // update state

        const diffCard = document.createElement('div');
        diffCard.className = 'diff-card';
        diffCard.innerHTML = `
            <div class="diff-header">
                <span>Code Comparison</span>
                <span class="card-meta">Version 1 vs Version 2</span>
            </div>
            <div class="diff-grid">
                <div class="diff-version-pane">
                    <div class="diff-pane-title">Version 1 (Original)</div>
                    <div class="diff-pane-code">
                        <span class="diff-line">public class Palindrome {</span>
                        <span class="diff-line">    public static boolean isPalindrome(String str) {</span>
                        <span class="diff-line">        if (str == null) return false;</span>
                        <span class="diff-line">        str = str.toLowerCase();</span>
                        <span class="diff-line del">-       return true; </span>
                        <span class="diff-line">    }</span>
                        <span class="diff-line">}</span>
                    </div>
                </div>
                <div class="diff-version-pane">
                    <div class="diff-pane-title">Version 2 (Fixed Condition)</div>
                    <div class="diff-pane-code">
                        <span class="diff-line">public class Palindrome {</span>
                        <span class="diff-line">    public static boolean isPalindrome(String str) {</span>
                        <span class="diff-line">        if (str == null) return false;</span>
                        <span class="diff-line">        str = str.toLowerCase();</span>
                        <span class="diff-line add">+       int n = str.length();</span>
                        <span class="diff-line add">+       for (int i = 0; i < n / 2; i++) {</span>
                        <span class="diff-line add">+           if (str.charAt(i) != str.charAt(n - 1 - i)) {</span>
                        <span class="diff-line add">+               return false;</span>
                        <span class="diff-line add">+           }</span>
                        <span class="diff-line add">+       }</span>
                        <span class="diff-line add">+       return true;</span>
                        <span class="diff-line">    }</span>
                        <span class="diff-line">}</span>
                    </div>
                </div>
            </div>
            <button class="btn-diff-run" id="btn-run-tests-again">Run Tests Again</button>
        `;
        dynamicFlowContainer.appendChild(diffCard);
        scrollToBottom();

        // Update main bubble V1 styling so it represents Version 2
        document.getElementById('code-body-1').querySelector('code').innerHTML = `public class Palindrome {
    public static boolean isPalindrome(String str) {
        if (str == null) return false;
        
        // Check letters (case-insensitive)
        str = str.toLowerCase();
        
        int n = str.length();
        for (int i = 0; i < n / 2; i++) {
            if (str.charAt(i) != str.charAt(n - 1 - i)) {
                return false; // Fixed!
            }
        }
        return true;
    }
}`;
        // Update metadata description of code block to v2
        const ascHeader = document.getElementById('assistant-bubble-v1').querySelector('.card-meta');
        ascHeader.textContent = 'Version 2';

        document.getElementById('btn-run-tests-again').addEventListener('click', () => {
            diffCard.remove();
            runSuccessTestsFlow();
        });
    }

    // Step 7: Run Fixed Tests (All Pass)
    function runSuccessTestsFlow() {
        appendTerminalLine('Compiling revised logic version 2...', 't-muted');
        appendTerminalLine('Compilation successful.', 't-success');
        appendTerminalLine('Executing tests with revised logic...\n');

        const resultsCard = document.createElement('div');
        resultsCard.className = 'execution-results-card';
        resultsCard.innerHTML = `
            <div class="progress-bar-container">
                <div class="progress-header">
                    <span>Executing Test Cases</span>
                    <span id="exec-progress-num">0 / 4 Passed</span>
                </div>
                <div class="bar-bg">
                    <div class="bar-fill" id="exec-bar-fill" style="width: 0%; background-color: var(--primary-color);"></div>
                </div>
            </div>
            <div class="test-grid" id="exec-test-grid"></div>
        `;
        dynamicFlowContainer.appendChild(resultsCard);
        scrollToBottom();

        const grid = document.getElementById('exec-test-grid');
        const fill = document.getElementById('exec-bar-fill');
        const progressNum = document.getElementById('exec-progress-num');

        // Sequence runs
        setTimeout(() => {
            appendTerminalLine('PASS | Input: "madam" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "madam"', 'Expected: true', 'PASS', true));
            fill.style.width = '25%';
            progressNum.textContent = '1 / 4 Passed';
            scrollToBottom();
        }, 400);

        setTimeout(() => {
            appendTerminalLine('PASS | Input: "racecar" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "racecar"', 'Expected: true', 'PASS', true));
            fill.style.width = '50%';
            progressNum.textContent = '2 / 4 Passed';
            scrollToBottom();
        }, 800);

        setTimeout(() => {
            appendTerminalLine('PASS | Input: "hello" (Expected: false, Got: false)', 't-success');
            grid.appendChild(createTestExecCard('Input: "hello"', 'Expected: false', 'PASS', true));
            fill.style.width = '75%';
            progressNum.textContent = '3 / 4 Passed';
            scrollToBottom();
        }, 1200);

        setTimeout(() => {
            appendTerminalLine('PASS | Input: "noon" (Expected: true, Got: true)', 't-success');
            grid.appendChild(createTestExecCard('Input: "noon"', 'Expected: true', 'PASS', true));
            fill.style.width = '100%';
            fill.style.backgroundColor = 'var(--success-color)';
            progressNum.textContent = '4 / 4 Passed';
            scrollToBottom();

            appendTerminalLine('\nALL TESTS PASSED SUCCESSFULLY.', 't-success');

            // Success panel display
            resultsCard.remove();
            showSuccessCard();
        }, 1600);
    }

    // Step 8: Success Card
    function showSuccessCard() {
        const successCard = document.createElement('div');
        successCard.className = 'success-panel-card';
        successCard.innerHTML = `
            <div class="success-header-wrapper">
                <div class="success-check-ico">
                    <i data-lucide="check"></i>
                </div>
                <div class="success-titles">
                    <h3>All Tests Passed</h3>
                    <p>Program verified against generated test suites successfully.</p>
                </div>
            </div>
            <div class="success-stats-grid">
                <div class="stat-item">
                    <span class="lbl">Test Coverage:</span>
                    <span class="val">100%</span>
                </div>
                <div class="stat-item">
                    <span class="lbl">Exec Time:</span>
                    <span class="val">14 ms</span>
                </div>
                <div class="stat-item">
                    <span class="lbl">Memory Usage:</span>
                    <span class="val">4.2 MB</span>
                </div>
                <div class="stat-item">
                    <span class="lbl">Exit Code:</span>
                    <span class="val font-mono">0</span>
                </div>
            </div>
            <div class="success-actions">
                <button class="btn-success-act btn-success-act-primary">Download Program</button>
                <button class="btn-success-act btn-success-act-secondary" id="btn-continue-chat">Continue Chat</button>
                <button class="btn-success-act btn-success-act-secondary">Generate Explanation</button>
            </div>
        `;
        dynamicFlowContainer.appendChild(successCard);
        lucide.createIcons();
        scrollToBottom();

        // Enable auto test button back
        runAutoTestsBtn.disabled = false;

        document.getElementById('btn-continue-chat').addEventListener('click', () => {
            chatInputFocusAndScroll();
        });
    }

    function chatInputFocusAndScroll() {
        promptInput.focus();
        scrollToBottom();
    }


    // 5. CHAT EXPERIENCE & SUGGESTED CHIPS
    // Suggestions
    document.querySelectorAll('.prompt-chip').forEach(chip => {
        chip.addEventListener('click', () => {
            const query = chip.getAttribute('data-query');
            submitQuery(query);
        });
    });

    promptForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const query = promptInput.value.trim();
        if (query) {
            submitQuery(query);
            promptInput.value = '';
        }
    });

    function submitQuery(text) {
        // Append user bubble
        appendChatBubble('user', text);
        scrollToBottom();

        // Simulated AI response
        setTimeout(() => {
            appendChatBubble('assistant-skeleton');
            scrollToBottom();
        }, 400);

        setTimeout(() => {
            // Remove skeleton and add response bubble
            const skeletons = chatContainer.querySelectorAll('.skeleton-bubble');
            skeletons.forEach(s => s.remove());
            
            let assistantReply = '';
            if (text.toLowerCase().includes('python')) {
                assistantReply = `Here is the optimized palindrome logic converted to **Python**:
                
\`\`\`python
def is_palindrome(text: str) -> bool:
    if text is None:
        return False
    clean_text = "".join(char.lower() for char in text if char.isalnum())
    return clean_text == clean_text[::-1]
\`\`\`
Let me know if you would like me to compile or generate unit tests for this python variant.`;
            } else if (text.toLowerCase().includes('explain')) {
                assistantReply = `Here is the line-by-line explanation of the solution:
                
1. **Case Conversion**: \`str = str.toLowerCase();\` ensures the comparison is case-insensitive.
2. **Loop Indexes**: The loop bounds \`i < n / 2\` check elements from opposite ends until they meet in the middle.
3. **Short-circuit Mismatch**: If characters don't match, we return \`false\` instantly, preventing redundant comparisons.
4. **Conclusion**: If the loop exits cleanly, the string is a valid palindrome, yielding \`true\`.`;
            } else {
                assistantReply = `I am ready to help. You asked: "${text}". I am simulating responses in this design mockup workspace. Click the action buttons on the Java Code block card above to see the full testing and auto-fixing workspace flows in action!`;
            }

            appendChatBubble('assistant', assistantReply);
            scrollToBottom();
        }, 1600);
    }

    function appendChatBubble(role, text) {
        const bubble = document.createElement('div');
        
        if (role === 'assistant-skeleton') {
            bubble.className = 'chat-bubble assistant-bubble skeleton-bubble';
            bubble.innerHTML = `
                <div class="bubble-avatar">🤖</div>
                <div class="bubble-content">
                    <div style="background: white; border: 1px solid var(--border-color); padding: 16px; border-radius: var(--radius-lg); width: 200px;">
                        <div style="height: 10px; background: #e2e8f0; border-radius: 4px; margin-bottom: 8px; animation: pulse 1.5s infinite;"></div>
                        <div style="height: 10px; background: #e2e8f0; border-radius: 4px; width: 60%; animation: pulse 1.5s infinite;"></div>
                    </div>
                </div>
            `;
            chatContainer.appendChild(bubble);
            return;
        }

        bubble.className = `chat-bubble ${role === 'user' ? 'user-bubble' : 'assistant-bubble'}`;
        const avatar = role === 'user' ? '👤' : '🤖';
        
        const content = role === 'user' ? `<p>${text}</p>` : `<div class="elegant-card" style="padding: 16px; font-size: 14.5px; line-height: 1.6; color: var(--text-secondary);">${parseMarkdown(text)}</div>`;
        
        bubble.innerHTML = `
            <div class="bubble-avatar">${avatar}</div>
            <div class="bubble-content">${content}</div>
        `;
        chatContainer.appendChild(bubble);
    }

    function parseMarkdown(mdText) {
        let escaped = mdText
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;");
        
        // Bold
        escaped = escaped.replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>');
        // Inline code
        escaped = escaped.replace(/`([^`]+)`/g, '<code>$1</code>');
        // Multiline code blocks
        escaped = escaped.replace(/```python([\s\S]*?)```/g, '<pre><code class="language-python">$1</code></pre>');
        
        return escaped.replace(/\n/g, '<br>');
    }

    function scrollToBottom() {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }

    // Reset Session / New Chat resets the container to its initial state and generates a new thread ID
    if (resetSessionBtn) {
        resetSessionBtn.addEventListener('click', () => {
            if (confirm('Are you sure you want to start a new session? This will clear your chat history.')) {
                generateNewThread();

                currentVersion = 1;
                
                // Reset code bubble HTML back to V1
                document.getElementById('code-body-1').querySelector('code').innerHTML = `public class Palindrome {
    public static boolean isPalindrome(String str) {
        if (str == null) return false;
        
        // Check letters (case-insensitive)
        str = str.toLowerCase();
        
        // Bug: It always returns true regardless of mismatches!
        return true; 
    }
}`;
                const ascHeader = document.getElementById('assistant-bubble-v1').querySelector('.card-meta');
                ascHeader.textContent = 'Version 1';
                
                // Reset sidebar version node highlight
                versionNode1.classList.add('active');
                versionNode2.classList.remove('active');

                // Reset terminal text
                terminalDisplay.innerHTML = `
                    <div class="terminal-line"><span class="t-success">Compiling...</span></div>
                    <div class="terminal-line">Compilation Successful.</div>
                    <div class="terminal-line"><span class="t-muted">Ready to run tests...</span></div>
                `;

                // Clear dynamic flows
                dynamicFlowContainer.innerHTML = '';
                
                // Remove additional chat bubbles
                const extraBubbles = chatContainer.querySelectorAll('.chat-bubble');
                extraBubbles.forEach((b, idx) => {
                    if (idx > 1) b.remove(); // keep only the first query and code generation response
                });

                runAutoTestsBtn.disabled = false;
                scrollToBottom();
            }
        });
    }
});

// Helper Copy Code
window.copyCode = function(ver) {
    const code = document.getElementById(`code-body-${ver}`).querySelector('code').innerText;
    navigator.clipboard.writeText(code).then(() => {
        alert('Code copied to clipboard!');
    });
};
