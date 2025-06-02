// Test runner script for MOMS
const puppeteer = require('puppeteer');

async function runTests() {
    console.log('🧪 Starting MOMS Test Suite...\n');
    
    const browser = await puppeteer.launch({
        headless: true,
        args: ['--no-sandbox', '--disable-setuid-sandbox']
    });
    
    try {
        const page = await browser.newPage();
        
        // Capture console logs from the page
        page.on('console', msg => {
            const type = msg.type();
            const text = msg.text();
            
            if (type === 'error') {
                console.log(`❌ Browser Error: ${text}`);
            } else if (text.includes('Test:') || text.includes('PASS') || text.includes('FAIL')) {
                console.log(`📋 ${text}`);
            }
        });
        
        // Navigate to test suite
        console.log('📱 Loading test suite...');
        await page.goto('http://localhost:8000/test_suite.html', { 
            waitUntil: 'networkidle0',
            timeout: 30000 
        });
        
        // Wait for page to load completely
        await page.waitForTimeout(3000);
        
        console.log('🔧 Running server tests...');
        await page.click('button[onclick="testServers()"]');
        await page.waitForTimeout(2000);
        
        console.log('⚡ Running THREE.js tests...');
        await page.click('button[onclick="testThreeJS()"]');
        await page.waitForTimeout(2000);
        
        console.log('🎮 Running 3D viewer tests...');
        await page.click('button[onclick="test3DViewer()"]');
        await page.waitForTimeout(2000);
        
        console.log('🖥️ Running UI component tests...');
        await page.click('button[onclick="testUIComponents()"]');
        await page.waitForTimeout(2000);
        
        console.log('⚔️ Running combat analyzer tests...');
        await page.click('button[onclick="testCombatAnalyzer()"]');
        await page.waitForTimeout(2000);
        
        console.log('📦 Running archive tests...');
        await page.click('button[onclick="testArchives()"]');
        await page.waitForTimeout(2000);
        
        console.log('📊 Running performance tests...');
        await page.click('button[onclick="testPerformance()"]');
        await page.waitForTimeout(3000);
        
        // Get test results summary
        const summary = await page.evaluate(() => {
            const summaryDiv = document.getElementById('summary');
            return summaryDiv ? summaryDiv.innerText : 'No summary available';
        });
        
        console.log('\n📈 Test Results Summary:');
        console.log(summary);
        
        // Get detailed results
        const results = await page.evaluate(() => {
            const testResults = [];
            const resultDivs = document.querySelectorAll('.test-result');
            resultDivs.forEach(div => {
                const className = div.className;
                const text = div.innerText;
                const status = className.includes('pass') ? 'PASS' : 
                             className.includes('fail') ? 'FAIL' : 
                             className.includes('warn') ? 'WARN' : 'UNKNOWN';
                testResults.push({ status, text });
            });
            return testResults;
        });
        
        console.log('\n📝 Detailed Test Results:');
        let passCount = 0;
        let failCount = 0;
        let warnCount = 0;
        
        results.forEach(result => {
            const icon = result.status === 'PASS' ? '✅' : 
                        result.status === 'FAIL' ? '❌' : 
                        result.status === 'WARN' ? '⚠️' : '❓';
            console.log(`${icon} ${result.text}`);
            
            if (result.status === 'PASS') passCount++;
            else if (result.status === 'FAIL') failCount++;
            else if (result.status === 'WARN') warnCount++;
        });
        
        console.log(`\n📊 Final Results: ${passCount} passed, ${failCount} failed, ${warnCount} warnings`);
        
        if (failCount > 0) {
            console.log('\n🚨 Tests failed! Issues need to be fixed.');
            process.exit(1);
        } else {
            console.log('\n🎉 All tests passed!');
        }
        
    } catch (error) {
        console.error('❌ Test runner error:', error);
        process.exit(1);
    } finally {
        await browser.close();
    }
}

runTests().catch(console.error);