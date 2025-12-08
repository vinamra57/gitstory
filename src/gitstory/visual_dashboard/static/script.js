// GitStory Dashboard Visualizations and Interactions

// ============================================================================
// SIDEBAR AND SETTINGS FUNCTIONALITY
// ============================================================================

// Sidebar toggle and resize functionality
function initializeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const sidebarToggle = document.getElementById('sidebar-toggle');
    const sidebarMinimize = document.getElementById('sidebar-minimize');
    const sidebarOverlay = document.getElementById('sidebar-overlay');
    const sidebarResizer = document.getElementById('sidebar-resizer');
    const mainContent = document.querySelector('.main-content');

    let isResizing = false;

    // Toggle sidebar (mobile and minimized desktop)
    function openSidebar() {
        if (window.innerWidth >= 1200 && sidebar.classList.contains('minimized')) {
            // On desktop, if minimized, un-minimize it
            toggleMinimize();
        } else {
            // On mobile, open sidebar
            sidebar.classList.add('open');
            sidebarOverlay.classList.add('active');
        }
    }

    function closeSidebar() {
        sidebar.classList.remove('open');
        sidebarOverlay.classList.remove('active');
    }

    // Minimize/maximize sidebar (desktop)
    function toggleMinimize() {
        sidebar.classList.toggle('minimized');
        if (sidebar.classList.contains('minimized')) {
            mainContent.style.marginLeft = '0';
            if (sidebarToggle && window.innerWidth >= 1200) {
                sidebarToggle.style.display = 'block';
            }
            localStorage.setItem('gitstory-sidebar-minimized', 'true');
        } else {
            const width = localStorage.getItem('gitstory-sidebar-width') || '300';
            mainContent.style.marginLeft = `${width}px`;
            if (sidebarToggle && window.innerWidth >= 1200) {
                sidebarToggle.style.display = 'none';
            }
            localStorage.setItem('gitstory-sidebar-minimized', 'false');
        }
    }

    // Resize functionality
    function startResize(e) {
        isResizing = true;
        sidebar.classList.add('resizing');
        document.body.style.cursor = 'ew-resize';
        document.body.style.userSelect = 'none';
        e.preventDefault();
    }

    function resize(e) {
        if (!isResizing) return;
        e.preventDefault();

        const newWidth = e.clientX;

        if (newWidth >= 200 && newWidth <= 600) {
            sidebar.style.width = `${newWidth}px`;
            mainContent.style.marginLeft = `${newWidth}px`;
            localStorage.setItem('gitstory-sidebar-width', newWidth);
        }
    }

    function stopResize() {
        if (!isResizing) return;
        isResizing = false;
        sidebar.classList.remove('resizing');
        document.body.style.cursor = '';
        document.body.style.userSelect = '';
    }

    // Event listeners
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', openSidebar);
    }

    if (sidebarMinimize) {
        sidebarMinimize.addEventListener('click', toggleMinimize);
    }

    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', closeSidebar);
    }

    if (sidebarResizer) {
        sidebarResizer.addEventListener('mousedown', startResize);
        document.addEventListener('mousemove', resize);
        document.addEventListener('mouseup', stopResize);
    }

    // Restore saved sidebar state
    const savedWidth = localStorage.getItem('gitstory-sidebar-width');
    const savedMinimized = localStorage.getItem('gitstory-sidebar-minimized');

    if (savedWidth && window.innerWidth >= 1200) {
        sidebar.style.width = `${savedWidth}px`;
        mainContent.style.marginLeft = `${savedWidth}px`;
    }

    if (savedMinimized === 'true' && window.innerWidth >= 1200) {
        sidebar.classList.add('minimized');
        mainContent.style.marginLeft = '0';
        if (sidebarToggle) {
            sidebarToggle.style.display = 'block';
        }
    }

    // Close sidebar when clicking on a link (mobile)
    document.querySelectorAll('.sidebar-link, .sidebar-sublink').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth < 1200) {
                closeSidebar();
            }
        });
    });
}

// Theme switching functionality
function initializeThemeSwitcher() {
    const themeSelect = document.getElementById('theme-select');
    const savedTheme = localStorage.getItem('gitstory-theme') || 'light';

    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);
    themeSelect.value = savedTheme;

    themeSelect.addEventListener('change', (e) => {
        const theme = e.target.value;
        document.documentElement.setAttribute('data-theme', theme);
        localStorage.setItem('gitstory-theme', theme);
    });
}

// Font switching functionality
function initializeFontSwitcher() {
    const fontSelect = document.getElementById('font-select');
    const savedFont = localStorage.getItem('gitstory-font') || 'system';

    // Apply saved font
    document.body.className = document.body.className.replace(/font-\w+/g, '');
    document.body.classList.add(`font-${savedFont}`);
    fontSelect.value = savedFont;

    fontSelect.addEventListener('change', (e) => {
        const font = e.target.value;
        document.body.className = document.body.className.replace(/font-\w+/g, '');
        document.body.classList.add(`font-${font}`);
        localStorage.setItem('gitstory-font', font);
    });
}

// Add IDs to headings in AI summary for navigation
function addHeadingIds() {
    const aiSummaryContent = document.querySelector('.ai-summary-content');
    if (!aiSummaryContent) return;

    // Find all h2 and h3 headings in the AI summary
    const headings = aiSummaryContent.querySelectorAll('h2, h3');

    headings.forEach(heading => {
        const text = heading.textContent.trim();
        // Create an ID from the heading text
        const id = text.toLowerCase()
            .replace(/[^\w\s-]/g, '')
            .replace(/\s+/g, '-')
            .replace(/-+/g, '-');

        heading.id = id;
    });
}

// Smooth scrolling for sidebar links
function initializeSmoothScrolling() {
    document.querySelectorAll('.sidebar-link, .sidebar-sublink').forEach(link => {
        link.addEventListener('click', (e) => {
            e.preventDefault();
            const targetId = link.getAttribute('href').substring(1);
            const targetElement = document.getElementById(targetId);

            if (targetElement) {
                targetElement.scrollIntoView({ behavior: 'smooth', block: 'start' });

                // Update active link
                document.querySelectorAll('.sidebar-link, .sidebar-sublink').forEach(l => l.classList.remove('active'));
                link.classList.add('active');
            }
        });
    });
}

// Highlight active section in sidebar based on scroll position
function initializeActiveSection() {
    const sections = document.querySelectorAll('section[id], .ai-summary-content h2[id], .ai-summary-content h3[id]');
    const sidebarLinks = document.querySelectorAll('.sidebar-link, .sidebar-sublink');

    function updateActiveLink() {
        let currentSection = '';

        sections.forEach(section => {
            const sectionTop = section.offsetTop;

            if (window.scrollY >= sectionTop - 100) {
                currentSection = section.getAttribute('id');
            }
        });

        sidebarLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === `#${currentSection}`) {
                link.classList.add('active');
            }
        });
    }

    window.addEventListener('scroll', updateActiveLink);
    updateActiveLink(); // Call once on load
}

// Color schemes for the charts
const typeColors = {
    "feature": "#4CAF50",
    "bugfix": "#F44336",
    "refactor": "#2196F3",
    "docs": "#FF9800",
    "style": "#9C27B0",
    "test": "#00BCD4",
    "chore": "#795548",
    "other": "#9E9E9E"
};

// ============================================================================
// DATA PREPARATION FUNCTIONS
// ============================================================================

// Prepare data for commits by type pie chart
function prepareTypeData(byType) {
    return Object.entries(byType).map(([type, count]) => ({
        type: type,
        count: count
    }));
}

// Prepare data for commits by author pie chart
function prepareAuthorData(byAuthor) {
    return Object.entries(byAuthor).map(([author, data]) => ({
        author: author,
        count: data.count
    }));
}

// Prepare data for activity timeline
function prepareTimelineData(commits) {
    // Group commits by date
    const commitsByDate = {};
    const commitsByDateAndType = {};

    commits.forEach(commit => {
        const date = commit.timestamp.split('T')[0]; // Get just the date part
        const type = commit.type;

        // Count total commits by date
        if (!commitsByDate[date]) {
            commitsByDate[date] = 0;
        }
        commitsByDate[date]++;

        // Count commits by date and type
        const key = `${date}-${type}`;
        if (!commitsByDateAndType[key]) {
            commitsByDateAndType[key] = { date, type, count: 0 };
        }
        commitsByDateAndType[key].count++;
    });

    // Convert to array format for Vega-Lite
    return Object.values(commitsByDateAndType);
}


// ============================================================================
// VEGA-LITE CHART SPECIFICATIONS
// ============================================================================

// Commits by type pie chart
function createTypesPieChart(data) {
    // Calculate total for percentages
    const total = data.reduce((sum, item) => sum + item.count, 0);

    // Add percentage to data
    const dataWithPercentage = data.map(item => ({
        ...item,
        percentage: ((item.count / total) * 100).toFixed(1)
    }));

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Distribution of commits by type",
        "data": { "values": dataWithPercentage },
        "mark": {"type": "arc", "tooltip": true},
        "encoding": {
            "theta": { "field": "count", "type": "quantitative" },
            "color": {
                "field": "type",
                "type": "nominal",
                "scale": {
                    "domain": Object.keys(typeColors),
                    "range": Object.values(typeColors)
                },
                "legend": {"title": "Commit Type"}
            },
            "tooltip": [
                {"field": "type", "type": "nominal", "title": "Type"},
                {"field": "count", "type": "quantitative", "title": "Commits"},
                {"field": "percentage", "type": "nominal", "title": "Percentage", "format": ".1f"}
            ]
        },
        "width": 400,
        "height": 400
    };
}

// Commits by author pie chart
function createAuthorsPieChart(data) {
    // Calculate total for percentages
    const total = data.reduce((sum, item) => sum + item.count, 0);

    // Add percentage to data
    const dataWithPercentage = data.map(item => ({
        ...item,
        percentage: ((item.count / total) * 100).toFixed(1)
    }));

    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Distribution of commits by author",
        "data": { "values": dataWithPercentage },
        "mark": {"type": "arc", "tooltip": true},
        "encoding": {
            "theta": { "field": "count", "type": "quantitative" },
            "color": {
                "field": "author",
                "type": "nominal",
                "legend": {"title": "Author"}
            },
            "tooltip": [
                {"field": "author", "type": "nominal", "title": "Author"},
                {"field": "count", "type": "quantitative", "title": "Commits"},
                {"field": "percentage", "type": "nominal", "title": "Percentage", "format": ".1f"}
            ]
        },
        "width": 400,
        "height": 400
    };
}

// Activity timeline chart
function createTimelineChart(data) {
    return {
        "$schema": "https://vega.github.io/schema/vega-lite/v5.json",
        "description": "Commit activity over time",
        "data": { "values": data },
        "mark": {"type": "area", "interpolate": "monotone", "tooltip": true},
        "encoding": {
            "x": {
                "field": "date",
                "type": "temporal",
                "title": "Date",
                "axis": {"format": "%Y-%m-%d"}
            },
            "y": {
                "field": "count",
                "type": "quantitative",
                "title": "Number of Commits",
                "stack": true
            },
            "color": {
                "field": "type",
                "type": "nominal",
                "scale": {
                    "domain": Object.keys(typeColors),
                    "range": Object.values(typeColors)
                },
                "legend": {"title": "Commit Type"}
            },
            "tooltip": [
                {"field": "date", "type": "temporal", "title": "Date", "format": "%Y-%m-%d"},
                {"field": "type", "type": "nominal", "title": "Type"},
                {"field": "count", "type": "quantitative", "title": "Commits"}
            ]
        },
        "width": 800,
        "height": 300
    };
}


// ============================================================================
// INTERACTIVE TABLE FUNCTIONALITY
// ============================================================================

class CommitsTable {
    constructor(commits) {
        this.allCommits = commits;
        this.filteredCommits = commits;
        this.currentSort = { column: null, direction: 'asc' };

        this.initializeFilters();
        this.attachEventListeners();
    }

    initializeFilters() {
        // Populate author filter
        const authors = [...new Set(this.allCommits.map(c => c.author))].sort();
        const authorSelect = document.getElementById('filter-author');
        authors.forEach(author => {
            const option = document.createElement('option');
            option.value = author;
            option.textContent = author;
            authorSelect.appendChild(option);
        });

        // Populate type filter
        const types = [...new Set(this.allCommits.map(c => c.type))].sort();
        const typeSelect = document.getElementById('filter-type');
        types.forEach(type => {
            const option = document.createElement('option');
            option.value = type;
            option.textContent = type;
            typeSelect.appendChild(option);
        });

        // Set date range
        const dates = this.allCommits.map(c => new Date(c.timestamp)).sort((a, b) => a - b);
        if (dates.length > 0) {
            const startInput = document.getElementById('filter-date-start');
            const endInput = document.getElementById('filter-date-end');
            startInput.value = dates[0].toISOString().split('T')[0];
            endInput.value = dates[dates.length - 1].toISOString().split('T')[0];
        }
    }

    attachEventListeners() {
        // Filter change listeners
        document.getElementById('filter-author').addEventListener('change', () => this.applyFilters());
        document.getElementById('filter-type').addEventListener('change', () => this.applyFilters());
        document.getElementById('filter-date-start').addEventListener('change', () => this.applyFilters());
        document.getElementById('filter-date-end').addEventListener('change', () => this.applyFilters());

        // Reset button
        document.getElementById('reset-filters').addEventListener('click', () => this.resetFilters());

        // Sort headers
        document.querySelectorAll('th[data-sort]').forEach(header => {
            header.addEventListener('click', () => this.sortBy(header.dataset.sort));
        });
    }

    applyFilters() {
        const authorFilter = document.getElementById('filter-author').value;
        const typeFilter = document.getElementById('filter-type').value;
        const dateStart = new Date(document.getElementById('filter-date-start').value);
        const dateEnd = new Date(document.getElementById('filter-date-end').value);

        this.filteredCommits = this.allCommits.filter(commit => {
            const commitDate = new Date(commit.timestamp);

            const authorMatch = !authorFilter || commit.author === authorFilter;
            const typeMatch = !typeFilter || commit.type === typeFilter;
            const dateMatch = commitDate >= dateStart && commitDate <= dateEnd;

            return authorMatch && typeMatch && dateMatch;
        });

        this.updateTableDisplay();
    }

    resetFilters() {
        document.getElementById('filter-author').value = '';
        document.getElementById('filter-type').value = '';

        const dates = this.allCommits.map(c => new Date(c.timestamp)).sort((a, b) => a - b);
        if (dates.length > 0) {
            document.getElementById('filter-date-start').value = dates[0].toISOString().split('T')[0];
            document.getElementById('filter-date-end').value = dates[dates.length - 1].toISOString().split('T')[0];
        }

        this.filteredCommits = this.allCommits;
        this.updateTableDisplay();
    }

    sortBy(column) {
        // Toggle sort direction
        if (this.currentSort.column === column) {
            this.currentSort.direction = this.currentSort.direction === 'asc' ? 'desc' : 'asc';
        } else {
            this.currentSort.column = column;
            this.currentSort.direction = 'asc';
        }

        // Sort the filtered commits
        this.filteredCommits.sort((a, b) => {
            let aVal, bVal;

            switch(column) {
                case 'timestamp':
                    aVal = new Date(a.timestamp);
                    bVal = new Date(b.timestamp);
                    break;
                case 'files_changed':
                    aVal = a.files_changed || 0;
                    bVal = b.files_changed || 0;
                    break;
                case 'changes':
                    aVal = a.changes || 0;
                    bVal = b.changes || 0;
                    break;
                default:
                    aVal = a[column] || '';
                    bVal = b[column] || '';
            }

            if (aVal < bVal) return this.currentSort.direction === 'asc' ? -1 : 1;
            if (aVal > bVal) return this.currentSort.direction === 'asc' ? 1 : -1;
            return 0;
        });

        this.updateSortIndicators();
        this.updateTableDisplay();
    }

    updateSortIndicators() {
        // Clear all sort indicators
        document.querySelectorAll('th[data-sort]').forEach(header => {
            header.classList.remove('sort-asc', 'sort-desc');
        });

        // Add indicator to current sort column
        if (this.currentSort.column) {
            const header = document.querySelector(`th[data-sort="${this.currentSort.column}"]`);
            if (header) {
                header.classList.add(`sort-${this.currentSort.direction}`);
            }
        }
    }

    updateTableDisplay() {
        const tbody = document.getElementById('commits-tbody');
        const rows = Array.from(tbody.querySelectorAll('tr'));

        // Create a map of commit hash to filtered commits for quick lookup
        const filteredHashes = new Set(this.filteredCommits.map(c => c.hash));

        // Hide/show rows based on filter
        rows.forEach(row => {
            const hash = row.querySelector('td:first-child').textContent;
            if (filteredHashes.has(hash)) {
                row.classList.remove('filtered-out');
            } else {
                row.classList.add('filtered-out');
            }
        });

        // Reorder visible rows based on sort
        const visibleRows = rows.filter(row => !row.classList.contains('filtered-out'));
        const sortedHashes = this.filteredCommits.map(c => c.hash);

        visibleRows.sort((a, b) => {
            const aHash = a.querySelector('td:first-child').textContent;
            const bHash = b.querySelector('td:first-child').textContent;
            return sortedHashes.indexOf(aHash) - sortedHashes.indexOf(bHash);
        });

        // Re-append rows in sorted order
        visibleRows.forEach(row => tbody.appendChild(row));

        // Update count display
        document.getElementById('showing-count').textContent =
            `Showing ${this.filteredCommits.length} of ${this.allCommits.length} commits`;
    }
}

// ============================================================================
// INITIALIZATION
// ============================================================================

document.addEventListener('DOMContentLoaded', function() {
    // Initialize sidebar and settings
    initializeSidebar();
    initializeThemeSwitcher();
    initializeFontSwitcher();
    addHeadingIds();
    initializeSmoothScrolling();
    initializeActiveSection();

    // Check if data is available
    if (typeof statsData === 'undefined' || typeof commitsData === 'undefined') {
        console.error('Stats data or commits data not available for visualizations');
        return;
    }

    // Render pie charts
    const typeData = prepareTypeData(statsData.byType);
    const typeSpec = createTypesPieChart(typeData);
    vegaEmbed('#viz-by-type', typeSpec, {
        actions: { export: true, source: false, compiled: false, editor: false }
    }).catch(console.error);

    const authorData = prepareAuthorData(statsData.byAuthor);
    const authorSpec = createAuthorsPieChart(authorData);
    vegaEmbed('#viz-by-author', authorSpec, {
        actions: { export: true, source: false, compiled: false, editor: false }
    }).catch(console.error);

    // Render activity timeline
    const timelineData = prepareTimelineData(commitsData);
    const timelineSpec = createTimelineChart(timelineData);
    vegaEmbed('#viz-timeline', timelineSpec, {
        actions: { export: true, source: false, compiled: false, editor: false }
    }).catch(console.error);

    // Initialize interactive commits table
    new CommitsTable(commitsData);
});
