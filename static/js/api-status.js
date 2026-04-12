// API Status Dashboard - Checks health of NGOpen APIs
(function() {
    'use strict';

    const APIs = {
        usaspending: { name: 'USAspending', path: '/ngopen/usaspending/' },
        samer: { name: 'SAM Entity Registry', path: '/ngopen/samer/' },
        irs_ng: { name: 'IRS Nonprofits', path: '/ngopen/irs_ng/' },
        usp_cl: { name: 'Congress Legislators', path: '/ngopen/usp_cl/' },
        up_cdmaps: { name: 'Congressional Districts', path: '/ngopen/up_cdmaps/' }
    };

    const TIMEOUT_MS = 10000; // 10 second timeout
    const REFRESH_INTERVAL = 60000; // Auto-refresh every 60 seconds

    /**
     * Check the health of a single API endpoint
     * @param {string} apiKey - The API identifier
     * @returns {Promise<Object>} - Health status result
     */
    async function checkApiHealth(apiKey) {
        const api = APIs[apiKey];
        const startTime = performance.now();
        
        try {
            const controller = new AbortController();
            const timeoutId = setTimeout(() => controller.abort(), TIMEOUT_MS);
            
            // Try to fetch the root endpoint (returns OpenAPI spec)
            const response = await fetch(api.path, {
                method: 'GET',
                signal: controller.signal,
                headers: {
                    'Accept': 'application/json'
                }
            });
            
            clearTimeout(timeoutId);
            const endTime = performance.now();
            const responseTime = Math.round(endTime - startTime);
            
            if (response.ok) {
                return {
                    healthy: true,
                    responseTime: responseTime,
                    statusCode: response.status
                };
            } else {
                return {
                    healthy: false,
                    responseTime: responseTime,
                    statusCode: response.status,
                    error: `HTTP ${response.status}`
                };
            }
        } catch (error) {
            const endTime = performance.now();
            const responseTime = Math.round(endTime - startTime);
            
            if (error.name === 'AbortError') {
                return {
                    healthy: false,
                    responseTime: responseTime,
                    error: 'Timeout'
                };
            }
            
            return {
                healthy: false,
                responseTime: responseTime,
                error: error.message || 'Network Error'
            };
        }
    }

    /**
     * Update the UI for a single API status item
     * @param {string} apiKey - The API identifier
     * @param {Object} result - The health check result
     */
    function updateStatusItem(apiKey, result) {
        const item = document.querySelector(`.status-item[data-api="${apiKey}"]`);
        if (!item) return;

        // Remove loading state
        item.classList.remove('loading', 'healthy', 'unhealthy');
        item.classList.add(result.healthy ? 'healthy' : 'unhealthy');

        // Update status text and dot
        const statusText = item.querySelector('.status-text');
        const statusDot = item.querySelector('.status-dot');
        
        if (result.healthy) {
            statusText.textContent = 'Operational';
            statusDot.style.animation = 'none';
        } else {
            statusText.textContent = result.error || 'Unavailable';
            statusDot.style.animation = 'none';
        }

        // Update response time
        const responseTimeEl = item.querySelector('.response-time');
        responseTimeEl.textContent = `${result.responseTime} ms`;
    }

    /**
     * Update the last checked timestamp
     */
    function updateTimestamp() {
        const timestampEl = document.getElementById('last-updated');
        if (timestampEl) {
            const now = new Date();
            timestampEl.textContent = now.toLocaleTimeString();
        }
    }

    /**
     * Run health checks for all APIs
     */
    async function checkAllApis() {
        const refreshBtn = document.getElementById('refresh-status');
        if (refreshBtn) {
            refreshBtn.disabled = true;
            refreshBtn.textContent = 'Checking...';
        }

        // Reset all status items to loading state
        document.querySelectorAll('.status-item').forEach(item => {
            item.classList.remove('healthy', 'unhealthy');
            item.classList.add('loading');
            const statusText = item.querySelector('.status-text');
            if (statusText) statusText.textContent = 'Checking...';
            const dot = item.querySelector('.status-dot');
            if (dot) dot.style.animation = 'pulse 1.5s infinite';
        });

        // Check all APIs in parallel
        const checks = Object.keys(APIs).map(async (apiKey) => {
            const result = await checkApiHealth(apiKey);
            updateStatusItem(apiKey, result);
            return { apiKey, result };
        });

        await Promise.all(checks);
        updateTimestamp();

        if (refreshBtn) {
            refreshBtn.disabled = false;
            refreshBtn.textContent = 'Refresh';
        }
    }

    /**
     * Initialize the dashboard
     */
    function init() {
        // Check APIs on page load
        checkAllApis();

        // Set up refresh button
        const refreshBtn = document.getElementById('refresh-status');
        if (refreshBtn) {
            refreshBtn.addEventListener('click', checkAllApis);
        }

        // Auto-refresh every 60 seconds
        setInterval(checkAllApis, REFRESH_INTERVAL);
    }

    // Initialize when DOM is ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }
})();
