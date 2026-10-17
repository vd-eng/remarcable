// Show/hide the filter side panel and remember the choice across page reloads.
(function () {
    const STORAGE_KEY = 'products.filterPanelCollapsed';

    function readCollapsed() {
        try {
            return localStorage.getItem(STORAGE_KEY) === '1';
        } catch (e) {
            return false;
        }
    }

    function saveCollapsed(collapsed) {
        try {
            localStorage.setItem(STORAGE_KEY, collapsed ? '1' : '0');
        } catch (e) {
            // Storage unavailable (e.g. private mode); the toggle still works for this page.
        }
    }

    document.addEventListener('DOMContentLoaded', function () {
        const layout = document.querySelector('.layout');
        const toggle = document.querySelector('.panel-toggle');
        if (!layout || !toggle) {
            return;
        }

        function apply(collapsed) {
            layout.classList.toggle('panel-collapsed', collapsed);
            toggle.setAttribute('aria-expanded', String(!collapsed));
            toggle.textContent = collapsed ? 'Show filters' : 'Hide filters';
        }

        apply(readCollapsed());

        toggle.addEventListener('click', function () {
            const collapsed = !layout.classList.contains('panel-collapsed');
            apply(collapsed);
            saveCollapsed(collapsed);
        });
    });
})();
